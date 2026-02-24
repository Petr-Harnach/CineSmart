import axios from 'axios';
import { useAuthStore } from '../stores/auth';
import { useRuntimeConfig } from '#app';
import { ref } from 'vue';
import qs from 'qs';

// Globální stav pro indikaci probouzení backendu
export const isBackendWakingUp = ref(false);

export const useApi = () => {
  const config = useRuntimeConfig();
  
  const apiClient = axios.create({
    baseURL: config.public.apiBaseUrl,
    timeout: 30000, // Zvýšíme timeout na 30s pro studené starty
    headers: {
      'Content-Type': 'application/json',
    },
    paramsSerializer: params => qs.stringify(params, { arrayFormat: 'repeat' })
  });

  // Interceptor pro request (přidání tokenu)
  apiClient.interceptors.request.use(config => {
    const authStore = useAuthStore();
    const token = authStore.accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  }, error => Promise.reject(error));

  // Interceptor pro response (detekce probouzení a retry)
  apiClient.interceptors.response.use(
    response => {
      // Pokud se podařilo dostat odpověď, server je vzhůru
      isBackendWakingUp.value = false;
      return response;
    },
    async error => {
      const { config, response } = error;
      
      // Pokud je chyba 502, 503, 504 nebo Timeout (Render se probouzí)
      if (!response || [502, 503, 504].includes(response.status)) {
        isBackendWakingUp.value = true;
        
        // Zkusíme retry po 5 sekundách (maximálně 3x)
        config._retryCount = config._retryCount || 0;
        if (config._retryCount < 3) {
          config._retryCount += 1;
          console.warn(`Backend se probouzí, zkouším znovu (${config._retryCount}/3)...`);
          
          await new Promise(resolve => setTimeout(resolve, 5000));
          return apiClient(config);
        }
      }
      
      return Promise.reject(error);
    }
  );
  
  const getMovies = (params) => {
    if (typeof params === 'string') {
      return apiClient.get(params);
    }
    return apiClient.get('movies/', { params });
  };
  
  const getMovieById = (id) => apiClient.get(`movies/${id}/`);
  const getGenres = () => apiClient.get('genres/');
  const login = (credentials) => apiClient.post('auth/login/', credentials);
  const register = (userData) => apiClient.post('auth/register/', userData);
  const getProfile = () => apiClient.get('auth/profile/');
  const updateProfile = (formData) => apiClient.patch('auth/profile/', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
  const requestPasswordReset = (email) => apiClient.post('auth/password-reset/', { email });
  const confirmPasswordReset = (token, password) => apiClient.post('auth/password-reset/confirm/', { token, password });
  const changePassword = (passwordData) => apiClient.post('auth/change-password/', passwordData);
  const getReviews = (params) => apiClient.get('reviews/', { params });
  const toggleLikeReview = (reviewId) => apiClient.post(`reviews/${reviewId}/like/`);
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
    const response = await apiClient.get('movies/', { params: { ordering: '?', limit: 1, t: new Date().getTime() } });
    return response.data.results[0]?.id;
  };

  return {
    getMovies, getMovieById, getGenres, getActors, getActorById, getDirectorById, getUserById, getRandomMovieId,
    login, register, getProfile, updateProfile, requestPasswordReset, confirmPasswordReset, changePassword,
    getReviews, toggleLikeReview, addReview, updateReview, deleteReview, getWatchlist, addToWatchlist, 
    removeFromWatchlist, updateWatchlistItem, getCollections, getCollectionById, createCollection, 
    deleteCollection, addMovieToCollection, removeMovieFromCollection,
  };
};