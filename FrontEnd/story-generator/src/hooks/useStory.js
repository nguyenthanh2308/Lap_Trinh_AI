import { useState } from 'react';
import { storyService } from '../services/storyService';

export const useStory = () => {
  const [story, setStory] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generateStory = async (storyData) => {
    setLoading(true);
    setError(null);
    try {
      const result = await storyService.generateStory(storyData);
      setStory(result.story);
      return result;
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'Failed to generate story';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const resetStory = () => {
    setStory('');
    setError(null);
  };

  return {
    story,
    loading,
    error,
    generateStory,
    resetStory,
  };
};
