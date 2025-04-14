import React, { useState } from 'react';
import { View, Button, Platform } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import axios from 'axios';

const App = () => {
  const [videoUri, setVideoUri] = useState(null);

  const pickVideo = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Videos,
      quality: 1,
    });
    if (!result.cancelled) {
      setVideoUri(result.uri);
    }
  };

  const uploadVideo = async () => {
    const formData = new FormData();
    formData.append('file', {
      uri: videoUri,
      name: 'video.mp4',
      type: 'video/mp4',
    });

    try {
      const response = await axios.post('http://your_backend_url/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert(response.data.message);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <View>
      <Button title="Pick Video" onPress={pickVideo} />
      {videoUri && <Button title="Upload Video" onPress={uploadVideo} />}
    </View>
  );
};

export default App;
