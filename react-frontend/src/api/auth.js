import axios from 'axios';
import axiosInstance from './axios';

// 회원가입 API
export const signup = async (userData) => {
  try {
    const response = await axiosInstance.post('/account/signup/', userData);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

// 토큰 갱신 API
export const refreshToken = async () => {
  try {
    const refresh = localStorage.getItem('refresh_token');
    if (!refresh) throw new Error('No refresh token');

    const response = await axios.post('http://localhost:8000/api/v1/account/token/refresh/', {
      refresh: refresh
    });
    
    const { access } = response.data;
    localStorage.setItem('access_token', access);
    return access;
  } catch (error) {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    throw error;
  }
};

// 로그인 API
export const login = async (credentials) => {
  try {
    const response = await axiosInstance.post('/account/login/', credentials);
    const { access, refresh } = response.data;
    // 토큰 저장
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

// 로그아웃 API
export const logout = async () => {
  try {
    const refresh = localStorage.getItem('refresh_token');
    await axiosInstance.post('/account/logout/', { refresh });
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  } catch (error) {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    throw error.response.data;
  }
}; 