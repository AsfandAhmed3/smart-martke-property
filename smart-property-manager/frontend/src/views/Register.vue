<template>
  <div class="register-page">
    <div class="register-card">
      <!-- Building Icon -->
      <div class="icon-container">
        <svg class="building-icon" viewBox="0 0 24 24" fill="currentColor">
          <path d="M3 9h4V5H3v4zm0 5h4v-4H3v4zm5 0h4v-4H8v4zm5 0h4v-4h-4v4zM8 9h4V5H8v4zm5-4v4h4V5h-4zm5 9h4v-4h-4v4zM3 19h4v-4H3v4zm5 0h4v-4H8v4zm5 0h4v-4h-4v4zm5 0h4v-4h-4v4zM3 5h4V1H3v4zm5 0h4V1H8v4zm5 0h4V1h-4v4z"/>
        </svg>
      </div>

      <!-- Title -->
      <h1 class="title">Create Your Account</h1>
      <p class="subtitle">Sign up to get started</p>

      <!-- Error Message -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <!-- Registration Form -->
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-row">
          <div class="form-group">
            <label for="first_name">First Name</label>
            <input
              id="first_name"
              v-model="formData.first_name"
              type="text"
              required
            />
          </div>

          <div class="form-group">
            <label for="last_name">Last Name</label>
            <input
              id="last_name"
              v-model="formData.last_name"
              type="text"
              required
            />
          </div>
        </div>

        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="formData.username"
            type="text"
            required
          />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            required
            minlength="8"
          />
        </div>

        <div class="form-group">
          <label for="password_confirm">Confirm Password</label>
          <input
            id="password_confirm"
            v-model="formData.password_confirm"
            type="password"
            required
            minlength="8"
          />
        </div>

        <button type="submit" class="signup-button" :disabled="loading">
          {{ loading ? 'Creating Account...' : 'Sign Up' }}
        </button>
      </form>

      <!-- Login Link -->
      <div class="login-section">
        <p class="login-text">Already have an account?</p>
        <router-link to="/login" class="login-link">Sign In</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const formData = ref({
  first_name: '',
  last_name: '',
  username: '',
  email: '',
  password: '',
  password_confirm: '',
});

const loading = ref(false);
const error = ref('');

const handleRegister = async () => {
  // Validate passwords match
  if (formData.value.password !== formData.value.password_confirm) {
    error.value = 'Passwords do not match';
    return;
  }

  loading.value = true;
  error.value = '';

  const result = await authStore.register(formData.value);

  loading.value = false;

  if (result.success) {
    router.push('/dashboard');
  } else {
    error.value = result.error?.email?.[0] || 
                  result.error?.username?.[0] || 
                  result.error?.password?.[0] ||
                  'Registration failed. Please try again.';
  }
};
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #7C6FDC 0%, #9B8FE8 100%);
  padding: 2rem 1rem;
}

.register-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  padding: 2.5rem 2.5rem;
  width: 100%;
  max-width: 520px;
}

.icon-container {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.building-icon {
  width: 48px;
  height: 48px;
  color: #3B82F6;
}

.title {
  text-align: center;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 0.5rem;
}

.subtitle {
  text-align: center;
  font-size: 0.875rem;
  color: #6B7280;
  margin-bottom: 2rem;
}

.error-message {
  background: #FEE2E2;
  border: 1px solid #F87171;
  color: #DC2626;
  padding: 0.75rem;
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
}

.register-form {
  margin-bottom: 1rem;
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
  padding: 0.75rem 1rem;
  border: 1px solid #D1D5DB;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: all 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #7C6FDC;
  box-shadow: 0 0 0 3px rgba(124, 111, 220, 0.1);
}

.signup-button {
  width: 100%;
  padding: 0.875rem;
  background: #3B82F6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 0.5rem;
}

.signup-button:hover:not(:disabled) {
  background: #2563EB;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

.signup-button:active:not(:disabled) {
  transform: translateY(0);
}

.signup-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #E5E7EB;
}

.login-text {
  font-size: 0.875rem;
  color: #6B7280;
}

.login-link {
  font-size: 0.875rem;
  color: #3B82F6;
  font-weight: 600;
  text-decoration: none;
}

.login-link:hover {
  color: #2563EB;
  text-decoration: underline;
}
</style>
