import api from './api';

export const storyService = {
  generateStory: async (storyData) => {
    try {
      const response = await api.post('/api/v1/generate', {
        name: storyData.name,
        personality: storyData.personality,
        setting: storyData.setting,
        theme: storyData.theme,
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  checkHealth: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};
