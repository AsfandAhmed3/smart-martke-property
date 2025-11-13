<template>
  <div class="profile-page">
    <!-- Profile Header -->
    <div class="profile-header">
      <div class="header-background"></div>
      <div class="profile-content">
        <div class="avatar-section">
          <div class="profile-avatar">
            {{ user?.first_name?.charAt(0) }}{{ user?.last_name?.charAt(0) }}
          </div>
          <button class="change-photo-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
              <path d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Change Photo
          </button>
        </div>
        <div class="profile-info">
          <h1 class="profile-name">{{ user?.first_name }} {{ user?.last_name }}</h1>
          <p class="profile-role">{{ user?.role_details?.name || 'Portfolio Manager' }}</p>
          <div class="profile-meta">
            <div class="meta-item">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              {{ user?.email }}
            </div>
            <div class="meta-item">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              Member since {{ formatDate(user?.date_joined) }}
            </div>
          </div>
        </div>
        <button @click="showEditModal = true" class="btn-edit-profile">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          Edit Profile
        </button>
      </div>
    </div>

    <!-- Profile Body -->
    <div class="profile-body">
      <!-- Personal Information Card -->
      <div class="info-card">
        <div class="card-header">
          <h2 class="card-title">Personal Information</h2>
        </div>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">First Name</span>
            <span class="info-value">{{ user?.first_name || 'Not set' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Last Name</span>
            <span class="info-value">{{ user?.last_name || 'Not set' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Username</span>
            <span class="info-value">{{ user?.username || 'Not set' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Email Address</span>
            <span class="info-value">{{ user?.email || 'Not set' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Phone Number</span>
            <span class="info-value">{{ user?.phone || 'Not set' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Date of Birth</span>
            <span class="info-value">{{ user?.date_of_birth || 'Not set' }}</span>
          </div>
        </div>
      </div>

      <!-- Account Details Card -->
      <div class="info-card">
        <div class="card-header">
          <h2 class="card-title">Account Details</h2>
        </div>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">Role</span>
            <span class="info-value">
              <span class="role-badge">{{ user?.role_details?.name || 'User' }}</span>
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">Account Status</span>
            <span class="info-value">
              <span class="status-badge active">Active</span>
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">Member Since</span>
            <span class="info-value">{{ formatDate(user?.date_joined) }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Last Login</span>
            <span class="info-value">{{ formatDate(user?.last_login) }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Two-Factor Auth</span>
            <span class="info-value">
              <span :class="['mfa-badge', user?.mfa_enabled ? 'enabled' : 'disabled']">
                {{ user?.mfa_enabled ? 'Enabled' : 'Disabled' }}
              </span>
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">Email Verified</span>
            <span class="info-value">
              <span class="status-badge verified">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Verified
              </span>
            </span>
          </div>
        </div>
      </div>

      <!-- Permissions Card -->
      <div class="info-card" v-if="user?.role_details">
        <div class="card-header">
          <h2 class="card-title">Role Permissions</h2>
        </div>
        <div class="permissions-grid">
          <div class="permission-item" :class="{ active: user.role_details.can_create_properties }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" v-if="user.role_details.can_create_properties" />
              <path d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" v-else />
            </svg>
            <span>Create Properties</span>
          </div>
          <div class="permission-item" :class="{ active: user.role_details.can_edit_properties }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" v-if="user.role_details.can_edit_properties" />
              <path d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" v-else />
            </svg>
            <span>Edit Properties</span>
          </div>
          <div class="permission-item" :class="{ active: user.role_details.can_delete_properties }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" v-if="user.role_details.can_delete_properties" />
              <path d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" v-else />
            </svg>
            <span>Delete Properties</span>
          </div>
          <div class="permission-item" :class="{ active: user.role_details.can_manage_tenants }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" v-if="user.role_details.can_manage_tenants" />
              <path d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" v-else />
            </svg>
            <span>Manage Tenants</span>
          </div>
          <div class="permission-item" :class="{ active: user.role_details.can_manage_leases }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" v-if="user.role_details.can_manage_leases" />
              <path d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" v-else />
            </svg>
            <span>Manage Leases</span>
          </div>
          <div class="permission-item" :class="{ active: user.role_details.can_manage_financials }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" v-if="user.role_details.can_manage_financials" />
              <path d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" v-else />
            </svg>
            <span>Manage Financials</span>
          </div>
          <div class="permission-item" :class="{ active: user.role_details.can_manage_users }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" v-if="user.role_details.can_manage_users" />
              <path d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" v-else />
            </svg>
            <span>Manage Users</span>
          </div>
          <div class="permission-item" :class="{ active: user.role_details.can_view_analytics }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" v-if="user.role_details.can_view_analytics" />
              <path d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" v-else />
            </svg>
            <span>View Analytics</span>
          </div>
          <div class="permission-item" :class="{ active: user.role_details.can_export_reports }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" v-if="user.role_details.can_export_reports" />
              <path d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" v-else />
            </svg>
            <span>Export Reports</span>
          </div>
        </div>
      </div>

      <!-- Activity Stats Card -->
      <div class="info-card">
        <div class="card-header">
          <h2 class="card-title">Activity Statistics</h2>
        </div>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-icon" style="background: #DBEAFE; color: #3B82F6;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-value">23</span>
              <span class="stat-label">Properties Managed</span>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon" style="background: #D1FAE5; color: #10B981;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-value">127</span>
              <span class="stat-label">Total Tenants</span>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon" style="background: #FEF3C7; color: #F59E0B;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-value">45</span>
              <span class="stat-label">Active Leases</span>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon" style="background: #FCE7F3; color: #DB2777;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-value">$386K</span>
              <span class="stat-label">Monthly Revenue</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Profile Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="showEditModal = false">
      <div class="modal-container">
        <div class="modal-header">
          <h2 class="modal-title">Edit Profile</h2>
          <button @click="showEditModal = false" class="close-button">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <form @submit.prevent="handleUpdateProfile" class="modal-body">
          <div class="form-row">
            <div class="form-group">
              <label for="first_name">First Name</label>
              <input
                id="first_name"
                v-model="editForm.first_name"
                type="text"
                required
              />
            </div>
            <div class="form-group">
              <label for="last_name">Last Name</label>
              <input
                id="last_name"
                v-model="editForm.last_name"
                type="text"
                required
              />
            </div>
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="editForm.email"
              type="email"
              required
            />
          </div>
          <div class="form-group">
            <label for="phone">Phone</label>
            <input
              id="phone"
              v-model="editForm.phone"
              type="tel"
            />
          </div>
          <div class="form-group">
            <label for="date_of_birth">Date of Birth</label>
            <input
              id="date_of_birth"
              v-model="editForm.date_of_birth"
              type="date"
            />
          </div>
          <div class="modal-footer">
            <button type="button" @click="showEditModal = false" class="btn-cancel">Cancel</button>
            <button type="submit" class="btn-submit" :disabled="updateLoading">
              {{ updateLoading ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const user = computed(() => authStore.user);

const showEditModal = ref(false);
const updateLoading = ref(false);

const editForm = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  date_of_birth: '',
});

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
};

const handleUpdateProfile = async () => {
  updateLoading.value = true;
  try {
    // TODO: Call API to update profile
    await new Promise(resolve => setTimeout(resolve, 1000));
    showEditModal.value = false;
  } catch (error) {
    console.error('Error updating profile:', error);
  } finally {
    updateLoading.value = false;
  }
};

onMounted(() => {
  if (user.value) {
    editForm.value = {
      first_name: user.value.first_name || '',
      last_name: user.value.last_name || '',
      email: user.value.email || '',
      phone: user.value.phone || '',
      date_of_birth: user.value.date_of_birth || '',
    };
  }
});
</script>

<style scoped>
.profile-page {
  max-width: 1200px;
  margin: 0 auto;
}

.profile-header {
  position: relative;
  margin-bottom: 2rem;
}

.header-background {
  height: 200px;
  background: linear-gradient(135deg, #7C6FDC 0%, #9B8FE8 100%);
  border-radius: 1rem;
}

.profile-content {
  position: relative;
  display: flex;
  align-items: flex-end;
  gap: 2rem;
  padding: 0 2rem;
  margin-top: -80px;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.profile-avatar {
  width: 160px;
  height: 160px;
  border-radius: 1rem;
  background: white;
  border: 4px solid white;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: 600;
  color: #7C6FDC;
}

.change-photo-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: white;
  color: #374151;
  border: 1px solid #E5E7EB;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.change-photo-btn:hover {
  background: #F9FAFB;
}

.profile-info {
  flex: 1;
  padding-bottom: 1rem;
}

.profile-name {
  font-size: 2rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 0.5rem;
}

.profile-role {
  font-size: 1rem;
  color: #6B7280;
  margin-bottom: 1rem;
}

.profile-meta {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #6B7280;
}

.meta-item svg {
  color: #9CA3AF;
}

.btn-edit-profile {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #3B82F6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 1rem;
}

.btn-edit-profile:hover {
  background: #2563EB;
}

.profile-body {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.info-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 0.75rem;
  padding: 2rem;
}

.card-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #E5E7EB;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1A1A1A;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-label {
  font-size: 0.75rem;
  color: #6B7280;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-value {
  font-size: 0.875rem;
  color: #1A1A1A;
  font-weight: 500;
}

.role-badge {
  padding: 0.375rem 0.75rem;
  background: #E0E7FF;
  color: #7C6FDC;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.status-badge.active {
  background: #D1FAE5;
  color: #065F46;
}

.status-badge.verified {
  background: #DBEAFE;
  color: #1E40AF;
}

.mfa-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.mfa-badge.enabled {
  background: #D1FAE5;
  color: #065F46;
}

.mfa-badge.disabled {
  background: #FEE2E2;
  color: #991B1B;
}

.permissions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.permission-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  color: #6B7280;
  transition: all 0.2s;
}

.permission-item.active {
  background: #D1FAE5;
  border-color: #10B981;
  color: #065F46;
}

.permission-item svg {
  flex-shrink: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: #F9FAFB;
  border-radius: 0.75rem;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1A1A1A;
}

.stat-label {
  font-size: 0.75rem;
  color: #6B7280;
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
  padding: 1rem;
}

.modal-container {
  background: white;
  border-radius: 1rem;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 1.5rem 1rem 1.5rem;
  border-bottom: 1px solid #E5E7EB;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1A1A1A;
}

.close-button {
  background: none;
  border: none;
  color: #6B7280;
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.375rem;
  transition: all 0.2s;
}

.close-button:hover {
  background: #F3F4F6;
  color: #1A1A1A;
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
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #D1D5DB;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.form-group input:focus {
  outline: none;
  border-color: #7C6FDC;
  box-shadow: 0 0 0 3px rgba(124, 111, 220, 0.1);
}

.modal-footer {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  padding-top: 1.5rem;
  border-top: 1px solid #E5E7EB;
  margin-top: 1.5rem;
}

.btn-cancel {
  padding: 0.75rem 1.5rem;
  background: #F3F4F6;
  color: #374151;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: #E5E7EB;
}

.btn-submit {
  padding: 0.75rem 1.5rem;
  background: #3B82F6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-submit:hover:not(:disabled) {
  background: #2563EB;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
