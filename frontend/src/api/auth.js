import axios from 'axios';
import { BASE_URL, ENDPOINTS } from './config';

const api = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
});

export const authAPI = {
  signup: async (userData) => {
    try {
      const response = await api.post(ENDPOINTS.SIGNUP, userData);
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : error;
    }
  },

  login: async (credentials) => {
    try {
      const response = await api.post(ENDPOINTS.LOGIN, credentials);
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : error;
    }
  },

  logout: async () => {
    try {
      const response = await api.post(ENDPOINTS.LOGOUT);
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : error;
    }
  },
}; 