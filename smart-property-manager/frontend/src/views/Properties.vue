<template>
  <div class="properties-page">
    <!-- Page Header -->
    <div class="page-header">
      <h2 class="page-title">Property Portfolio</h2>
      <button @click="showAddPropertyModal = true" class="btn-add-property">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Add Property
      </button>
    </div>

    <!-- Property Locations Map -->
    <div class="map-section">
      <div class="map-header">
        <h3>Property Locations</h3>
      </div>
      <div class="map-container">
        <div class="map-placeholder">
          <svg class="map-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
          </svg>
          <p class="map-text">Interactive Map View</p>
          <p class="map-subtext">Google Maps API Integration</p>
        </div>
      </div>
    </div>

    <!-- Properties Grid -->
    <div class="properties-grid" v-if="!loading && properties.length > 0">
      <div v-for="property in properties" :key="property?.id || Math.random()" class="property-card">
        <!-- Property Name & Location -->
        <div class="property-header">
          <h3 class="property-name">{{ property?.name || 'Unnamed Property' }}</h3>
          <p class="property-location">{{ property?.city || 'Unknown' }} • {{ property?.total_units || 0 }} Units</p>
        </div>

        <!-- Occupancy Badge -->
        <div class="property-metrics">
          <span 
            class="occupancy-badge"
            :class="getOccupancyClass(property?.occupancy_rate || 0)"
          >
            {{ property?.occupancy_rate || 0 }}% Occupied
          </span>
        </div>

        <!-- Financial Info -->
        <div class="property-financials">
          <div class="financial-item">
            <span class="financial-label">Monthly Revenue:</span>
            <span class="financial-value">${{ formatNumber(property?.monthly_revenue || 0) }}</span>
          </div>
          <div class="financial-item">
            <span class="financial-label">Property Value:</span>
            <span class="financial-value">${{ formatValue(property?.current_value || 0) }}</span>
          </div>
          <div class="financial-item">
            <span class="financial-label">ROI:</span>
            <span class="financial-value roi">{{ property?.roi || 0 }}%</span>
          </div>
        </div>

        <!-- Actions -->
        <div class="property-actions">
          <button @click="viewPropertyDetails(property)" class="btn-view">View Details</button>
          <button @click="editProperty(property)" class="btn-edit">Edit</button>
          <button @click="deleteProperty(property)" class="btn-delete">Delete</button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <p>Loading properties...</p>
    </div>

    <!-- Empty State -->
    <div v-if="!loading && properties.length === 0" class="empty-state">
      <p>No properties found</p>
    </div>

    <!-- Add Property Modal -->
    <AddPropertyModal
      :isOpen="showAddPropertyModal"
      @close="showAddPropertyModal = false"
      @success="handlePropertyAdded"
    />

    <!-- View Details Modal -->
    <ConfirmModal
      :isOpen="showDetailsModal"
      :title="selectedProperty?.name || 'Property Details'"
      confirmText="Close"
      cancelText=""
      @close="showDetailsModal = false"
      @confirm="showDetailsModal = false"
    >
      <div class="details-content">
        <div class="detail-item">
          <span class="detail-label">Address:</span>
          <span class="detail-value">{{ selectedProperty?.address }}, {{ selectedProperty?.city }}, {{ selectedProperty?.state }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Type:</span>
          <span class="detail-value">{{ selectedProperty?.property_type }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Units:</span>
          <span class="detail-value">{{ selectedProperty?.occupied_units }}/{{ selectedProperty?.total_units }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Occupancy Rate:</span>
          <span class="detail-value">{{ selectedProperty?.occupancy_rate || 0 }}%</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Monthly Revenue:</span>
          <span class="detail-value">${{ formatNumber(selectedProperty?.monthly_revenue || 0) }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Property Value:</span>
          <span class="detail-value">${{ formatNumber(selectedProperty?.current_value || 0) }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">ROI:</span>
          <span class="detail-value">{{ selectedProperty?.roi || 0 }}%</span>
        </div>
      </div>
    </ConfirmModal>

    <!-- Edit Property Modal -->
    <ConfirmModal
      :isOpen="showEditModal"
      title="Edit Property"
      confirmText="Save"
      @close="showEditModal = false"
      @confirm="savePropertyEdit"
    >
      <div class="edit-form">
        <div class="form-group">
          <label>Property Name</label>
          <input v-model="editForm.name" type="text" class="form-input" />
        </div>
        <div class="form-group">
          <label>Monthly Revenue</label>
          <input v-model="editForm.monthly_revenue" type="number" class="form-input" />
        </div>
      </div>
    </ConfirmModal>

    <!-- Delete Confirmation Modal -->
    <ConfirmModal
      :isOpen="showDeleteModal"
      title="Delete Property"
      confirmText="Delete"
      confirmType="danger"
      @close="showDeleteModal = false"
      @confirm="confirmDelete"
    >
      <p>Are you sure you want to delete <strong>{{ selectedProperty?.name }}</strong>? This action cannot be undone.</p>
    </ConfirmModal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';
import AddPropertyModal from '../components/AddPropertyModal.vue';
import ConfirmModal from '../components/ConfirmModal.vue';

const properties = ref([]);
const loading = ref(true);
const showAddPropertyModal = ref(false);
const showDetailsModal = ref(false);
const showEditModal = ref(false);
const showDeleteModal = ref(false);
const selectedProperty = ref(null);
const editForm = ref({ name: '', monthly_revenue: '' });

const loadProperties = async () => {
  loading.value = true;
  try {
    const response = await api.getProperties();
    // Handle both array and paginated response formats
    properties.value = Array.isArray(response.data) ? response.data : (response.data.results || []);
  } catch (error) {
    console.error('Error loading properties:', error);
    properties.value = [];
  } finally {
    loading.value = false;
  }
};

const handlePropertyAdded = () => {
  loadProperties();
};

const viewPropertyDetails = (property) => {
  selectedProperty.value = property;
  showDetailsModal.value = true;
};

const editProperty = (property) => {
  selectedProperty.value = property;
  editForm.value = {
    name: property.name,
    monthly_revenue: property.monthly_revenue
  };
  showEditModal.value = true;
};

const savePropertyEdit = async () => {
  try {
    await api.updateProperty(selectedProperty.value.id, {
      ...selectedProperty.value,
      ...editForm.value
    });
    showEditModal.value = false;
    loadProperties();
  } catch (error) {
    console.error('Error updating property:', error);
  }
};

const deleteProperty = (property) => {
  selectedProperty.value = property;
  showDeleteModal.value = true;
};

const confirmDelete = async () => {
  try {
    await api.deleteProperty(selectedProperty.value.id);
    showDeleteModal.value = false;
    loadProperties();
  } catch (error) {
    console.error('Error deleting property:', error);
  }
};

const getOccupancyClass = (rate) => {
  if (rate >= 95) return 'high';
  if (rate >= 85) return 'medium';
  return 'low';
};

const formatNumber = (num) => {
  return new Intl.NumberFormat('en-US').format(num);
};

const formatValue = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(0) + 'K';
  }
  return formatNumber(num);
};

onMounted(() => {
  loadProperties();
});
</script>

<style scoped>
.properties-page {
  max-width: 1400px;
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: #1F2937;
}

.btn-add-property {
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

.btn-add-property svg {
  width: 20px;
  height: 20px;
}

.btn-add-property:hover {
  background: #2563EB;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

/* Map Section */
.map-section {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
}

.map-header {
  margin-bottom: 1rem;
}

.map-header h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1F2937;
}

.map-container {
  height: 300px;
  background: #F3F4F6;
  border-radius: 0.5rem;
  overflow: hidden;
}

.map-placeholder {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #9CA3AF;
}

.map-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 0.5rem;
  color: #D1D5DB;
}

.map-text {
  font-size: 1rem;
  font-weight: 500;
  color: #6B7280;
}

.map-subtext {
  font-size: 0.875rem;
  color: #9CA3AF;
}

/* Properties Grid */
.properties-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

/* Property Card */
.property-card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  transition: all 0.2s;
}

.property-card:hover {
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  transform: translateY(-2px);
}

.property-header {
  margin-bottom: 1rem;
}

.property-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1F2937;
  margin-bottom: 0.25rem;
}

.property-location {
  font-size: 0.875rem;
  color: #6B7280;
}

/* Occupancy Badge */
.property-metrics {
  margin-bottom: 1rem;
}

.occupancy-badge {
  display: inline-flex;
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
}

.occupancy-badge.high {
  background: #D1FAE5;
  color: #10B981;
}

.occupancy-badge.medium {
  background: #FEF3C7;
  color: #F59E0B;
}

.occupancy-badge.low {
  background: #FEE2E2;
  color: #EF4444;
}

/* Financial Info */
.property-financials {
  padding: 1rem 0;
  border-top: 1px solid #E5E7EB;
  border-bottom: 1px solid #E5E7EB;
  margin-bottom: 1rem;
}

.financial-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.financial-item:last-child {
  margin-bottom: 0;
}

.financial-label {
  font-size: 0.875rem;
  color: #6B7280;
}

.financial-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1F2937;
}

.financial-value.roi {
  color: #10B981;
}

/* Actions */
.property-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-view, .btn-edit, .btn-delete {
  flex: 1;
  padding: 0.625rem 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-view {
  background: white;
  color: #3B82F6;
  border: 1px solid #3B82F6;
}

.btn-view:hover {
  background: #3B82F6;
  color: white;
}

.btn-edit {
  background: #F59E0B;
  color: white;
}

.btn-edit:hover {
  background: #D97706;
}

.btn-delete {
  background: #EF4444;
  color: white;
}

.btn-delete:hover {
  background: #DC2626;
}

/* Loading & Empty States */
.loading-state,
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #9CA3AF;
}

/* Modal Content Styles */
.details-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem;
  background: #F9FAFB;
  border-radius: 0.5rem;
}

.detail-label {
  font-weight: 600;
  color: #6B7280;
}

.detail-value {
  color: #1F2937;
  font-weight: 500;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.form-input {
  padding: 0.625rem 0.75rem;
  border: 1px solid #D1D5DB;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.form-input:focus {
  outline: none;
  border-color: #3B82F6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
</style>
