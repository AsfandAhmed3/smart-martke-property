<template>
  <div class="account-settings-page">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Account Settings</h1>
        <p class="page-subtitle">Manage your account preferences and security</p>
      </div>
    </div>

    <!-- Settings Container -->
    <div class="settings-container">
      <!-- Change Password Section -->
      <div class="settings-card">
        <div class="card-header">
          <div class="header-icon" style="background: #DBEAFE; color: #3B82F6;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <div>
            <h2 class="card-title">Change Password</h2>
            <p class="card-description">Update your password to keep your account secure</p>
          </div>
        </div>
        <form @submit.prevent="handleChangePassword" class="settings-form">
          <div class="form-group">
            <label for="current_password">Current Password</label>
            <input
              id="current_password"
              v-model="passwordForm.current_password"
              type="password"
              required
            />
          </div>
          <div class="form-group">
            <label for="new_password">New Password</label>
            <input
              id="new_password"
              v-model="passwordForm.new_password"
              type="password"
              minlength="8"
              required
            />
          </div>
          <div class="form-group">
            <label for="confirm_password">Confirm New Password</label>
            <input
              id="confirm_password"
              v-model="passwordForm.confirm_password"
              type="password"
              minlength="8"
              required
            />
          </div>
          <div v-if="passwordError" class="error-message">{{ passwordError }}</div>
          <div v-if="passwordSuccess" class="success-message">{{ passwordSuccess }}</div>
          <button type="submit" class="btn-primary" :disabled="passwordLoading">
            {{ passwordLoading ? 'Updating...' : 'Update Password' }}
          </button>
        </form>
      </div>

      <!-- Notification Preferences Section -->
      <div class="settings-card">
        <div class="card-header">
          <div class="header-icon" style="background: #FEF3C7; color: #F59E0B;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </div>
          <div>
            <h2 class="card-title">Notification Preferences</h2>
            <p class="card-description">Choose what notifications you want to receive</p>
          </div>
        </div>
        <div class="settings-form">
          <div class="notification-item">
            <div class="notification-info">
              <h4 class="notification-title">Email Notifications</h4>
              <p class="notification-desc">Receive email updates about your properties</p>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="notifications.email" @change="saveNotifications">
              <span class="toggle-slider"></span>
            </label>
          </div>
          <div class="notification-item">
            <div class="notification-info">
              <h4 class="notification-title">Lease Reminders</h4>
              <p class="notification-desc">Get notified when leases are expiring</p>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="notifications.lease_reminders" @change="saveNotifications">
              <span class="toggle-slider"></span>
            </label>
          </div>
          <div class="notification-item">
            <div class="notification-info">
              <h4 class="notification-title">Maintenance Alerts</h4>
              <p class="notification-desc">Receive alerts for new maintenance requests</p>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="notifications.maintenance_alerts" @change="saveNotifications">
              <span class="toggle-slider"></span>
            </label>
          </div>
          <div class="notification-item">
            <div class="notification-info">
              <h4 class="notification-title">Payment Notifications</h4>
              <p class="notification-desc">Get notified about rent payments and due dates</p>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="notifications.payment_notifications" @change="saveNotifications">
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <!-- Two-Factor Authentication Section -->
      <div class="settings-card">
        <div class="card-header">
          <div class="header-icon" style="background: #D1FAE5; color: #10B981;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <div>
            <h2 class="card-title">Two-Factor Authentication</h2>
            <p class="card-description">Add an extra layer of security to your account</p>
          </div>
        </div>
        <div class="settings-form">
          <div class="mfa-status">
            <span :class="['status-badge', mfaEnabled ? 'enabled' : 'disabled']">
              {{ mfaEnabled ? 'Enabled' : 'Disabled' }}
            </span>
            <button @click="toggleMFA" class="btn-secondary">
              {{ mfaEnabled ? 'Disable 2FA' : 'Enable 2FA' }}
            </button>
          </div>
          <p class="mfa-description">
            Two-factor authentication adds an extra layer of security by requiring a code from your phone in addition to your password.
          </p>
        </div>
      </div>

      <!-- API Access Keys Section -->
      <div class="settings-card">
        <div class="card-header">
          <div class="header-icon" style="background: #E0E7FF; color: #7C6FDC;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
            </svg>
          </div>
          <div>
            <h2 class="card-title">API Access Keys</h2>
            <p class="card-description">Manage API keys for third-party integrations</p>
          </div>
        </div>
        <div class="settings-form">
          <div class="api-key-list">
            <div v-for="key in apiKeys" :key="key.id" class="api-key-item">
              <div class="api-key-info">
                <h4 class="api-key-name">{{ key.name }}</h4>
                <code class="api-key-value">{{ key.masked_key }}</code>
                <p class="api-key-date">Created: {{ key.created }}</p>
              </div>
              <button @click="deleteApiKey(key.id)" class="btn-danger-small">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
          <button @click="generateApiKey" class="btn-outline">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 4v16m8-8H4" />
            </svg>
            Generate New Key
          </button>
        </div>
      </div>

      <!-- Billing Information Section -->
      <div class="settings-card">
        <div class="card-header">
          <div class="header-icon" style="background: #FEE2E2; color: #EF4444;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
            </svg>
          </div>
          <div>
            <h2 class="card-title">Billing Information</h2>
            <p class="card-description">Manage your subscription and payment methods</p>
          </div>
        </div>
        <div class="settings-form">
          <div class="billing-info">
            <div class="billing-item">
              <span class="billing-label">Current Plan</span>
              <span class="billing-value">Professional</span>
            </div>
            <div class="billing-item">
              <span class="billing-label">Billing Cycle</span>
              <span class="billing-value">Monthly</span>
            </div>
            <div class="billing-item">
              <span class="billing-label">Next Billing Date</span>
              <span class="billing-value">December 9, 2025</span>
            </div>
            <div class="billing-item">
              <span class="billing-label">Amount</span>
              <span class="billing-value">$99.00/month</span>
            </div>
          </div>
          <button class="btn-outline">Update Payment Method</button>
        </div>
      </div>

      <!-- Data Export Section -->
      <div class="settings-card">
        <div class="card-header">
          <div class="header-icon" style="background: #FCE7F3; color: #DB2777;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
          </div>
          <div>
            <h2 class="card-title">Data Export</h2>
            <p class="card-description">Download your data in various formats</p>
          </div>
        </div>
        <div class="settings-form">
          <p class="export-description">
            Export all your property, tenant, and financial data. You can choose from JSON, CSV, or Excel formats.
          </p>
          <div class="export-buttons">
            <button @click="exportData('json')" class="btn-outline">Export as JSON</button>
            <button @click="exportData('csv')" class="btn-outline">Export as CSV</button>
            <button @click="exportData('excel')" class="btn-outline">Export as Excel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();

