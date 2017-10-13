import { fork } from 'redux-saga/effects';
import watchUploadSong from './uploadSong';

export default function* rootSaga() {
  yield [
    fork(watchUploadSong),
  ];
}
