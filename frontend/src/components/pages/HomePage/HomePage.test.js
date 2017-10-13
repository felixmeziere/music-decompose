import React from 'react';
import renderer from 'react-test-renderer';
import HomePage from './HomePage';

it('renders without crashing', () => {
  const component = renderer.create(<HomePage
    loading={false}
    errorMessage="There is an error."
    message="Totor Panache"
    uploadSong={() => {}}
    setUploadSongField={() => {}}
  />);
  const tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});
