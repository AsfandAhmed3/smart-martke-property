import { defineStore } from 'pinia';
import api from '../services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('access_token'),
    refreshToken: localStorage.getItem('refresh_token'),
    isAuthenticated: !!localStorage.getItem('access_token'),
  }),

  getters: {
    getUser: (state) => state.user,
    isLoggedIn: (state) => state.isAuthenticated,
    userRole: (state) => state.user?.role_details?.name || null,
    hasPermission: (state) => (permission) => {
      if (!state.user || !state.user.role_details) return false;
      return state.user.role_details[permission] || false;
    },
  },

  actions: {
    async login(credentials) {
      try {
        const response = await api.login(credentials);
        const { user, tokens } = response.data;

        this.user = user;
        this.accessToken = tokens.access;
        this.refreshToken = tokens.refresh;
        this.isAuthenticated = true;

        localStorage.setItem('access_token', tokens.access);
        localStorage.setItem('refresh_token', tokens.refresh);
        localStorage.setItem('user', JSON.stringify(user));

        return { success: true, user };
      } catch (error) {
        return {
          success: false,
          error: error.response?.data?.detail || 'Login failed',
        };
      }
    },

    async register(userData) {
      try {
        const response = await api.register(userData);
        const { user, tokens } = response.data;

        this.user = user;
        this.accessToken = tokens.access;
        this.refreshToken = tokens.refresh;
        this.isAuthenticated = true;

        localStorage.setItem('access_token', tokens.access);
        localStorage.setItem('refresh_token', tokens.refresh);
        localStorage.setItem('user', JSON.stringify(user));

        return { success: true, user };
      } catch (error) {
        return {
          success: false,
          error: error.response?.data || 'Registration failed',
        };
      }
    },

    async logout() {
      try {
        await api.logout();
      } catch (error) {
        console.error('Logout error:', error);
      } finally {
        this.user = null;
        this.accessToken = null;
        this.refreshToken = null;
        this.isAuthenticated = false;

        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
      }
    },

    async fetchUserProfile() {
      try {
        const response = await api.getUserProfile();
        this.user = response.data;
        localStorage.setItem('user', JSON.stringify(response.data));
        return { success: true };
      } catch (error) {
        return { success: false, error: error.response?.data };
      }
    },

    loadUserFromStorage() {
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        this.user = JSON.parse(storedUser);
      }
    },
  },
});
