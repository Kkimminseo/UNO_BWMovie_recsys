import axiosInstance from './axios';

export const sendMessage = async (message) => {
  try {
    const response = await axiosInstance.post('/chat/', { message });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
}; 