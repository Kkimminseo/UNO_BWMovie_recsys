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
    const refresh_token = localStorage.getItem('refresh_token');
    await axiosInstance.post('/account/logout/', { refresh: refresh_token });
    // 로컬 스토리지 토큰 제거
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  } catch (error) {
    throw error.response.data;
  }
};

// 액세스 토큰 가져오기
export const getAccessToken = () => {
  return localStorage.getItem('access_token');
}; 