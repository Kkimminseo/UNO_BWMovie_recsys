import axiosInstance from './axios';

export const movieApi = {
  getInitialMovies: () => {
    return axiosInstance.get('/movie/movielist/');
  },

  saveMoviePreferences: (selectedMovies) => {
    return axiosInstance.post('/movie/moviepreference/', {
      movie_id_fk: selectedMovies
    });
  }
}; 