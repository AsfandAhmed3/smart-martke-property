<template>
  <div class="maintenance-page">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Maintenance Requests</h1>
        <p class="page-subtitle">Track and manage maintenance tickets</p>
      </div>
      <button class="btn-primary" @click="showModal = true">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 5v14m-7-7h14" stroke-linecap="round" />
        </svg>
        New Request
      </button>
    </div>

    <!-- Stats -->
    <div class="stats-grid">
      <div class="stat-card">
        <h3 class="stat-value">{{ stats.open }}</h3>
        <p class="stat-label">Open Tickets</p>
      </div>
      <div class="stat-card">
        <h3 class="stat-value">{{ stats.in_progress }}</h3>
        <p class="stat-label">In Progress</p>
      </div>
      <div class="stat-card">
        <h3 class="stat-value">{{ stats.completed }}</h3>
        <p class="stat-label">Completed</p>
      </div>
      <div class="stat-card">
        <h3 class="stat-value">{{ stats.avg_resolution_time }}</h3>
        <p class="stat-label">Avg Resolution Time</p>
      </div>
    </div>

    <!-- Tickets List -->
    <div v-if="!loading && tickets.length > 0" class="tickets-container">
      <div v-for="ticket in tickets" :key="ticket.id" class="ticket-card">
        <div class="ticket-header">
          <span :class="['priority-badge', ticket.priority]">{{ ticket.priority }}</span>
          <span :class="['status-badge', ticket.status]">{{ ticket.status }}</span>
        </div>
        <h3 class="ticket-title">{{ ticket.title }}</h3>
        <p class="ticket-description">{{ ticket.description }}</p>
        <div class="ticket-footer">
          <span class="ticket-property">{{ ticket.property_details?.name || 'N/A' }} #{{ ticket.unit_number || 'N/A' }}</span>
          <span class="ticket-date">{{ formatTimestamp(ticket.reported_date) }}</span>
        </div>
        <div class="ticket-actions">
          <button @click="viewTicketDetails(ticket)" class="btn-view-sm">View</button>
          <button @click="editTicket(ticket)" class="btn-edit-sm">Edit</button>
          <button @click="deleteTicket(ticket)" class="btn-delete-sm">Delete</button>
        </div>
      </div>
    </div>
    <div v-else-if="loading" class="loading-state">
      <p>Loading maintenance requests...</p>
    </div>
    <div v-else class="empty-state">
      <p>No maintenance requests found</p>
    </div>

    <!-- Add Maintenance Modal -->
    <AddMaintenanceModal 
      :isOpen="showModal" 
      @close="showModal = false"
      @success="handleMaintenanceCreated"
    />

    <!-- View Details Modal -->
    <ConfirmModal
      :isOpen="showDetailsModal"
      :title="selectedTicket?.title"
      confirmText="Close"
      cancelText=""
      @close="showDetailsModal = false"
      @confirm="showDetailsModal = false"
    >
      <div class="details-content">
        <div class="detail-item">
          <span class="detail-label">Description:</span>
          <span class="detail-value">{{ selectedTicket?.description }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Category:</span>
          <span class="detail-value">{{ selectedTicket?.category }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Priority:</span>
          <span class="detail-value">{{ selectedTicket?.priority }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Status:</span>
          <span class="detail-value">{{ selectedTicket?.status }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Property:</span>
          <span class="detail-value">{{ selectedTicket?.property_details?.name || 'N/A' }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Unit:</span>
          <span class="detail-value">{{ selectedTicket?.unit_number || 'N/A' }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Reported:</span>
          <span class="detail-value">{{ formatTimestamp(selectedTicket?.reported_date) }}</span>
        </div>
      </div>
    </ConfirmModal>

    <!-- Edit Ticket Modal -->
    <ConfirmModal
      :isOpen="showEditModal"
      title="Edit Maintenance Request"
      confirmText="Save"
      @close="showEditModal = false"
      @confirm="saveTicketEdit"
    >
      <div class="edit-form">
        <div class="form-group">
          <label>Status</label>
          <select v-model="editForm.status" class="form-input">
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>
        <div class="form-group">
          <label>Priority</label>
          <select v-model="editForm.priority" class="form-input">
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>
        </div>
      </div>
    </ConfirmModal>

    <!-- Delete Confirmation Modal -->
    <ConfirmModal
      :isOpen="showDeleteModal"
      title="Delete Maintenance Request"
      confirmText="Delete"
      confirmType="danger"
      @close="showDeleteModal = false"
      @confirm="confirmDelete"
    >
      <p>Are you sure you want to delete <strong>{{ selectedTicket?.title }}</strong>? This action cannot be undone.</p>
    </ConfirmModal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';
import AddMaintenanceModal from '../components/AddMaintenanceModal.vue';
import ConfirmModal from '../components/ConfirmModal.vue';

const tickets = ref([]);
const stats = ref({
  open: 0,
  in_progress: 0,
  completed: 0,
  avg_resolution_time: '0 days'
});
const loading = ref(true);
const showModal = ref(false);
const showDetailsModal = ref(false);
const showEditModal = ref(false);
const showDeleteModal = ref(false);
const selectedTicket = ref(null);
const editForm = ref({ status: '', priority: '' });

const fetchMaintenanceRequests = async () => {
  try {
    loading.value = true;
    const response = await api.getMaintenanceRequests({ limit: 10 });
    // Handle both array and paginated response formats
    tickets.value = Array.isArray(response.data) ? response.data : (response.data.results || []);
  } catch (error) {
    console.error('Failed to fetch maintenance requests:', error);
    if (error.response?.status === 401) {
      console.error('Authentication required. Please log in again.');
    }
    tickets.value = [];
  } finally {
    loading.value = false;
  }
};

const fetchMaintenanceStats = async () => {
  try {
    const response = await api.getMaintenanceStatistics();
    stats.value = {
      open: response.data.open || 0,
      in_progress: response.data.in_progress || 0,
      completed: response.data.completed || 0,
      avg_resolution_time: response.data.average_days_to_complete 
        ? `${response.data.average_days_to_complete} days` 
        : '0 days'
    };
  } catch (error) {
    console.error('Failed to fetch maintenance stats:', error);
    if (error.response?.status === 401) {
      console.error('Authentication required. Please log in again.');
    }
  }
};

const formatTimestamp = (date) => {
  if (!date) return '';
  const now = new Date();
  const then = new Date(date);
  const diffMs = now - then;
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);
  
  if (diffHours < 24) return `${diffHours} hours ago`;
  if (diffDays < 7) return `${diffDays} days ago`;
  return then.toLocaleDateString();
};

const handleMaintenanceCreated = () => {
  showModal.value = false;
  fetchMaintenanceRequests();
  fetchMaintenanceStats();
};

const viewTicketDetails = (ticket) => {
  selectedTicket.value = ticket;
  showDetailsModal.value = true;
};

const editTicket = (ticket) => {
  selectedTicket.value = ticket;
  editForm.value = {
    status: ticket.status || 'open',
    priority: ticket.priority || 'medium'
  };
  showEditModal.value = true;
};

const saveTicketEdit = async () => {
  try {
    await api.updateMaintenanceRequest(selectedTicket.value.id, editForm.value);
    showEditModal.value = false;
    await fetchMaintenanceRequests();
    await fetchMaintenanceStats();
  } catch (error) {
    console.error('Failed to update maintenance request:', error);
  }
};

const deleteTicket = (ticket) => {
  selectedTicket.value = ticket;
  showDeleteModal.value = true;
};

const confirmDelete = async () => {
  try {
    await api.deleteMaintenanceRequest(selectedTicket.value.id);
    showDeleteModal.value = false;
    await fetchMaintenanceRequests();
    await fetchMaintenanceStats();
  } catch (error) {
    console.error('Failed to delete maintenance request:', error);
  }
};

onMounted(() => {
  fetchMaintenanceRequests();
  fetchMaintenanceStats();
});
</script>

<style scoped>
.maintenance-page {
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
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 0.75rem;
  padding: 1.5rem;
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.875rem;
  color: #6B7280;
}

.tickets-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.ticket-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.ticket-header {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.priority-badge, .status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: capitalize;
}

.priority-badge.urgent {
  background: #FEE2E2;
  color: #991B1B;
}

.priority-badge.high {
  background: #FED7AA;
  color: #9A3412;
}

.priority-badge.medium {
  background: #FEF3C7;
  color: #92400E;
}

.status-badge.open {
  background: #DBEAFE;
  color: #1E40AF;
}

.status-badge.in-progress {
  background: #FEF3C7;
  color: #92400E;
}

.ticket-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 0.5rem;
}

.ticket-description {
  font-size: 0.875rem;
  color: #6B7280;
  margin-bottom: 1rem;
}

.ticket-footer {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #9CA3AF;
  margin-bottom: 1rem;
}

.ticket-property {
  font-weight: 500;
}

.ticket-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #E5E7EB;
}

.btn-view-sm, .btn-edit-sm, .btn-delete-sm {
  flex: 1;
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-view-sm {
  background: #DBEAFE;
  color: #1E40AF;
}

.btn-view-sm:hover {
  background: #BFDBFE;
}

.btn-edit-sm {
  background: #FEF3C7;
  color: #92400E;
}

.btn-edit-sm:hover {
  background: #FDE68A;
}

.btn-delete-sm {
  background: #FEE2E2;
  color: #991B1B;
}

.btn-delete-sm:hover {
  background: #FECACA;
}

.details-content {
  padding: 1rem 0;
}

.detail-item {
  display: flex;
  flex-direction: column;
  padding: 0.75rem 0;
  border-bottom: 1px solid #E5E7EB;
  gap: 0.25rem;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  font-weight: 600;
  color: #6B7280;
  font-size: 0.875rem;
}

.detail-value {
  color: #1A1A1A;
  font-size: 0.9375rem;
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

