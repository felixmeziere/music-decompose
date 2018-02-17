import { fork } from 'redux-saga/effects';
import watchSongUpload from './songUpload';

export default function* rootSaga() {
  yield [
    fork(watchSongUpload),
  ];
}
