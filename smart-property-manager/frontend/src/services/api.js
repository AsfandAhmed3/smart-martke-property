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
  
  // Admin - User Management
  getAdminUsers(params) {
    return apiClient.get('/auth/admin/users/', { params });
  },
  getAdminUser(id) {
    return apiClient.get(`/auth/admin/users/${id}/`);
  },
  createAdminUser(data) {
    return apiClient.post('/auth/admin/users/create/', data);
  },
  updateAdminUser(id, data) {
    return apiClient.patch(`/auth/admin/users/${id}/`, data);
  },
  deleteAdminUser(id) {
    return apiClient.delete(`/auth/admin/users/${id}/`);
  },
  toggleSuperadmin(userId) {
    return apiClient.post(`/auth/admin/users/${userId}/toggle-superadmin/`);
  },
  getAdminUserStats() {
    return apiClient.get('/auth/admin/users/stats/');
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

  // Dashboard
  getDashboardStatistics(params) {
    return apiClient.get('/dashboard/statistics/', { params });
  },

  // Tenants
  getTenants(params) {
    return apiClient.get('/tenants/', { params });
  },
  getTenant(id) {
    return apiClient.get(`/tenants/${id}/`);
  },
  createTenant(data) {
    return apiClient.post('/tenants/', data);
  },
  updateTenant(id, data) {
    return apiClient.patch(`/tenants/${id}/`, data);
  },
  deleteTenant(id) {
    return apiClient.delete(`/tenants/${id}/`);
  },
  getTenantStatistics() {
    return apiClient.get('/tenants/statistics/');
  },

  // Leases
  getLeases(params) {
    return apiClient.get('/leases/', { params });
  },
  getLease(id) {
    return apiClient.get(`/leases/${id}/`);
  },
  createLease(data) {
    return apiClient.post('/leases/', data);
  },
  updateLease(id, data) {
    return apiClient.patch(`/leases/${id}/`, data);
  },
  deleteLease(id) {
    return apiClient.delete(`/leases/${id}/`);
  },
  getLeaseStatistics() {
    return apiClient.get('/leases/statistics/');
  },

  // Maintenance
  getMaintenanceRequests(params) {
    return apiClient.get('/maintenance/', { params });
  },
  getMaintenanceRequest(id) {
    return apiClient.get(`/maintenance/${id}/`);
  },
  createMaintenanceRequest(data) {
    return apiClient.post('/maintenance/', data);
  },
  updateMaintenanceRequest(id, data) {
    return apiClient.patch(`/maintenance/${id}/`, data);
  },
  deleteMaintenanceRequest(id) {
    return apiClient.delete(`/maintenance/${id}/`);
  },
  getMaintenanceStatistics() {
    return apiClient.get('/maintenance/statistics/');
  },

  // Documents
  getFolders(params) {
    return apiClient.get('/documents/folders/', { params });
  },
  getFolder(id) {
    return apiClient.get(`/documents/folders/${id}/`);
  },
  createFolder(data) {
    return apiClient.post('/documents/folders/', data);
  },
  getDocuments(params) {
    return apiClient.get('/documents/', { params });
  },
  getDocument(id) {
    return apiClient.get(`/documents/${id}/`);
  },
  uploadDocument(formData) {
    return apiClient.post('/documents/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  deleteDocument(id) {
    return apiClient.delete(`/documents/${id}/`);
  },
  getDocumentStatistics() {
    return apiClient.get('/documents/statistics/');
  },
};
