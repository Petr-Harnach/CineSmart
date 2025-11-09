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
  const getMovies = () => apiClient.get('movies/');
  
  const getMovieById = (id) => apiClient.get(`movies/${id}/`);

  const login = (credentials) => apiClient.post('auth/login/', credentials);

  const register = (userData) => apiClient.post('auth/register/', userData);

  const getProfile = () => apiClient.get('auth/profile/');

  return {
    getMovies,
    getMovieById,
    login,
    register,
    getProfile,
  };
};