// Password form
const passwordForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: '',
});
const passwordLoading = ref(false);
const passwordError = ref('');
const passwordSuccess = ref('');

// Notifications
const notifications = ref({
  email: true,
  lease_reminders: true,
  maintenance_alerts: true,
  payment_notifications: false,
});

// MFA
const mfaEnabled = ref(false);

// API Keys
const apiKeys = ref([
  {
    id: 1,
    name: 'Production API Key',
    masked_key: 'pk_live_••••••••••••1234',
    created: 'Oct 15, 2025',
  },
  {
    id: 2,
    name: 'Development API Key',
    masked_key: 'pk_test_••••••••••••5678',
    created: 'Nov 1, 2025',
  },
]);

const handleChangePassword = async () => {
  passwordError.value = '';
  passwordSuccess.value = '';

  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    passwordError.value = 'New passwords do not match';
    return;
  }

  passwordLoading.value = true;

  try {
    // TODO: Call API to change password
    await new Promise(resolve => setTimeout(resolve, 1000));
    passwordSuccess.value = 'Password updated successfully!';
    passwordForm.value = {
      current_password: '',
      new_password: '',
      confirm_password: '',
    };
  } catch (error) {
    passwordError.value = 'Failed to update password. Please try again.';
  } finally {
    passwordLoading.value = false;
  }
};

