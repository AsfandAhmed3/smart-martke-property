<template>
  <div class="tenants-page">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Tenant CRM</h1>
        <p class="page-subtitle">Manage tenant information and relationships</p>
      </div>
      <button @click="showAddTenantModal = true" class="btn-primary">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 5v14m-7-7h14" stroke-linecap="round" />
        </svg>
        Add Tenant
      </button>
    </div>

    <!-- Search and Filters -->
    <div class="filters-section">
      <div class="search-box">
        <svg class="search-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search tenants..."
          class="search-input"
        />
      </div>
      <select v-model="filterStatus" class="filter-select">
        <option value="">All Status</option>
        <option value="active">Active</option>
        <option value="inactive">Inactive</option>
      </select>
    </div>

    <!-- Tenants Grid -->
    <div v-if="!loading" class="tenants-grid">
      <div v-for="tenant in filteredTenants" :key="tenant.id" class="tenant-card">
        <div class="tenant-header">
          <div class="tenant-avatar">
            {{ tenant.first_name.charAt(0) }}{{ tenant.last_name.charAt(0) }}
          </div>
          <div class="tenant-info">
            <h3 class="tenant-name">{{ tenant.first_name }} {{ tenant.last_name }}</h3>
            <p class="tenant-property">{{ tenant.property_details?.name || 'No Property' }} - Unit {{ tenant.unit_number || 'N/A' }}</p>
          </div>
          <span :class="['status-badge', tenant.status]">{{ tenant.status }}</span>
        </div>

        <div class="tenant-details">
          <div class="detail-row">
            <svg class="detail-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            <span>{{ tenant.email || 'No email' }}</span>
          </div>
          <div class="detail-row">
            <svg class="detail-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
            <span>{{ tenant.phone || 'No phone' }}</span>
          </div>
          <div class="detail-row">
            <svg class="detail-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span>Lease: {{ formatDate(tenant.move_in_date) }} - {{ formatDate(tenant.move_out_date) }}</span>
          </div>
          <div class="detail-row">
            <svg class="detail-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>Rent: {{ formatCurrency(tenant.monthly_rent) }}</span>
          </div>
        </div>

        <div class="tenant-actions">
          <button @click="viewTenantDetails(tenant)" class="btn-secondary">View Details</button>
          <button @click="contactTenant(tenant)" class="btn-outline">Contact</button>
          <button @click="editTenant(tenant)" class="btn-edit">Edit</button>
          <button @click="deleteTenant(tenant)" class="btn-delete">Delete</button>
        </div>
      </div>
    </div>
    <div v-else class="loading-state">
      <p>Loading tenants...</p>
    </div>

    <!-- Add Tenant Modal -->
    <AddTenantModal
      :isOpen="showAddTenantModal"
      @close="showAddTenantModal = false"
      @success="handleTenantAdded"
    />

    <!-- View Details Modal -->
    <ConfirmModal
      :isOpen="showDetailsModal"
      :title="`${selectedTenant?.first_name} ${selectedTenant?.last_name}`"
      confirmText="Close"
      cancelText=""
      @close="showDetailsModal = false"
      @confirm="showDetailsModal = false"
    >
      <div class="details-content">
        <div class="detail-item">
          <span class="detail-label">Email:</span>
          <span class="detail-value">{{ selectedTenant?.email }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Phone:</span>
          <span class="detail-value">{{ selectedTenant?.phone }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Property:</span>
          <span class="detail-value">{{ selectedTenant?.property_details?.name || 'N/A' }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Unit:</span>
          <span class="detail-value">{{ selectedTenant?.unit_number || 'N/A' }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Status:</span>
          <span class="detail-value">{{ selectedTenant?.status }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Move-in Date:</span>
          <span class="detail-value">{{ formatDate(selectedTenant?.move_in_date) }}</span>
        </div>
      </div>
    </ConfirmModal>

    <!-- Edit Tenant Modal -->
    <ConfirmModal
      :isOpen="showEditModal"
      title="Edit Tenant"
      confirmText="Save"
      @close="showEditModal = false"
      @confirm="saveTenantEdit"
    >
      <div class="edit-form">
        <div class="form-group">
          <label>Phone Number</label>
          <input v-model="editForm.phone" type="text" class="form-input" />
        </div>
        <div class="form-group">
          <label>Status</label>
          <select v-model="editForm.status" class="form-input">
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="pending">Pending</option>
          </select>
        </div>
      </div>
    </ConfirmModal>

    <!-- Delete Confirmation Modal -->
    <ConfirmModal
      :isOpen="showDeleteModal"
      title="Delete Tenant"
      confirmText="Delete"
      confirmType="danger"
      @close="showDeleteModal = false"
      @confirm="confirmDelete"
    >
      <p>Are you sure you want to delete <strong>{{ selectedTenant?.first_name }} {{ selectedTenant?.last_name }}</strong>? This action cannot be undone.</p>
    </ConfirmModal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import AddTenantModal from '../components/AddTenantModal.vue';
import ConfirmModal from '../components/ConfirmModal.vue';
import api from '../services/api';

const showAddTenantModal = ref(false);
const searchQuery = ref('');
const filterStatus = ref('');
const tenants = ref([]);
const loading = ref(true);
const showDetailsModal = ref(false);
const showEditModal = ref(false);
const showDeleteModal = ref(false);
const selectedTenant = ref(null);
const editForm = ref({ phone: '', status: '' });

const fetchTenants = async () => {
  try {
    loading.value = true;
    const params = {};
    if (filterStatus.value) params.status = filterStatus.value;
    
    const response = await api.getTenants(params);
    // Handle both array and paginated response formats
    tenants.value = Array.isArray(response.data) ? response.data : (response.data.results || []);
  } catch (error) {
    console.error('Failed to fetch tenants:', error);
    tenants.value = [];
  } finally {
    loading.value = false;
  }
};

const filteredTenants = computed(() => {
  if (!searchQuery.value) return tenants.value;
  
  const query = searchQuery.value.toLowerCase();
  return tenants.value.filter(tenant => {
    const fullName = `${tenant.first_name} ${tenant.last_name}`.toLowerCase();
    return fullName.includes(query) || 
           tenant.email?.toLowerCase().includes(query) ||
           tenant.phone?.toLowerCase().includes(query);
  });
});

const handleTenantAdded = () => {
  showAddTenantModal.value = false;
  fetchTenants();
};

const viewTenantDetails = (tenant) => {
  selectedTenant.value = tenant;
  showDetailsModal.value = true;
};

const contactTenant = (tenant) => {
  if (tenant.email) {
    window.location.href = `mailto:${tenant.email}?subject=Regarding Your Tenancy`;
  } else {
    alert(`Contact ${tenant.first_name} ${tenant.last_name} at ${tenant.phone || 'No phone available'}`);
  }
};

const editTenant = (tenant) => {
  selectedTenant.value = tenant;
  editForm.value = {
    phone: tenant.phone || '',
    status: tenant.status || 'active'
  };
  showEditModal.value = true;
};

const saveTenantEdit = async () => {
  try {
    await api.updateTenant(selectedTenant.value.id, editForm.value);
    showEditModal.value = false;
    await fetchTenants();
  } catch (error) {
    console.error('Failed to update tenant:', error);
  }
};

const deleteTenant = (tenant) => {
  selectedTenant.value = tenant;
  showDeleteModal.value = true;
};

const confirmDelete = async () => {
  try {
    await api.deleteTenant(selectedTenant.value.id);
    showDeleteModal.value = false;
    await fetchTenants();
  } catch (error) {
    console.error('Failed to delete tenant:', error);
  }
};

const formatDate = (date) => {
  if (!date) return 'N/A';
  return new Date(date).toLocaleDateString();
};

const formatCurrency = (amount) => {
  if (!amount) return '$0';
  return `$${parseFloat(amount).toLocaleString()}`;
};

onMounted(() => {
  fetchTenants();
});
</script>

<style scoped>
.tenants-page {
  max-width: 1400px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
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

.btn-primary {
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
}

.btn-primary:hover {
  background: #2563EB;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

.filters-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-box {
  flex: 1;
  position: relative;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #6B7280;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 1px solid #D1D5DB;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.search-input:focus {
  outline: none;
  border-color: #7C6FDC;
  box-shadow: 0 0 0 3px rgba(124, 111, 220, 0.1);
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 1px solid #D1D5DB;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
}

.filter-select:focus {
  outline: none;
  border-color: #7C6FDC;
}

.tenants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.tenant-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 0.75rem;
  padding: 1.5rem;
  transition: all 0.2s;
}

.tenant-card:hover {
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  transform: translateY(-2px);
}

.tenant-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #E5E7EB;
}

.tenant-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #7C6FDC 0%, #9B8FE8 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1rem;
  flex-shrink: 0;
}

.tenant-info {
  flex: 1;
}

.tenant-name {
  font-size: 1rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 0.25rem;
}

.tenant-property {
  font-size: 0.75rem;
  color: #6B7280;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: capitalize;
}

.status-badge.active {
  background: #D1FAE5;
  color: #065F46;
}

.status-badge.inactive {
  background: #FEE2E2;
  color: #991B1B;
}

.tenant-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #374151;
}

.detail-icon {
  width: 16px;
  height: 16px;
  color: #6B7280;
  flex-shrink: 0;
}

.tenant-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.btn-secondary, .btn-outline, .btn-edit, .btn-delete {
  flex: 1;
  min-width: 70px;
  padding: 0.625rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary {
  background: #F3F4F6;
  color: #374151;
  border: none;
}

.btn-secondary:hover {
  background: #E5E7EB;
}

.btn-outline {
  background: white;
  color: #3B82F6;
  border: 1px solid #3B82F6;
}

.btn-outline:hover {
  background: #EFF6FF;
}

.btn-edit {
  background: #F59E0B;
  color: white;
  border: none;
}

.btn-edit:hover {
  background: #D97706;
}

.btn-delete {
  background: #EF4444;
  color: white;
  border: none;
}

.btn-delete:hover {
  background: #DC2626;
}

.details-content {
  padding: 1rem 0;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #E5E7EB;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  font-weight: 600;
  color: #6B7280;
}

.detail-value {
  color: #1A1A1A;
}

.edit-form {
  padding: 1rem 0;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #374151;
}

.form-input {
  width: 100%;
  padding: 0.625rem;
  border: 1px solid #D1D5DB;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.form-input:focus {
  outline: none;
  border-color: #7C6FDC;
  box-shadow: 0 0 0 3px rgba(124, 111, 220, 0.1);
}
</style>

