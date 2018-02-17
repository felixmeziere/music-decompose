import { connect } from 'react-redux';
import {
  addSong,
  setSongUploadField,
} from 'redux/actions/songUpload';
import HomePage from './HomePage';

const mapStateToProps = ({ status, songUpload }) => ({
  loading: status.loading,
  errorMessage: status.errors.songUpload,
  message: status.message,
  title: songUpload.title,
  songFile: songUpload.file,
  songUUID: songUpload.songUUID,
});

const mapDispatchToProps = {
  addSong,
  setSongUploadField,
};

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(HomePage);
