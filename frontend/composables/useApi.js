import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const useApi = () => {
  const getMovies = () => apiClient.get('movies/');
  
  // Add other API calls here later, e.g.:
  // const getMovieById = (id) => apiClient.get(`/movies/${id}/`);

  return {
    getMovies,
  };
};
