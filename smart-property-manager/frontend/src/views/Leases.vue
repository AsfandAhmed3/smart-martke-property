<template>
  <div class="leases-page">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Lease Management</h1>
        <p class="page-subtitle">Track and manage property leases</p>
      </div>
      <button @click="showCreateLeaseModal = true" class="btn-primary">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 5v14m-7-7h14" stroke-linecap="round" />
        </svg>
        Create Lease
      </button>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon" style="background: #DBEAFE; color: #1E40AF;">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">Total Leases</p>
          <h3 class="stat-value">{{ stats.total_leases }}</h3>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: #D1FAE5; color: #065F46;">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">Active</p>
          <h3 class="stat-value">{{ stats.active_leases }}</h3>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: #FEF3C7; color: #92400E;">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">Expiring Soon</p>
          <h3 class="stat-value">{{ stats.expiring_soon }}</h3>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: #FEE2E2; color: #991B1B;">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">Expired</p>
          <h3 class="stat-value">{{ stats.expired_leases }}</h3>
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
          v-model="searchQuery"
          type="text"
          placeholder="Search leases..."
          class="search-input"
        />
      </div>
      <select v-model="filterStatus" class="filter-select">
        <option value="">All Status</option>
        <option value="active">Active</option>
        <option value="expiring">Expiring Soon</option>
        <option value="expired">Expired</option>
      </select>
    </div>

    <!-- Leases Table -->
    <div class="table-container">
      <table class="leases-table">
        <thead>
          <tr>
            <th>Tenant</th>
            <th>Property</th>
            <th>Unit</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Monthly Rent</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lease in filteredLeases" :key="lease.id">
            <td>
              <div class="tenant-cell">
                <div class="tenant-avatar-small">
                  {{ lease.tenant_initials }}
                </div>
                <span>{{ lease.tenant_name }}</span>
              </div>
            </td>
            <td>{{ lease.property }}</td>
            <td>{{ lease.unit_number || 'N/A' }}</td>
            <td>{{ formatDate(lease.start_date) }}</td>
            <td>{{ formatDate(lease.end_date) }}</td>
            <td class="rent-cell">${{ formatCurrency(lease.monthly_rent) }}</td>
            <td>
              <span :class="['status-badge', lease.status]">
                {{ lease.status_label }}
              </span>
            </td>
            <td>
              <div class="action-buttons">
                <button @click="viewLeaseDetails(lease)" class="action-btn" title="View">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
                <button @click="editLease(lease)" class="action-btn" title="Edit">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button @click="deleteLease(lease)" class="action-btn action-btn-danger" title="Delete">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create Lease Modal -->
    <CreateLeaseModal
      :isOpen="showCreateLeaseModal"
      @close="showCreateLeaseModal = false"
      @success="handleLeaseCreated"
    />

    <!-- View Details Modal -->
    <ConfirmModal
      :isOpen="showDetailsModal"
      :title="`Lease Details - ${selectedLease?.tenant_name}`"
      confirmText="Close"
      cancelText=""
      @close="showDetailsModal = false"
      @confirm="showDetailsModal = false"
    >
      <div class="details-content">
        <div class="detail-item">
          <span class="detail-label">Tenant:</span>
          <span class="detail-value">{{ selectedLease?.tenant_name }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Property:</span>
          <span class="detail-value">{{ selectedLease?.property }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Unit:</span>
          <span class="detail-value">{{ selectedLease?.unit_number || 'N/A' }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Start Date:</span>
          <span class="detail-value">{{ formatDate(selectedLease?.start_date) }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">End Date:</span>
          <span class="detail-value">{{ formatDate(selectedLease?.end_date) }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Monthly Rent:</span>
          <span class="detail-value">${{ formatCurrency(selectedLease?.monthly_rent) }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Security Deposit:</span>
          <span class="detail-value">${{ formatCurrency(selectedLease?.security_deposit) }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Status:</span>
          <span class="detail-value">{{ selectedLease?.status_label }}</span>
        </div>
      </div>
    </ConfirmModal>

    <!-- Edit Lease Modal -->
    <ConfirmModal
      :isOpen="showEditModal"
      title="Edit Lease"
      confirmText="Save"
      @close="showEditModal = false"
      @confirm="saveLeaseEdit"
    >
      <div class="edit-form">
        <div class="form-group">
          <label>Monthly Rent</label>
          <input v-model="editForm.monthly_rent" type="number" step="0.01" class="form-input" />
        </div>
        <div class="form-group">
          <label>Status</label>
          <select v-model="editForm.status" class="form-input">
            <option value="active">Active</option>
            <option value="expired">Expired</option>
            <option value="terminated">Terminated</option>
          </select>
        </div>
      </div>
    </ConfirmModal>

    <!-- Delete Confirmation Modal -->
    <ConfirmModal
      :isOpen="showDeleteModal"
      title="Delete Lease"
      confirmText="Delete"
      confirmType="danger"
      @close="showDeleteModal = false"
      @confirm="confirmDelete"
    >
      <p>Are you sure you want to delete the lease for <strong>{{ selectedLease?.tenant_name }}</strong>? This action cannot be undone.</p>
    </ConfirmModal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import CreateLeaseModal from '../components/CreateLeaseModal.vue';
import ConfirmModal from '../components/ConfirmModal.vue';
import api from '../services/api';

const showCreateLeaseModal = ref(false);
const searchQuery = ref('');
const filterStatus = ref('');
const leases = ref([]);
const stats = ref({
  total_leases: 0,
  active_leases: 0,
  expiring_soon: 0,
  expired_leases: 0
});
const loading = ref(true);
const showDetailsModal = ref(false);
const showEditModal = ref(false);
const showDeleteModal = ref(false);
const selectedLease = ref(null);
const editForm = ref({ monthly_rent: 0, status: '' });

const fetchLeases = async () => {
  try {
    loading.value = true;
    const params = {};
    if (filterStatus.value) params.status = filterStatus.value;
    
    const response = await api.getLeases(params);
    // Handle both array and paginated response formats
    const leasesData = Array.isArray(response.data) ? response.data : (response.data.results || []);
    
    leases.value = leasesData.map(lease => ({
      ...lease,
      tenant_name: lease.tenant_details ? `${lease.tenant_details.first_name} ${lease.tenant_details.last_name}` : 'N/A',
      tenant_initials: lease.tenant_details ? `${lease.tenant_details.first_name.charAt(0)}${lease.tenant_details.last_name.charAt(0)}` : 'N',
      property: lease.property_details?.name || 'N/A',
      status_label: lease.status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
    }));
  } catch (error) {
    console.error('Failed to fetch leases:', error);
    leases.value = [];
  } finally {
    loading.value = false;
  }
};

const fetchLeaseStats = async () => {
  try {
    const response = await api.getLeaseStatistics();
    stats.value = response.data;
  } catch (error) {
    console.error('Failed to fetch lease statistics:', error);
  }
};

const filteredLeases = computed(() => {
  if (!searchQuery.value) return leases.value;
  
  const query = searchQuery.value.toLowerCase();
  return leases.value.filter(lease => {
    return lease.tenant_name.toLowerCase().includes(query) ||
           lease.property.toLowerCase().includes(query) ||
           (lease.unit_number && lease.unit_number.toLowerCase().includes(query));
  });
});

const handleLeaseCreated = () => {
  showCreateLeaseModal.value = false;
  fetchLeases();
  fetchLeaseStats();
};

const viewLeaseDetails = (lease) => {
  selectedLease.value = lease;
  showDetailsModal.value = true;
};

const editLease = (lease) => {
  selectedLease.value = lease;
  editForm.value = {
    monthly_rent: lease.monthly_rent || 0,
    status: lease.status || 'active'
  };
  showEditModal.value = true;
};

const saveLeaseEdit = async () => {
  try {
    await api.updateLease(selectedLease.value.id, editForm.value);
    showEditModal.value = false;
    await fetchLeases();
    await fetchLeaseStats();
  } catch (error) {
    console.error('Failed to update lease:', error);
  }
};

const deleteLease = (lease) => {
  selectedLease.value = lease;
  showDeleteModal.value = true;
};

const confirmDelete = async () => {
  try {
    await api.deleteLease(selectedLease.value.id);
    showDeleteModal.value = false;
    await fetchLeases();
    await fetchLeaseStats();
  } catch (error) {
    console.error('Failed to delete lease:', error);
  }
};

const formatDate = (date) => {
  if (!date) return '';
  return new Date(date).toLocaleDateString();
};

const formatCurrency = (amount) => {
  if (!amount) return '0';
  return parseFloat(amount).toLocaleString();
};

onMounted(() => {
  fetchLeases();
  fetchLeaseStats();
});
</script>

<style scoped>
.leases-page {
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 0.75rem;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #6B7280;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.875rem;
  font-weight: 600;
  color: #1A1A1A;
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

.table-container {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 0.75rem;
  overflow: hidden;
}

.leases-table {
  width: 100%;
  border-collapse: collapse;
}

.leases-table thead {
  background: #F9FAFB;
}

.leases-table th {
  padding: 1rem;
  text-align: left;
  font-size: 0.75rem;
  font-weight: 600;
  color: #6B7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.leases-table td {
  padding: 1rem;
  font-size: 0.875rem;
  color: #374151;
  border-top: 1px solid #E5E7EB;
}

.tenant-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.tenant-avatar-small {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #7C6FDC 0%, #9B8FE8 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.75rem;
  flex-shrink: 0;
}

.rent-cell {
  font-weight: 600;
  color: #1A1A1A;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  display: inline-block;
}

.status-badge.active {
  background: #D1FAE5;
  color: #065F46;
}

.status-badge.expiring {
  background: #FEF3C7;
  color: #92400E;
}

.status-badge.expired {
  background: #FEE2E2;
  color: #991B1B;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.5rem;
  background: none;
  border: 1px solid #D1D5DB;
  border-radius: 0.375rem;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #F3F4F6;
  color: #374151;
  border-color: #9CA3AF;
}

.action-btn-danger {
  border-color: #FCA5A5;
  color: #EF4444;
}

.action-btn-danger:hover {
  background: #FEE2E2;
  color: #DC2626;
  border-color: #EF4444;
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

