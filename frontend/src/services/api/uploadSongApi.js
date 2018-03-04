import axios from 'axios';

const callAddSong = (payload) => {
  const data = new FormData();
  data.append('original_file', payload.file);
  data.append('title', payload.title);
  return axios.post(
    '/song/',
    data,
    {
      headers: {
        'Content-Type': payload.file.type,
        'Content-Disposition': `attachment; filename=${payload.file.name}`,
      },
    },
  );
};

export {
  callAddSong,
};
