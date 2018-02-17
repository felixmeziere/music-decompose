import { select, call, put, takeEvery } from 'redux-saga/effects';
import {
  types,
  addSongSuccess,
  addSongFailure,
} from 'redux/actions/songUpload';
import { callAddSong } from 'services/api';

const getSongUpload = state => state.songUpload;

function* addSongSaga() {
  const songUpload = yield select(getSongUpload);
  try {
    const addResponse = yield call(
      callAddSong,
      songUpload,
    );
    yield put(addSongSuccess(addResponse.data));
  } catch (errorObject) {
    yield put(addSongFailure(errorObject));
  }
}

function* watchUploadSong() {
  yield takeEvery(types.ADD_SONG.REQUEST, addSongSaga);
}

export default watchUploadSong;
