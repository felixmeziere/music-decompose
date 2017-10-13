import React from 'react';
import PropTypes from 'prop-types';

const HomePage = props => (
  <div>
    <div>Error Message:</div>
    <div>{props.errorMessage}</div>
    <div>Message:</div>
    <div>{props.message}</div>
    <div>Loading?</div>
    <div>{props.loading ? 'Yes' : 'No'}</div>
    <form
      onSubmit={(e) => {
        e.preventDefault();
        props.uploadSong();
      }}
    >
      <input
        onChange={(e) => {
          e.preventDefault();
          props.setUploadSongField('file', e.target.value);
        }}
        type="text"
      />
      <input type="submit" />
    </form>
    <submit />
  </div>
);

HomePage.propTypes = {
  loading: PropTypes.bool.isRequired,
  errorMessage: PropTypes.string.isRequired,
  message: PropTypes.string.isRequired,
  uploadSong: PropTypes.func.isRequired,
  setUploadSongField: PropTypes.func.isRequired,
};

export default HomePage;
