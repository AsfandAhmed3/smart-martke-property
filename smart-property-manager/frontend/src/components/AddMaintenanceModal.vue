<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
    <div class="modal-container">
      <!-- Modal Header -->
      <div class="modal-header">
        <h2 class="modal-title">New Maintenance Request</h2>
        <button @click="closeModal" class="close-btn">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <!-- Modal Body -->
      <form @submit.prevent="handleSubmit" class="modal-body">
        <!-- Title -->
        <div class="form-group">
          <label class="form-label">Title *</label>
          <input
            v-model="formData.title"
            type="text"
            class="form-input"
            placeholder="Brief description of the issue"
            required
          />
        </div>

        <!-- Category & Priority -->
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Category *</label>
            <select v-model="formData.category" class="form-input" required>
              <option value="">Select category</option>
              <option value="plumbing">Plumbing</option>
              <option value="electrical">Electrical</option>
              <option value="hvac">HVAC</option>
              <option value="appliance">Appliance</option>
              <option value="structural">Structural</option>
              <option value="pest_control">Pest Control</option>
              <option value="landscaping">Landscaping</option>
              <option value="painting">Painting</option>
              <option value="flooring">Flooring</option>
              <option value="security">Security</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Priority *</label>
            <select v-model="formData.priority" class="form-input" required>
              <option value="">Select priority</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="emergency">Emergency</option>
            </select>
          </div>
        </div>

        <!-- Property & Unit -->
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Property *</label>
            <select v-model="formData.property_id" class="form-input" required>
              <option value="">Select property</option>
              <option v-for="property in properties" :key="property.id" :value="property.id">
                {{ property.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Unit Number</label>
            <input
              v-model="formData.unit_number"
              type="text"
              class="form-input"
              placeholder="e.g., 101, A, etc."
            />
          </div>
        </div>

        <!-- Tenant (Optional) -->
        <div class="form-group">
          <label class="form-label">Tenant (Optional)</label>
          <select v-model="formData.tenant_id" class="form-input">
            <option value="">Select tenant</option>
            <option v-for="tenant in tenants" :key="tenant.id" :value="tenant.id">
              {{ tenant.first_name }} {{ tenant.last_name }}
            </option>
          </select>
        </div>

        <!-- Description -->
        <div class="form-group">
          <label class="form-label">Description *</label>
          <textarea
            v-model="formData.description"
            class="form-input"
            rows="4"
            placeholder="Detailed description of the maintenance issue"
            required
          ></textarea>
        </div>

        <!-- Scheduled Date (Optional) -->
        <div class="form-group">
          <label class="form-label">Scheduled Date (Optional)</label>
          <input
            v-model="formData.scheduled_date"
            type="date"
            class="form-input"
          />
        </div>

        <!-- Modal Footer -->
        <div class="modal-footer">
          <button type="button" @click="closeModal" class="btn-secondary">Cancel</button>
          <button type="submit" class="btn-primary" :disabled="loading">
            {{ loading ? 'Creating...' : 'Create Request' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import api from '../services/api';

const props = defineProps({
  isOpen: Boolean,
});

const emit = defineEmits(['close', 'success']);

const formData = ref({
  title: '',
  description: '',
  category: '',
  priority: 'medium',
  property_id: '',
  unit_number: '',
  tenant_id: '',
  scheduled_date: ''
});

const properties = ref([]);
const tenants = ref([]);
const loading = ref(false);
const error = ref('');

const loadData = async () => {
  try {
    const [propertiesRes, tenantsRes] = await Promise.all([
      api.getProperties(),
      api.getTenants(),
    ]);
    properties.value = Array.isArray(propertiesRes.data) ? propertiesRes.data : (propertiesRes.data.results || []);
    tenants.value = Array.isArray(tenantsRes.data) ? tenantsRes.data : (tenantsRes.data.results || []);
  } catch (err) {
    console.error('Failed to load data:', err);
  }
};

const closeModal = () => {
  emit('close');
  resetForm();
};

const resetForm = () => {
  formData.value = {
    title: '',
    description: '',
    category: '',
    priority: 'medium',
    property_id: '',
    unit_number: '',
    tenant_id: '',
    scheduled_date: ''
  };
  error.value = '';
};

const handleSubmit = async () => {
  loading.value = true;
  error.value = '';

  try {
    const maintenanceData = {
      title: formData.value.title,
      description: formData.value.description,
      category: formData.value.category,
      priority: formData.value.priority,
      maintenance_property: formData.value.property_id,
      unit_number: formData.value.unit_number || null,
      tenant: formData.value.tenant_id || null,
      scheduled_date: formData.value.scheduled_date || null,
      status: 'open'
    };
    await api.createMaintenanceRequest(maintenanceData);
    emit('success');
    closeModal();
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to create maintenance request';
  } finally {
    loading.value = false;
  }
};

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    loadData();
  } else {
    resetForm();
  }
});

onMounted(() => {
  if (props.isOpen) {
    loadData();
  }
});
</script>

<style scoped>
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
  max-width: 700px;
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
  font-size: 1.5rem;
  font-weight: 600;
  color: #1A1A1A;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  color: #6B7280;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #1A1A1A;
}

.error-message {
  margin: 1rem 1.5rem;
  padding: 0.75rem 1rem;
  background: #FEE2E2;
  border: 1px solid #FCA5A5;
  border-radius: 0.5rem;
  color: #991B1B;
  font-size: 0.875rem;
}

.modal-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
  font-size: 0.875rem;
}

.form-input {
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: 1px solid #D1D5DB;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #3B82F6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

textarea.form-input {
  resize: vertical;
  font-family: inherit;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid #E5E7EB;
}

.btn-secondary {
  padding: 0.625rem 1.25rem;
  background: white;
  color: #374151;
  border: 1px solid #D1D5DB;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #F9FAFB;
}

.btn-primary {
  padding: 0.625rem 1.25rem;
  background: #3B82F6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #2563EB;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
