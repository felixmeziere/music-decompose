# pylint: skip-file

# # v. 06/15/18

import numpy as np
import scipy as sp
import pandas as pd
import _pickle as pkl
import matplotlib.pyplot as plt
import time
import os
import itertools
import sys
import math
import csv
from cvxopt import matrix, solvers
from sklearn import linear_model, mixture, datasets, preprocessing
from IPython.core.interactiveshell import InteractiveShell
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils, plot_model

InteractiveShell.ast_node_interactivity = "all"
solvers.options['show_progress'] = False


def normalize(v):
    '''
    Docstring please
    '''
    if np.sum(v) == 0:
        w = np.copy(v)
        w[0] = 1
        return w
    return v / np.sum(v)


def flatten_Ei(index, dim):
    '''
    Docstring please
    '''
    Ei = np.zeros((dim, dim))
    Ei[index, index] = 1
    return Ei.flatten()


def create_diagonal(cov_matrix, multiKN_par, method_diagonal):
    '''
    Docstring please
    '''
    if method_diagonal == 'SDP_diagonal':
        dim = cov_matrix.shape[0]
        c = matrix(-np.ones(dim))
        Gl = matrix(np.vstack([-np.identity(dim), np.identity(dim)]))
        hl = matrix(np.hstack([np.zeros(dim), np.ones(dim)]))
        Gs = [matrix(np.vstack([flatten_Ei(l, dim) for l in range(dim)]).T)]
        hs = [matrix(multiKN_par * cov_matrix)]
        result = solvers.sdp(c, Gl=Gl, hl=hl, Gs=Gs, hs=hs)
        diagonal = np.diag((np.array(result['x'])[:, 0])) * 0.9999
    else:
        print('Method not implemented')
    return diagonal


def knockoff_performance(selected, true):
    '''
    Docstring please
    '''
    if len(selected) == 0:
        return 0, 0
    FDR = len(set(selected).difference(set(true))) / len(selected)
    Power = len(set(selected).intersection(set(true))) / len(true)
    return FDR, Power


class generate_knockoff(object):
    '''
    INPUTS:
    X -- type np.array(dim,n_samples)
    n_clusters -- type int: number of clusters
    multiKN -- type int: number of simultaneous knockoffs. (Default = 1)

    OUTPUT:
    self.X_KN -- type np.array(dim,n_samples) : knockoffs for dataset X
    '''

    def __init__(self, X, n_clustersKN, method_diagonal='SDP_diagonal', multiKN=1):
        self.X = X                                  # PRINCIPAL INPUT : dataset X
        self.n_samples = self.X.shape[0]            # computed parameter from X
        self.dim = self.X.shape[1]                  # computed parameter from X
        self.n_clustersKN = n_clustersKN
        self.multiKN = multiKN

        self.EM = mixture.GaussianMixture(n_components=self.n_clustersKN)
        self.EM.fit(self.X)

        self._compute_matrix(method_diagonal=method_diagonal)
        self._compute_knockoff()

    def _compute_matrix(self, method_diagonal):
        '''
        Docstring please
        '''
        self.diagonal_clusters, self.SigmaInvDiag_clusters, self.SigmaChol_clusters = {}, {}, {}
        for cluster in range(self.n_clustersKN):
            self.diagonal_clusters[str(cluster)],
            self.SigmaInvDiag_clusters[str(cluster)],
            self.SigmaChol_clusters[str(cluster)] = self._KN_distribution(
                cov_matrix=self.EM.covariances_[cluster, ], method_diagonal=method_diagonal)

    def _compute_knockoff(self):
        '''
        Docstring please
        '''
        self.X_KN, self.clusterKN = [], []
        for samp in range(self.n_samples):
            X_KN, clusterKN = self._sample_KN(self.X[samp, :])
            self.X_KN.append(X_KN)
            self.clusterKN.append(clusterKN)
        self.X_KN = np.stack(self.X_KN, axis=0)

    def _KN_distribution(self, cov_matrix, method_diagonal):
        '''
        Docstring please
        '''
        multiKN_par = (self.multiKN + 1) / self.multiKN
        diagonal = create_diagonal(
            cov_matrix=cov_matrix, multiKN_par=multiKN_par, method_diagonal=method_diagonal)
        SigmaInvDiag = np.linalg.solve(cov_matrix, diagonal)
        Sigma_k = 2 * diagonal - diagonal.dot(SigmaInvDiag)
        Sigma_k = np.tile(Sigma_k - diagonal, reps=(self.multiKN, self.multiKN)
                          ) + np.diag(np.tile(np.diag(diagonal), reps=self.multiKN))
        SigmaChol = np.linalg.cholesky(
            Sigma_k + (1e-7) * np.identity(self.dim * self.multiKN)).T
        return np.diag(diagonal), SigmaInvDiag, SigmaChol

    def _sample_KN(self, X_ind):
        '''
        Docstring please
        '''
        cat_post = [self.EM.weights_[cluster, ] * sp.stats.multivariate_normal.pdf(x=X_ind, mean=self.EM.means_[cluster, ], cov=self.EM.covariances_[cluster, ])
                    for cluster in range(self.n_clustersKN)]
        clusterKN = np.random.choice(
            self.n_clustersKN, size=1, p=normalize(cat_post))[0]
        X_KN = np.tile(
            X_ind -
            np.matmul(X_ind - self.EM.means_[clusterKN, ],
                      self.SigmaInvDiag_clusters[str(clusterKN)]),
            reps=self.multiKN,
        ) + np.matmul(
            np.random.normal(size=self.dim * self.multiKN),
            self.SigmaChol_clusters[str(clusterKN)],
        )
        return X_KN, clusterKN
    ####################################


