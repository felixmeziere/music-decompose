import React from 'react';
import { Route } from 'react-router';
import { ConnectedRouter, routerMiddleware } from 'react-router-redux';
import createHistory from 'history/createBrowserHistory';
import {
  HomePage,
} from 'components/pages';
import { App } from 'components';

const history = createHistory();
export const routeMiddleware = routerMiddleware(history);

const router = () => (
  <ConnectedRouter history={history}>
    <App>
      <div>
        <Route exact path="/" component={HomePage} />
      </div>
    </App>
  </ConnectedRouter>
);

export default router;
