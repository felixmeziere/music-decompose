import { types } from 'redux/actions/songUpload';

const initialState = {
  file: '',
  fileUUID: '',
  songUUID: '',
  title: '',
};

export default function reducer(state = initialState, action = {}) {
  switch (action.type) {
    case types.SET_SONG_UPLOAD_FIELD:
      return {
        ...state,
        [action.field]: action.value,
      };
    case types.ADD_SONG.SUCCESS:
      return {
        ...state,
        songUUID: action.data.uuid,
        fileUUID: action.data.files,
      };
    default:
      return state;
  }
}