def generate_mixture_par(n_clusters, dim, spread_means=10, extra_cor=0):
    '''
    Docstring please
    '''
    parameters = {}
    parameters['cluster_prop'] = normalize(np.random.poisson(10, n_clusters))
    for cluster in range(n_clusters):
        parameters['mean' + str(cluster)] = np.random.multivariate_normal(
            mean=np.zeros(dim), cov=spread_means * np.identity(dim))
        parameters['cov' + str(cluster)] = datasets.make_spd_matrix(
            n_dim=dim) + extra_cor * np.ones(shape=(dim, dim))
    return parameters


def generate_response(X, **params):
    '''
    Docstring please
    '''
    Y = []
    funct = params['funct']
    pol_deg, trigo, feature_transform = params.get('pol_deg', 1), params.get(
        'trigo', False), params.get('feature_transform', None)

    expanded_X = [X]
    if pol_deg > 1:
        expanded_X.append(np.stack([np.prod(X[:, i], axis=1) for i in itertools.product(
            range(X.shape[1]), repeat=pol_deg)], axis=1))
    if trigo:
        expanded_X.append(np.cos(X))
    if feature_transform is not None:
        expanded_X.append(feature_transform(X, **params))
    expanded_X = np.hstack(expanded_X)

    for i in range(X.shape[0]):
        y = funct(x=expanded_X[i, :], **params)
        Y.append(y)

    return Y


def get_W(importance_scores, multiKN, antisym, **params_kn):
    '''
    Docstring please
    '''
    dim = int(len(importance_scores) / (multiKN + 1))
    if antisym == 'difference':
        W = list(map(lambda x, y: x - y,
                     importance_scores[0:dim], importance_scores[dim:2 * dim]))
    elif (antisym == 'multiKN_difference') and (multiKN > 1):
        W = np.sum([list(map(lambda x, y: x - y, importance_scores[0:dim],
                             importance_scores[(k + 1) * dim:(k + 2) * dim])) for k in range(multiKN)], axis=0)
    elif (antisym == 'multiKN_rank') and (multiKN > 1):
        W = np.array([(sp.stats.rankdata([importance_scores[i + k * dim]
                                          for k in range(multiKN + 1)])[0] - (multiKN + 1) / 2) for i in range(dim)])
    else:
        raise ValueError("No other antisymmetric functions are implemented")
    return W


