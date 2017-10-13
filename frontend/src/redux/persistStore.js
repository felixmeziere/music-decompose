import persistState from 'redux-localstorage';

function detectLocalStorage() {
  try {
    localStorage.setItem('a', 'a');
    localStorage.removeItem('a');
    return true;
  } catch (e) {
    return false;
  }
}

const localStorageDetected = detectLocalStorage();

const persistStore = localStorageDetected ? persistState(null, {
  deserialize: JSON.parse,
  key: 'redux',
  slicer: () => data => data,
}) : next => (reducer, initialState, enhancer) => next(reducer, initialState, enhancer);

export default persistStore;
