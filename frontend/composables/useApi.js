import axios from 'axios';
import { useAuthStore } from '../stores/auth';
import { useRuntimeConfig } from '#app';
import qs from 'qs';

export const useApi = () => {
  const config = useRuntimeConfig();
  
  const apiClient = axios.create({
    baseURL: config.public.apiBaseUrl,
    headers: {
      'Content-Type': 'application/json',
    },
    paramsSerializer: params => qs.stringify(params, { arrayFormat: 'repeat' })
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

  const updateProfile = (formData) => {
    return apiClient.patch('auth/profile/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  };

  const requestPasswordReset = (email) => {
    return apiClient.post('auth/password-reset/', { email });
  };

  const confirmPasswordReset = (token, password) => {
    return apiClient.post('auth/password-reset/confirm/', { token, password });
  };

  const changePassword = (passwordData) => apiClient.post('auth/change-password/', passwordData);

  const getReviews = (params) => apiClient.get('reviews/', { params });

  const toggleLikeReview = (reviewId) => {
    return apiClient.post(`reviews/${reviewId}/like/`);
  };

  const addReview = (reviewData) => apiClient.post('reviews/', reviewData);

  const updateReview = (reviewId, reviewData) => apiClient.patch(`reviews/${reviewId}/`, reviewData);

  const deleteReview = (reviewId) => apiClient.delete(`reviews/${reviewId}/`);

  const getWatchlist = () => apiClient.get('watchlist/');
  
  const addToWatchlist = (movieId) => apiClient.post('watchlist/', { movie_id: movieId });

  const removeFromWatchlist = (watchlistItemId) => apiClient.delete(`watchlist/${watchlistItemId}/`);

  const updateWatchlistItem = (id, data) => apiClient.patch(`watchlist/${id}/`, data);

  const getCollections = () => apiClient.get('collections/');

  const getCollectionById = (id) => apiClient.get(`collections/${id}/`);

  const createCollection = (data) => apiClient.post('collections/', data);

  const deleteCollection = (id) => apiClient.delete(`collections/${id}/`);

  const addMovieToCollection = (collectionId, movieId) => apiClient.post(`collections/${collectionId}/add_movie/`, { movie_id: movieId });

  const removeMovieFromCollection = (collectionId, movieId) => apiClient.post(`collections/${collectionId}/remove_movie/`, { movie_id: movieId });

  const getActors = () => apiClient.get('actors/');

  const getActorById = (id) => apiClient.get(`actors/${id}/`);

  const getDirectorById = (id) => apiClient.get(`directors/${id}/`);

  const getUserById = (id) => apiClient.get(`users/${id}/`);

  const getRandomMovieId = async () => {
    // Použijeme náhodné řazení na backendu
    const response = await apiClient.get('movies/', { 
      params: { 
        ordering: '?', 
        limit: 1, 
        t: new Date().getTime() // Anti-cache
      } 
    });
    return response.data.results[0]?.id;
  };

  return {
    getMovies,
    getMovieById,
    getGenres,
    getActors,
    getActorById,
    getDirectorById,
    getUserById,
    getRandomMovieId,
    login,
    register,
    getProfile,
    updateProfile,
    requestPasswordReset,
    confirmPasswordReset,
    changePassword,
    getReviews,
    toggleLikeReview,
    addReview,
    updateReview,
    deleteReview,
    getWatchlist,
    addToWatchlist,
    removeFromWatchlist,
    updateWatchlistItem,
    getCollections,
    getCollectionById,
    createCollection,
    deleteCollection,
    addMovieToCollection,
    removeMovieFromCollection,
  };
};