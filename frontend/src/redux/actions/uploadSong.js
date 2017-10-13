export const types = {
  SET_UPLOAD_SONG_FIELD: 'SET_UPLOAD_SONG_FIELD',
  UPLOAD_SONG: {
    REQUEST: 'UPLOAD_SONG_REQUEST',
    SUCCESS: 'UPLOAD_SONG_SUCCESS',
    FAILURE: 'UPLOAD_SONG_SUCCESS ',
  },
};

export const setUploadSongField = (field, value) => ({
  type: types.SET_UPLOAD_SONG_FIELD,
  field,
  value,
});

export const uploadSong = () => ({
  type: types.UPLOAD_SONG.REQUEST,
});

export const uploadSongSuccess = () => ({
  type: types.UPLOAD_SONG.SUCCESS,
});
export const uploadSongFailure = () => ({
  type: types.UPLOAD_SONG.FAILURE,
});