const saveNotifications = () => {
  // TODO: Save notification preferences to API
  console.log('Notification preferences saved:', notifications.value);
};

const toggleMFA = () => {
  mfaEnabled.value = !mfaEnabled.value;
  // TODO: Implement MFA setup/disable logic
  console.log('MFA toggled:', mfaEnabled.value);
};

const generateApiKey = () => {
  // TODO: Generate new API key
  const newKey = {
    id: apiKeys.value.length + 1,
    name: `API Key ${apiKeys.value.length + 1}`,
    masked_key: `pk_live_••••••••••••${Math.random().toString(36).substr(2, 4)}`,
    created: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
  };
  apiKeys.value.push(newKey);
};

const deleteApiKey = (id) => {
  apiKeys.value = apiKeys.value.filter(key => key.id !== id);
  // TODO: Delete API key from backend
};

const exportData = (format) => {
  console.log(`Exporting data as ${format}`);
  // TODO: Implement data export
};
</script>

<style scoped>
.account-settings-page {
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

.page-title {
  font-size: 1.875rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  color: #6B7280;
  font-size: 0.875rem;
}

.settings-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.settings-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 0.75rem;
  padding: 2rem;
}

.card-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #E5E7EB;
}

.header-icon {
  width: 48px;
  height: 48px;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 0.25rem;
}

.card-description {
  font-size: 0.875rem;
  color: #6B7280;
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.form-group input {
  padding: 0.75rem 1rem;
  border: 1px solid #D1D5DB;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.form-group input:focus {
  outline: none;
  border-color: #7C6FDC;
  box-shadow: 0 0 0 3px rgba(124, 111, 220, 0.1);
}

.error-message {
  background: #FEE2E2;
  border: 1px solid #F87171;
  color: #DC2626;
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.success-message {
  background: #D1FAE5;
  border: 1px solid #34D399;
  color: #065F46;
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background: #3B82F6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #2563EB;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.notification-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #F9FAFB;
  border-radius: 0.5rem;
}

.notification-info {
  flex: 1;
}

.notification-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 0.25rem;
}

.notification-desc {
  font-size: 0.75rem;
  color: #6B7280;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 24px;
  flex-shrink: 0;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #D1D5DB;
  transition: 0.3s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: #10B981;
}

input:checked + .toggle-slider:before {
  transform: translateX(24px);
}

.mfa-status {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: #F9FAFB;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.status-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-badge.enabled {
  background: #D1FAE5;
  color: #065F46;
}

.status-badge.disabled {
  background: #FEE2E2;
  color: #991B1B;
}

.btn-secondary {
  padding: 0.5rem 1rem;
  background: #F3F4F6;
  color: #374151;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #E5E7EB;
}

.mfa-description {
  font-size: 0.875rem;
  color: #6B7280;
  line-height: 1.5;
}

.api-key-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

.api-key-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 0.5rem;
}

.api-key-info {
  flex: 1;
}

.api-key-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 0.5rem;
}

.api-key-value {
  display: block;
  font-family: 'Courier New', monospace;
  font-size: 0.75rem;
  color: #6B7280;
  background: white;
  padding: 0.5rem;
  border-radius: 0.25rem;
  margin-bottom: 0.5rem;
}

.api-key-date {
  font-size: 0.75rem;
  color: #9CA3AF;
}

.btn-danger-small {
  padding: 0.5rem;
  background: #FEE2E2;
  color: #DC2626;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-danger-small:hover {
  background: #FEF2F2;
}

.btn-outline {
  padding: 0.75rem 1.5rem;
  background: white;
  color: #7C6FDC;
  border: 1px solid #7C6FDC;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-outline:hover {
  background: #F5F3FF;
}

.billing-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  padding: 1.5rem;
  background: #F9FAFB;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.billing-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.billing-label {
  font-size: 0.75rem;
  color: #6B7280;
  font-weight: 500;
}

.billing-value {
  font-size: 0.875rem;
  color: #1A1A1A;
  font-weight: 600;
}

.export-description {
  font-size: 0.875rem;
  color: #6B7280;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.export-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}
</style>
