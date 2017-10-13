import { createStore, applyMiddleware, compose } from 'redux';
import createSagaMiddleware from 'redux-saga';

import reducers from './reducers';
import { routeMiddleware } from '../router';
import rootSaga from './sagas';
import persistStore from './persistStore';

const sagaMiddleware = createSagaMiddleware();

const middlewares = applyMiddleware(routeMiddleware, sagaMiddleware);
const enhancer = compose(middlewares, persistStore);

const store = createStore(
  reducers,
  window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__(), // eslint-disable-line
  enhancer,
);

sagaMiddleware.run(rootSaga);

export default store;
