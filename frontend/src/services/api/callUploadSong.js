import axios from 'axios';

export default message => axios.post(
  '/song/',
  message,
);

