import { defineStore } from 'pinia';
import { useApi } from '../composables/useApi';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: null,
    user: null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.accessToken,
  },
  actions: {
    async login(credentials) {
      const { login } = useApi();
      try {
        const response = await login(credentials);
        this.accessToken = response.data.access;
        console.log('Login successful, fetching profile...');
        await this.fetchProfile();
        return true;
      } catch (error) {
        console.error('Login failed:', error);
        this.logout(); // Clear any partial state
        return false;
      }
    },
    async fetchProfile() {
      const { getProfile } = useApi();
      try {
        const response = await getProfile();
        this.user = response.data;
        console.log('Profile fetched:', this.user);
      } catch (error) {
        console.error('Failed to fetch profile:', error);
        this.logout(); // Log out if profile fetch fails
      }
    },
    async register(userData) {
      const { register } = useApi();
      try {
        await register(userData);
        console.log('Registration successful.');
        return true;
      } catch (error) {
        console.error('Registration failed:', error);
        return false;
      }
    },
    logout() {
      this.accessToken = null;
      this.user = null;
      console.log('Logged out.');
    },
  },
});