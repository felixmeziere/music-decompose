import React from 'react';
import PropTypes from 'prop-types';

const App = props => (
  <div>
    {props.children}
  </div>
);

App.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node,
  ]),
};

App.defaultProps = {
  children: null,
};

export default App;
