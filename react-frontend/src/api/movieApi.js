import axiosInstance from './axios';

export const movieApi = {
  getInitialMovies: () => {
    return axiosInstance.get('/api/movies/movielist/');
  },

  saveMoviePreferences: (selectedMovies) => {
    return axiosInstance.post('/api/movies/moviepreference/', {
      movie_id_fk: selectedMovies
    });
  }
}; 