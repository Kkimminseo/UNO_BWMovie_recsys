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

// ✅ 요청을 보내기 전에 CSRF 토큰을 자동으로 추가
axiosInstance.interceptors.request.use(
  (config) => {
    const csrfToken = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1];

    if (csrfToken) {
      config.headers["X-CSRFToken"] = csrfToken;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// ✅ CSRF 토큰을 미리 가져오기
getCSRFToken();

export default axiosInstance;
