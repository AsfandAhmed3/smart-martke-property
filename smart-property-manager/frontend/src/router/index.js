import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Dashboard from '../views/Dashboard.vue';
import DashboardLayout from '../layouts/DashboardLayout.vue';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresGuest: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresGuest: true },
  },
  {
    path: '/',
    component: DashboardLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/dashboard',
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard,
      },
      {
        path: 'properties',
        name: 'Properties',
        component: () => import('../views/Properties.vue'),
      },
      {
        path: 'tenants',
        name: 'Tenants',
        component: () => import('../views/Tenants.vue'),
      },
      {
        path: 'leases',
        name: 'Leases',
        component: () => import('../views/Leases.vue'),
      },
      {
        path: 'analytics',
        name: 'Analytics',
        component: () => import('../views/Analytics.vue'),
      },
      {
        path: 'maintenance',
        name: 'Maintenance',
        component: () => import('../views/Maintenance.vue'),
      },
      {
        path: 'ai-insights',
        name: 'AIInsights',
        component: () => import('../views/AIInsights.vue'),
      },
      {
        path: 'documents',
        name: 'Documents',
        component: () => import('../views/Documents.vue'),
      },
      {
        path: 'profile',
        name: 'ViewProfile',
        component: () => import('../views/ViewProfile.vue'),
      },
      {
        path: 'account-settings',
        name: 'AccountSettings',
        component: () => import('../views/AccountSettings.vue'),
      },
      {
        path: 'admin/users',
        name: 'UserManagement',
        component: () => import('../views/admin/UserManagement.vue'),
        meta: { requiresSuperAdmin: true },
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = authStore.isAuthenticated;

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else if (to.meta.requiresGuest && isAuthenticated) {
    next('/dashboard');
  } else if (to.meta.requiresSuperAdmin) {
    // Check if user is superadmin
    if (!authStore.user || (!authStore.user.is_superadmin && !authStore.user.is_superuser)) {
      alert('Access denied. Superadmin privileges required.');
      next('/dashboard');
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