class knockoff_procedure(object):
    '''
    For a given dataset of X, X_KN, Y, we run the knockoff selection procedure. 2 main steps:
    - First, computing the importance scores for each covariate by defining a method. If using NN, give extra arguments.
    - Second, running the selection procedure by defining an antisymmetric function to get the W scores from the importance scores, and then get the selection set by defining a FDR target and fixing the offset (Knockoff / Knockoff+).
    '''

    def __init__(self, FDR=0.2, offset=1, multiKN=1):
        self.FDR = FDR
        self.offset = offset
        self.multiKN = multiKN
        self.W = None
        self.dim = None

    def get_importance_scores(self, X, X_KN, Y, method, **params_kn):
        '''
        Docstring please
        '''
        dim = X.shape[1]
        full_covariate = np.hstack((X, X_KN))
        if method == 'LogisticRegression':
            reg = linear_model.LogisticRegressionCV()
            reg.fit(full_covariate, Y)
            self.importance_scores = abs(reg.coef_[0, :])
        elif method == 'LinearRegression':
            reg = linear_model.LinearRegression()
            reg.fit(full_covariate, Y)
            self.importance_scores = abs(reg.coef_)
        elif method == 'LassoCV':
            reg = linear_model.LassoCV()
            reg.fit(full_covariate, Y)
            self.importance_scores = abs(reg.coef_)
        elif method == 'ScoresSwapLasso':
            assert(len(params_kn['steps_lambda']) == 1)
            self.importance_scores = ScoresSwapLasso(
                full_covariate, Y, **params_kn)
        elif method == 'NNClassifierAccuracyMultiKN':
            self.importance_scores = NNClassifierAccuracyMultiKN(
                full_covariate, Y, dim, self.multiKN, **params_kn)
        else:
            raise ValueError(
                "No other importance score methods are implemented")

    def get_selections(self, antisym, **params_kn):
        '''
        Docstring please
        '''
        self.W = get_W(importance_scores=self.importance_scores,
                       multiKN=self.multiKN, antisym=antisym, **params_kn)
        sorted_abs_W, ratios = np.sort(np.absolute(self.W)), []
        for index in range(self.dim):
            above = np.count_nonzero(
                [x >= sorted_abs_W[index] for x in self.W])
            below = np.count_nonzero(
                [x <= - sorted_abs_W[index] for x in self.W])
            ratios.append(((self.offset + below) / np.maximum(above, 0.001)))
        if np.sum([ratio < self.FDR for ratio in ratios]) == 0:
            self.threshold, self.selected = None, []
        else:
            self.threshold = sorted_abs_W[np.min(
                [ind for ind in range(self.dim) if ratios[ind] < self.FDR])]
            self.selected = np.where(self.W >= self.threshold)[0]

        if params_kn.get('plotting_scores', False):
            plot_scores(self.importance_scores, self.W, self.threshold)


class generate_data(generate_knockoff, knockoff_procedure):
    '''
    INPUTS:
    self.n_samples -- type int: number of samples (direct input)
    self.n_clusters -- type int: number of clusters (direct input)
    self.dim -- type int: dimension of the covariates (direct input)
    '''

    def __init__(self, n_samples, n_clusters, dim):
        self.n_samples = n_samples
        self.n_clusters = n_clusters
        self.dim = dim

        self.parameters_gen = generate_mixture_par(
            n_clusters=self.n_clusters, dim=self.dim)
        self.parameters_kn = {}

        self.generate_X()

    def generate_X(self):
        '''
        Docstring please
        '''
        self.X = np.empty((self.n_samples, self.dim))
        self.assignments = np.random.choice(
            self.n_clusters, size=self.n_samples, p=self.parameters_gen['cluster_prop'])
        for i in range(self.n_samples):
            self.X[i, :] = np.random.multivariate_normal(mean=self.parameters_gen['mean' + str(
                self.assignments[i])], cov=self.parameters_gen['cov' + str(self.assignments[i])])

    def generate_Y(self, non_null, **params_gen):
        '''
        Docstring please
        '''
        self.parameters_gen['non_null'], self.parameters_gen['response_parameters'] = non_null, params_gen
        self.Y = generate_response(X=self.X[:, non_null], **params_gen)

    def generate_X_KN(self, n_clustersKN, multiKN):
        '''
        Docstring please
        '''
        self.parameters_kn['n_clustersKN'], self.parameters_kn['multiKN'] = n_clustersKN, multiKN
        generate_knockoff.__init__(
            self, X=self.X, n_clustersKN=n_clustersKN, multiKN=multiKN)

    def generate_selection(self, **params_kn):
        '''
        Docstring please
        '''
        knockoff_procedure.__init__(self, FDR=params_kn.get('FDR', 0.2), offset=params_kn.get(
            'offset', 1), multiKN=self.parameters_kn['multiKN'])
        method = params_kn.get('method', None)
        antisym = params_kn.get('antisym', None)
        if method is not None:
            self.parameters_kn['method'] = method
            self.get_importance_scores(
                X=self.X, X_KN=self.X_KN, Y=self.Y, **params_kn)
            if antisym is not None:
                self.parameters_kn['antisym'] = antisym
                self.get_selections(**params_kn)

    def generate_performance(self):
        '''
        Docstring please
        '''
        return knockoff_performance(selected=self.selected, true=self.parameters_gen['non_null'])


