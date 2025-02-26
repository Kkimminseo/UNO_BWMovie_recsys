import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,  // ✅ CSRF 쿠키를 포함하도록 설정
  headers: {
    'Content-Type': 'application/json',
  },
});

// ✅ CSRF 토큰을 강제 요청하여 가져오기
const getCSRFToken = async () => {
  try {
    const response = await axiosInstance.get('/account/csrf-token/');
    console.log("CSRF Token:", response.data.csrfToken);
  } catch (error) {
    console.error("CSRF Token 요청 실패:", error);
  }
};

// ✅ 요청을 보내기 전에 CSRF 토큰과 JWT 액세스 토큰을 자동으로 추가
axiosInstance.interceptors.request.use(
  (config) => {
    // CSRF 토큰 추가
    const csrfToken = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1];

    if (csrfToken) {
      config.headers["X-CSRFToken"] = csrfToken;
    }

    // JWT 액세스 토큰 추가
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// ✅ CSRF 토큰을 미리 가져오기
getCSRFToken();

// 응답 인터셉터: 토큰 만료 시 자동 갱신
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // 401 에러이고 재시도하지 않은 요청인 경우
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refresh_token = localStorage.getItem('refresh_token');
        const response = await axiosInstance.post('/account/token/refresh/', {
          refresh: refresh_token
        });
        
        const { access } = response.data;
        localStorage.setItem('access_token', access);
        originalRequest.headers['Authorization'] = `Bearer ${access}`;
        
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        // 리프레시 토큰도 만료된 경우
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default axiosInstance;
