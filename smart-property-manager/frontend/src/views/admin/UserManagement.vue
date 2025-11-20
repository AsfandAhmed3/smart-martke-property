<template>
  <div class="user-management">
    <div class="page-header">
      <h1 class="page-title">User Management</h1>
      <button @click="showCreateModal = true" class="btn-primary">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" style="width: 20px; height: 20px;">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Add User
      </button>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon" style="background: #E3F2FD;">
          <svg style="color: #1976D2;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
        </div>
        <div class="stat-info">
          <p class="stat-label">Total Users</p>
          <h3 class="stat-value">{{ stats.total_users }}</h3>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: #E8F5E9;">
          <svg style="color: #388E3C;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div class="stat-info">
          <p class="stat-label">Active Users</p>
          <h3 class="stat-value">{{ stats.active_users }}</h3>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: #FFF3E0;">
          <svg style="color: #F57C00;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <div class="stat-info">
          <p class="stat-label">Superadmins</p>
          <h3 class="stat-value">{{ stats.superadmins }}</h3>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: #FCE4EC;">
          <svg style="color: #C2185B;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
          </svg>
        </div>
        <div class="stat-info">
          <p class="stat-label">Inactive Users</p>
          <h3 class="stat-value">{{ stats.inactive_users }}</h3>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-section">
      <div class="search-box">
        <svg class="search-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input 
          v-model="filters.search" 
          @input="fetchUsers"
          type="text" 
          placeholder="Search by name or email..." 
          class="search-input"
        />
      </div>

      <select v-model="filters.role" @change="fetchUsers" class="filter-select">
        <option value="">All Roles</option>
        <option v-for="role in roles" :key="role?.id" :value="role?.id">{{ role?.name }}</option>
      </select>

      <select v-model="filters.is_active" @change="fetchUsers" class="filter-select">
        <option value="">All Status</option>
        <option value="true">Active</option>
        <option value="false">Inactive</option>
      </select>

      <select v-model="filters.is_superadmin" @change="fetchUsers" class="filter-select">
        <option value="">All Users</option>
        <option value="true">Superadmins Only</option>
        <option value="false">Regular Users</option>
      </select>
    </div>

    <!-- Users Table -->
    <div class="table-container">
      <table class="users-table">
        <thead>
          <tr>
            <th>User</th>
            <th>Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Type</th>
            <th>Joined</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="user in users" :key="user?.id || Math.random()">
            <tr v-if="user">
              <td>
                <div class="user-info">
                  <div class="user-avatar-small">{{ getUserInitials(user) }}</div>
                  <span class="user-name-cell">{{ user.full_name || user.username }}</span>
                </div>
              </td>
              <td>{{ user.email }}</td>
              <td>
                <span class="role-badge" :style="getRoleBadgeStyle(user.role_details?.name)">
                  {{ user.role_details?.name || 'No Role' }}
                </span>
              </td>
              <td>
                <span class="status-badge" :class="user.is_active ? 'status-active' : 'status-inactive'">
                  {{ user.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td>
                <span v-if="user.is_superadmin" class="admin-badge">Superadmin</span>
                <span v-else class="regular-badge">User</span>
              </td>
              <td>{{ formatDate(user.date_joined) }}</td>
              <td>
                <div class="action-buttons">
                  <button @click="editUser(user)" class="btn-icon" title="Edit">
                    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button @click="toggleSuperadmin(user)" class="btn-icon" :title="user.is_superadmin ? 'Revoke Superadmin' : 'Make Superadmin'">
                    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                  </button>
                  <button @click="deleteUser(user)" class="btn-icon btn-danger" title="Delete">
                    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
      <div v-if="users.length === 0" class="empty-state">
        <p>No users found. Please check your connection or try logging in again.</p>
      </div>
    </div>

    <!-- Create User Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
      <div class="modal">
        <div class="modal-header">
          <h2>Add New User</h2>
          <button @click="showCreateModal = false" class="btn-close">&times;</button>
        </div>
        <form @submit.prevent="createUser" class="modal-body">
          <div class="form-row">
            <div class="form-group">
              <label>First Name *</label>
              <input v-model="newUser.first_name" type="text" required />
            </div>
            <div class="form-group">
              <label>Last Name *</label>
              <input v-model="newUser.last_name" type="text" required />
            </div>
          </div>
          <div class="form-group">
            <label>Email *</label>
            <input v-model="newUser.email" type="email" required />
          </div>
          <div class="form-group">
            <label>Username *</label>
            <input v-model="newUser.username" type="text" required />
          </div>
          <div class="form-group">
            <label>Password *</label>
            <input v-model="newUser.password" type="password" required minlength="8" />
          </div>
          <div class="form-group">
            <label>Phone</label>
            <input v-model="newUser.phone" type="tel" />
          </div>
          <div class="form-group">
            <label>Role</label>
            <select v-model="newUser.role">
              <option :value="null">No Role</option>
              <option v-for="role in roles" :key="role?.id" :value="role?.id">{{ role?.name }}</option>
            </select>
          </div>
          <div class="form-group checkbox-group">
            <label>
              <input v-model="newUser.is_active" type="checkbox" />
              Active User
            </label>
          </div>
          <div class="form-group checkbox-group">
            <label>
              <input v-model="newUser.is_superadmin" type="checkbox" />
              Superadmin Privileges
            </label>
          </div>
          <div class="modal-footer">
            <button type="button" @click="showCreateModal = false" class="btn-secondary">Cancel</button>
            <button type="submit" class="btn-primary">Create User</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit User Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="showEditModal = false">
      <div class="modal">
        <div class="modal-header">
          <h2>Edit User</h2>
          <button @click="showEditModal = false" class="btn-close">&times;</button>
        </div>
        <form @submit.prevent="updateUser" class="modal-body">
          <div class="form-row">
            <div class="form-group">
              <label>First Name</label>
              <input v-model="editingUser.first_name" type="text" />
            </div>
            <div class="form-group">
              <label>Last Name</label>
              <input v-model="editingUser.last_name" type="text" />
            </div>
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="editingUser.email" type="email" />
          </div>
          <div class="form-group">
            <label>Username</label>
            <input v-model="editingUser.username" type="text" />
          </div>
          <div class="form-group">
            <label>Phone</label>
            <input v-model="editingUser.phone" type="tel" />
          </div>
          <div class="form-group">
            <label>Role</label>
            <select v-model="editingUser.role">
              <option :value="null">No Role</option>
              <option v-for="role in roles" :key="role?.id" :value="role?.id">{{ role?.name }}</option>
            </select>
          </div>
          <div class="form-group checkbox-group">
            <label>
              <input v-model="editingUser.is_active" type="checkbox" />
              Active User
            </label>
          </div>
          <div class="form-group checkbox-group">
            <label>
              <input v-model="editingUser.is_superadmin" type="checkbox" />
              Superadmin Privileges
            </label>
          </div>
          <div class="modal-footer">
            <button type="button" @click="showEditModal = false" class="btn-secondary">Cancel</button>
            <button type="submit" class="btn-primary">Update User</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../../services/api';

const users = ref([]);
const roles = ref([]);
const stats = ref({
  total_users: 0,
  active_users: 0,
  inactive_users: 0,
  superadmins: 0
});

const filters = ref({
  search: '',
  role: '',
  is_active: '',
  is_superadmin: ''
});

const showCreateModal = ref(false);
const showEditModal = ref(false);
const newUser = ref({
  first_name: '',
  last_name: '',
  email: '',
  username: '',
  password: '',
  phone: '',
  role: null,
  is_active: true,
  is_superadmin: false
});
const editingUser = ref(null);

const fetchUsers = async () => {
  try {
    const params = {};
    if (filters.value.search) params.search = filters.value.search;
    if (filters.value.role) params.role = filters.value.role;
    if (filters.value.is_active) params.is_active = filters.value.is_active;
    if (filters.value.is_superadmin) params.is_superadmin = filters.value.is_superadmin;

    const response = await api.getAdminUsers(params);
    users.value = response.data || [];
  } catch (error) {
    console.error('Failed to fetch users:', error);
    users.value = [];
    if (error.response?.status === 401) {
      alert('Session expired. Please login again.');
      window.location.href = '/login';
    }
  }
};

const fetchRoles = async () => {
  try {
    const response = await api.getRoles();
    roles.value = response.data || [];
  } catch (error) {
    console.error('Failed to fetch roles:', error);
    roles.value = [];
  }
};

const fetchStats = async () => {
  try {
    const response = await api.getAdminUserStats();
    stats.value = response.data || {
      total_users: 0,
      active_users: 0,
      inactive_users: 0,
      superadmins: 0
    };
  } catch (error) {
    console.error('Failed to fetch stats:', error);
  }
};

const createUser = async () => {
  try {
    await api.createAdminUser(newUser.value);
    alert('User created successfully');
    showCreateModal.value = false;
    resetNewUser();
    fetchUsers();
    fetchStats();
  } catch (error) {
    console.error('Failed to create user:', error);
    alert(error.response?.data?.email?.[0] || 'Failed to create user');
  }
};

const editUser = (user) => {
  editingUser.value = { ...user };
  showEditModal.value = true;
};

const updateUser = async () => {
  try {
    await api.updateAdminUser(editingUser.value.id, editingUser.value);
    alert('User updated successfully');
    showEditModal.value = false;
    fetchUsers();
  } catch (error) {
    console.error('Failed to update user:', error);
    alert('Failed to update user');
  }
};

const toggleSuperadmin = async (user) => {
  const action = user.is_superadmin ? 'revoke' : 'grant';
  if (!confirm(`Are you sure you want to ${action} superadmin privileges for ${user.full_name}?`)) {
    return;
  }

  try {
    await api.toggleSuperadmin(user.id);
    alert(`Superadmin privileges ${action === 'grant' ? 'granted' : 'revoked'} successfully`);
    fetchUsers();
    fetchStats();
  } catch (error) {
    console.error('Failed to toggle superadmin:', error);
    alert('Failed to update superadmin status');
  }
};

const deleteUser = async (user) => {
  if (!confirm(`Are you sure you want to delete user ${user.full_name}? This action cannot be undone.`)) {
    return;
  }

  try {
    await api.deleteAdminUser(user.id);
    alert('User deleted successfully');
    fetchUsers();
    fetchStats();
  } catch (error) {
    console.error('Failed to delete user:', error);
    alert('Failed to delete user');
  }
};

const resetNewUser = () => {
  newUser.value = {
    first_name: '',
    last_name: '',
    email: '',
    username: '',
    password: '',
    phone: '',
    role: null,
    is_active: true,
    is_superadmin: false
  };
};

const getUserInitials = (user) => {
  const firstName = user.first_name || '';
  const lastName = user.last_name || '';
  if (firstName && lastName) {
    return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
  }
  if (firstName) return firstName.charAt(0).toUpperCase();
  if (user.email) return user.email.charAt(0).toUpperCase();
  return 'U';
};

const getRoleBadgeStyle = (roleName) => {
  const styles = {
    'admin': { background: '#FEE2E2', color: '#991B1B' },
    'portfolio_manager': { background: '#DBEAFE', color: '#1E40AF' },
    'view_only': { background: '#E5E7EB', color: '#374151' }
  };
  return styles[roleName] || { background: '#F3F4F6', color: '#6B7280' };
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
};

onMounted(() => {
  fetchUsers();
  fetchRoles();
  fetchStats();
});
</script>

<style scoped>
.user-management {
  padding: 2rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 1.875rem;
  font-weight: 600;
  color: #1F2937;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 1rem;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon svg {
  width: 24px;
  height: 24px;
}

.stat-label {
  font-size: 0.875rem;
  color: #6B7280;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.875rem;
  font-weight: 600;
  color: #1F2937;
}

.filters-section {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  min-width: 250px;
  position: relative;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #9CA3AF;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 1px solid #D1D5DB;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 1px solid #D1D5DB;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  background: white;
  cursor: pointer;
}

.table-container {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table thead {
  background: #F9FAFB;
}

.users-table th {
  padding: 1rem;
  text-align: left;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  color: #6B7280;
  border-bottom: 1px solid #E5E7EB;
}

.users-table td {
  padding: 1rem;
  border-bottom: 1px solid #E5E7EB;
  font-size: 0.875rem;
  color: #1F2937;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar-small {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 600;
}

.user-name-cell {
  font-weight: 500;
}

.role-badge,
.status-badge,
.admin-badge,
.regular-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-active {
  background: #D1FAE5;
  color: #065F46;
}

.status-inactive {
  background: #FEE2E2;
  color: #991B1B;
}

.admin-badge {
  background: #FEF3C7;
  color: #92400E;
}

.regular-badge {
  background: #E5E7EB;
  color: #374151;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-icon {
  width: 32px;
  height: 32px;
  border: none;
  background: #F3F4F6;
  border-radius: 0.375rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-icon svg {
  width: 16px;
  height: 16px;
  color: #6B7280;
}

.btn-icon:hover {
  background: #E5E7EB;
}

.btn-icon.btn-danger:hover {
  background: #FEE2E2;
}

.btn-icon.btn-danger:hover svg {
  color: #DC2626;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: transform 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
}

.btn-secondary {
  background: #F3F4F6;
  color: #374151;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-secondary:hover {
  background: #E5E7EB;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 0.75rem;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #E5E7EB;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1F2937;
}

.btn-close {
  width: 32px;
  height: 32px;
  border: none;
  background: #F3F4F6;
  border-radius: 0.375rem;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6B7280;
}

.btn-close:hover {
  background: #E5E7EB;
}

.modal-body {
  padding: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #D1D5DB;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.checkbox-group input[type="checkbox"] {
  width: auto;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #E5E7EB;
}

.nav-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.2);
  margin: 1rem 0;
}
</style>
