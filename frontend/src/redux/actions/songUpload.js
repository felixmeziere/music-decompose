export const types = {
  SET_SONG_UPLOAD_FIELD: 'SET_SONG_UPLOAD_FIELD',
  ADD_SONG: {
    REQUEST: 'ADD_SONG_REQUEST',
    SUCCESS: 'ADD_SONG_SUCCESS',
    FAILURE: 'ADD_SONG_FAILURE',
  },
};

export const setSongUploadField = (field, value) => ({
  type: types.SET_SONG_UPLOAD_FIELD,
  field,
  value,
});

export const addSong = () => ({
  type: types.ADD_SONG.REQUEST,
});

export const addSongSuccess = (data = { message: '' }) => ({
  type: types.ADD_SONG.SUCCESS,
  data,
});
export const addSongFailure = errorObject => ({
  type: types.ADD_SONG.FAILURE,
  errorObject,
});

