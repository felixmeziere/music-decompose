import { call, put, takeEvery } from 'redux-saga/effects';
import {
  types,
  uploadSongSuccess,
  uploadSongFailure,
} from 'redux/actions/uploadSong';
import {
  callUploadSong,
} from 'services/api';

function* uploadSongSaga() {
  try {
    const uploadResponse = yield call(
      callUploadSong,
      'toto',
    );
    yield put(uploadSongSuccess(uploadResponse));
  } catch (errorObject) {
    yield put(uploadSongFailure(errorObject));
  }
}


function* watchUploadSong() {
  yield takeEvery(types.UPLOAD_SONG.REQUEST, uploadSongSaga);
}

export default watchUploadSong;
