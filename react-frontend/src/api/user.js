import axiosInstance from './axios';

export const getUserPreferences = async () => {
  try {
    const response = await axiosInstance.get('/preferences/');
    return response.data;
  } catch (error) {
    console.error('선호도 정보 가져오기 실패:', error);
    return {
      preferred_genres: [],
      preferred_movies: []
    };
  }
};

export const updateUserPreferences = async (preferences) => {
  try {
    const response = await axiosInstance.put('/preferences/', preferences);
    return response.data;
  } catch (error) {
    console.error('선호도 정보 업데이트 실패:', error);
    throw error;
  }
}; 