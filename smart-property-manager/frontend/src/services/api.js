import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return apiClient(originalRequest);
      } catch (err) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(err);
      }
    }

    return Promise.reject(error);
  }
);

export default {
  // Authentication
  login(credentials) {
    return apiClient.post('/auth/login/', credentials);
  },
  register(userData) {
    return apiClient.post('/auth/register/', userData);
  },
  logout() {
    const refreshToken = localStorage.getItem('refresh_token');
    return apiClient.post('/auth/logout/', { refresh_token: refreshToken });
  },
  getUserProfile() {
    return apiClient.get('/auth/profile/');
  },
  updateUserProfile(data) {
    return apiClient.patch('/auth/profile/', data);
  },
  changePassword(data) {
    return apiClient.post('/auth/change-password/', data);
  },
  getRoles() {
    return apiClient.get('/auth/roles/');
  },
  
  // Properties
  getProperties(params) {
    return apiClient.get('/properties/', { params });
  },
  getProperty(id) {
    return apiClient.get(`/properties/${id}/`);
  },
  createProperty(data) {
    return apiClient.post('/properties/', data);
  },
  updateProperty(id, data) {
    return apiClient.patch(`/properties/${id}/`, data);
  },
  deleteProperty(id) {
    return apiClient.delete(`/properties/${id}/`);
  },
  getPropertyStatistics() {
    return apiClient.get('/properties/statistics/');
  },
  
  // Owners
  getOwners() {
    return apiClient.get('/owners/');
  },
};
