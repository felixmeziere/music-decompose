import { types } from 'redux/actions/uploadSong';

const initialState = {
  loading: false,
  message: '',
  errors: {
    uploadSong: '',
  },
};

export default function reducer(state = initialState, action = {}) {
  switch (action.type) {
    case types.SET_UPLOAD_SONG_FIELD:
      return {
        ...state,
        [action.field]: action.value,
      };
    case types.UPLOAD_SONG.SUCCESS:
      return {
        ...state,
        message: action.message,
        loading: false,
      };
    case types.UPLOAD_SONG.FAILURE:
      return {
        ...state,
        message: 'An error has occured.',
        loading: false,
        errors: {
          ...state.errors,
          uploadSong: action.message,
        },
      };
    default:
      return state;
  }
}
