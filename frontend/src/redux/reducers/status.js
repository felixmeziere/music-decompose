import { types } from 'redux/actions/songUpload';

const initialState = {
  loading: false,
  message: '',
  errors: {
    songUpload: '',
  },
};

export default function reducer(state = initialState, action = {}) {
  switch (action.type) {
    case types.ADD_SONG.SUCCESS:
      return {
        ...state,
        message: action.data.message,
        loading: false,
      };
    case types.ADD_SONG.FAILURE:
      return {
        ...state,
        message: 'An error has occured.',
        loading: false,
        errors: {
          ...state.errors,
          songUpload: action.message,
        },
      };
    default:
      return state;
  }
}