def create_NN(input_dim, n_classes, **params):
    '''
    Docstring please
    '''
    n_layers, n_nodes = params.get('n_layers', 3), params.get('n_nodes', 200)
    model = Sequential()
    model.add(Dense(n_nodes, input_shape=(input_dim,)))
    for _ in range(n_layers):
        model.add(Dense(n_nodes, activation='relu'))
        model.add(Dropout(0.7))
    model.add(Dense(n_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy'])
    return model


def NNClassifier(X_train, Y_train, **params):
    '''
    Docstring please
    '''
    verbose = params.get('verbose', 0)
    classifier = create_NN(input_dim=X_train.shape[1], n_classes=len(
        np.unique(Y_train)), **params)
    classifier.fit(X_train, Y_train, batch_size=256,
                   epochs=params.get('n_epochs', 100), verbose=verbose)
    return classifier


def ScoresSwapLasso(full_covariate, Y, **params):
    '''
    Docstring please
    '''
    verbose = params.get('verbose', 0)
    dim = int(full_covariate.shape[1] / 2)
    le = preprocessing.LabelEncoder()
    le.fit(Y)
    Y_categ = np_utils.to_categorical(le.transform(Y), len(le.classes_))

    classifier = params.get('classifier', NNClassifier(
        X_train=full_covariate, Y_train=Y_categ, **params))
    initial_accuracy = classifier.evaluate(
        full_covariate, Y_categ, verbose=verbose)[1]

    steps_lambda = params.get('steps_lambda', np.arange(0, 5, 0.5))
    importance_scores = np.zeros((2 * dim, len(steps_lambda)))

    for index_lambda, cur_lambda in enumerate(steps_lambda):
        for covariate in range(2 * dim):
            full_covariate_swap_local = np.copy(full_covariate)
            new_column = (full_covariate[:, (covariate + dim) % (2 * dim)] -
                          full_covariate[:, covariate]) * cur_lambda + full_covariate[:, covariate]
            full_covariate_swap_local[:, covariate] = new_column
            importance_scores[covariate, index_lambda] = initial_accuracy - \
                classifier.evaluate(full_covariate_swap_local,
                                    Y_categ, verbose=verbose)[1]
    return np.array(importance_scores)


def path_performance(importance_scores, non_null, dim, FDR, offset, steps_lambda, plot_path=False):
    '''
    Docstring please
    '''
    n_steps = len(steps_lambda)
    assert (importance_scores.shape[0] == 2 *
            dim) and (importance_scores.shape[1] == n_steps)
    full_W = importance_scores[0:dim, :] - importance_scores[dim:2 * dim, :]
    area = np.array([np.trapz(full_W[:, :L + 1], x=steps_lambda[:L + 1])
                     for L in range(n_steps)])
    results = np.zeros((2, 2, n_steps))
    rejections = {}
    if plot_path:
        plot_scores_Lasso(
            W=full_W, steps_lambda=steps_lambda, non_null=non_null)
        plot_scores_Lasso(
            W=area.T, steps_lambda=steps_lambda, non_null=non_null)
    for i, cur_lambda in enumerate(steps_lambda):
        knock = knockoff_procedure(verbose=False)
        knock.FDR = FDR
        knock.dim = dim
        knock.W = full_W[:, i]
        knock._get_threshold(offset=offset)
        knock._get_selections()
        results[0, :, i] = knockoff_performance(
            selected=knock.selected, true=non_null, verbose=False)
        knock.W = area.T[:, i]
        knock._get_threshold(offset=offset)
        knock._get_selections()
        if cur_lambda == 10:
            rejections[str(i)] = knock.selected
        results[1, :, i] = knockoff_performance(
            selected=knock.selected, true=non_null, verbose=False)
    return results, rejections


def plot_scores_Lasso(W, steps_lambda, non_null=None):
    '''
    Docstring please
    '''
    assert len(steps_lambda) == W.shape[1]
    dim = W.shape[0]
    for ind in range(dim):
        if non_null is not None:
            if np.in1d([ind], non_null):
                plt.plot(steps_lambda, W[ind, :], c='r')
            else:
                plt.plot(steps_lambda, W[ind, :], c='g')
        else:
            plt.plot(steps_lambda, W[ind, :])
    plt.show()


def plot_scores(importance_scores, W, threshold):
    '''
    Docstring please
    '''
    plt.plot(np.arange(len(importance_scores)), importance_scores, 'r+')
    plt.plot(np.arange(len(W)), W, 'g^')
    if threshold is not None:
        plt.axhline(y=threshold)
    plt.show()
