import axios from 'axios';
import { refreshToken } from './auth';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터 - 토큰이 필요한 요청에 자동으로 토큰 추가
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터 - 토큰이 만료되었을 때 자동으로 갱신
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // 토큰이 만료되었고, 이전에 재시도하지 않았다면
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // 토큰 갱신 시도
        const newToken = await refreshToken();
        
        // 새로운 토큰으로 헤더 업데이트
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        
        // 원래 요청 재시도
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        // 토큰 갱신에 실패하면 로그인 페이지로 리다이렉트
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default axiosInstance; 