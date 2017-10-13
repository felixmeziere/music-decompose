import { combineReducers } from 'redux';
import { routerReducer } from 'react-router-redux';
import status from './status';

export default combineReducers({
  status,
  routing: routerReducer,
});
