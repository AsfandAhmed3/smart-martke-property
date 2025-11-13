<template>
  <div class="login-page">
    <div class="login-card">
      <!-- Building Icon -->
      <div class="icon-container">
        <svg class="building-icon" viewBox="0 0 24 24" fill="currentColor">
          <path d="M3 9h4V5H3v4zm0 5h4v-4H3v4zm5 0h4v-4H8v4zm5 0h4v-4h-4v4zM8 9h4V5H8v4zm5-4v4h4V5h-4zm5 9h4v-4h-4v4zM3 19h4v-4H3v4zm5 0h4v-4H8v4zm5 0h4v-4h-4v4zm5 0h4v-4h-4v4zM3 5h4V1H3v4zm5 0h4V1H8v4zm5 0h4V1h-4v4z"/>
        </svg>
      </div>

      <!-- Title -->
      <h1 class="title">Smart Property Manager</h1>
      <p class="subtitle">Sign in to your account</p>

      <!-- Error Message -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="jack@gmail.com"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="••••••••"
            required
          />
        </div>

        <button type="submit" class="signin-button" :disabled="loading">
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>

      <!-- Demo Credentials -->
      <p class="demo-text">Demo credentials: any email/password</p>

      <!-- Sign Up Link -->
      <div class="signup-section">
        <p class="signup-text">Don't have an account?</p>
        <router-link to="/register" class="signup-link">Sign Up</router-link>
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

const email = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');

const handleLogin = async () => {
  loading.value = true;
  error.value = '';

  const result = await authStore.login({
    email: email.value,
    password: password.value,
  });

  loading.value = false;

  if (result.success) {
    router.push('/dashboard');
  } else {
    error.value = result.error;
  }
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #7C6FDC 0%, #9B8FE8 100%);
  padding: 1rem;
}

.login-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  padding: 3rem 2.5rem;
  width: 100%;
  max-width: 420px;
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

.login-form {
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
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

.form-group input::placeholder {
  color: #9CA3AF;
}

.signin-button {
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
}

.signin-button:hover:not(:disabled) {
  background: #2563EB;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

.signin-button:active:not(:disabled) {
  transform: translateY(0);
}

.signin-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.demo-text {
  text-align: center;
  font-size: 0.75rem;
  color: #9CA3AF;
  margin-top: 1.5rem;
}

.signup-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #E5E7EB;
}

.signup-text {
  font-size: 0.875rem;
  color: #6B7280;
}

.signup-link {
  font-size: 0.875rem;
  color: #3B82F6;
  font-weight: 600;
  text-decoration: none;
}

.signup-link:hover {
  color: #2563EB;
  text-decoration: underline;
}
</style>
