import { combineReducers } from 'redux';
import { routerReducer } from 'react-router-redux';
import status from './status';
import songUpload from './songUpload';

export default combineReducers({
  status,
  songUpload,
  routing: routerReducer,
});
