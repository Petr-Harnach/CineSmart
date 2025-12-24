import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const apiClient = axios.create({
  baseURL: 'http://127.00.1:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the auth token
apiClient.interceptors.request.use(config => {
  const authStore = useAuthStore();
  const token = authStore.accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

export const useApi = () => {
  const getMovies = (params) => {
    if (typeof params === 'string') { // Handle raw URL for pagination
      return apiClient.get(params);
    }
    return apiClient.get('movies/', { params });
  };
  
  const getMovieById = (id) => apiClient.get(`movies/${id}/`);

  const getGenres = () => apiClient.get('genres/');

  const login = (credentials) => apiClient.post('auth/login/', credentials);

  const register = (userData) => apiClient.post('auth/register/', userData);

  const getProfile = () => apiClient.get('auth/profile/');

  const addReview = (reviewData) => apiClient.post('reviews/', reviewData);

  const updateReview = (reviewId, reviewData) => apiClient.patch(`reviews/${reviewId}/`, reviewData);

  const deleteReview = (reviewId) => apiClient.delete(`reviews/${reviewId}/`);

  const getWatchlist = () => apiClient.get('watchlist/');
  
  const addToWatchlist = (movieId) => apiClient.post('watchlist/', { movie_id: movieId });

  const removeFromWatchlist = (watchlistItemId) => apiClient.delete(`watchlist/${watchlistItemId}/`);

  return {
    getMovies,
    getMovieById,
    getGenres,
    login,
    register,
    getProfile,
    addReview,
    updateReview,
    deleteReview,
    getWatchlist,
    addToWatchlist,
    removeFromWatchlist,
  };
};