import { connect } from 'react-redux';
import { uploadSong, setUploadSongField } from 'redux/actions/uploadSong';
import HomePage from './HomePage';

const mapStateToProps = ({ status }) => ({
  loading: status.loading,
  errorMessage: status.errors.uploadSong,
  message: status.message,
});

const mapDispatchToProps = {
  uploadSong,
  setUploadSongField,
};

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(HomePage);
