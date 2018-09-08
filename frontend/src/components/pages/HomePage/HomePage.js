import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';

class HomePage extends PureComponent {
  handleSubmit(e) {
    e.preventDefault();
    this.props.addSong();
  }

  render() {
    const {
      message,
      loading,
      setSongUploadField,
      errorMessage,
      songUUID,
      title,
      file,
    } = this.props;

    return (
      <div>
        <div>Error Message:</div>
        <div>{errorMessage}</div>
        <div>Message:</div>
        <div>{message}</div>
        <div>Loading?</div>
        <div>{loading ? 'Yes' : 'No'}</div>
        <div>
          <input
            onChange={e => setSongUploadField('title', e.target.value)}
            type="text"
            value={title}
          />
          <input
            onChange={e => setSongUploadField('file', e.target.files[0])}
            type="file"
            value={file}
          />
          <button onClick={e => this.handleSubmit(e)}>TOTOR panache</button>
        </div>
        { songUUID &&
        <h2>UUID: {songUUID}</h2>
        }
      </div>
    );
  }
}

HomePage.propTypes = {
  addSong: PropTypes.func.isRequired,
  loading: PropTypes.bool.isRequired,
  errorMessage: PropTypes.string,
  message: PropTypes.string.isRequired,
  setSongUploadField: PropTypes.func.isRequired,
  title: PropTypes.string.isRequired,
  file: PropTypes.any.isRequired,
  songUUID: PropTypes.string.isRequired,
};

HomePage.defaultProps = {
  errorMessage: '',
};

export default HomePage;
