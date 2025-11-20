<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
    <div class="modal-container">
      <!-- Modal Header -->
      <div class="modal-header">
        <h2 class="modal-title">Create New Lease</h2>
        <button @click="closeModal" class="close-button">
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
        <!-- Lease Information Section -->
        <div class="section">
          <h3 class="section-title">Lease Information</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="property">Property</label>
              <select id="property" v-model="formData.property_id" required>
                <option value="">Select property</option>
                <option v-for="property in properties" :key="property.id" :value="property.id">
                  {{ property.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="unit_number">Unit Number</label>
              <input
                id="unit_number"
                v-model="formData.unit_number"
                type="text"
                placeholder="Unit #"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label for="tenant">Tenant</label>
            <select id="tenant" v-model="formData.tenant_id" required>
              <option value="">Select tenant</option>
              <option value="new">+ Add New Tenant</option>
              <option v-for="tenant in tenants" :key="tenant.id" :value="tenant.id">
                {{ tenant.first_name }} {{ tenant.last_name }}
              </option>
            </select>
          </div>
        </div>

        <!-- Lease Terms Section -->
        <div class="section">
          <h3 class="section-title">Lease Terms</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="start_date">Start Date</label>
              <input
                id="start_date"
                v-model="formData.start_date"
                type="date"
                required
              />
            </div>

            <div class="form-group">
              <label for="end_date">End Date</label>
              <input
                id="end_date"
                v-model="formData.end_date"
                type="date"
                required
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="monthly_rent">Monthly Rent</label>
              <input
                id="monthly_rent"
                v-model.number="formData.monthly_rent"
                type="number"
                placeholder="0.00"
                step="0.01"
                required
              />
            </div>

            <div class="form-group">
              <label for="security_deposit">Security Deposit</label>
              <input
                id="security_deposit"
                v-model.number="formData.security_deposit"
                type="number"
                placeholder="0.00"
                step="0.01"
                required
              />
            </div>
          </div>
        </div>

        <!-- Payment Terms Section -->
        <div class="section">
          <h3 class="section-title">Payment Terms</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="due_date">Due Date</label>
              <select id="due_date" v-model="formData.due_date" required>
                <option value="">Select due date</option>
                <option value="1">1st of month</option>
                <option value="15">15th of month</option>
              </select>
            </div>

            <div class="form-group">
              <label for="late_fee">Late Fee</label>
              <input
                id="late_fee"
                v-model.number="formData.late_fee"
                type="number"
                placeholder="0.00"
                step="0.01"
              />
            </div>

            <div class="form-group">
              <label for="grace_period">Grace Period (days)</label>
              <input
                id="grace_period"
                v-model.number="formData.grace_period"
                type="number"
                placeholder="5"
              />
            </div>
          </div>
        </div>

        <!-- Status Badge (if editing) -->
        <div v-if="formData.id" class="status-badges">
          <span class="badge badge-active">Active</span>
        </div>

        <!-- Modal Footer -->
        <div class="modal-footer">
          <button type="button" @click="closeModal" class="btn-cancel">
            Cancel
          </button>
          <button type="submit" class="btn-submit" :disabled="loading">
            {{ loading ? 'Creating...' : 'Create Lease' }}
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
  isOpen: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['close', 'success']);

const formData = ref({
  property_id: '',
  unit_number: '',
  tenant_id: '',
  start_date: '',
  end_date: '',
  monthly_rent: '',
  security_deposit: '',
  due_date: '1',
  late_fee: 50,
  grace_period: 5,
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
    property_id: '',
    unit_number: '',
    tenant_id: '',
    start_date: '',
    end_date: '',
    monthly_rent: '',
    security_deposit: '',
    due_date: '1',
    late_fee: 50,
    grace_period: 5,
  };
  error.value = '';
};

const handleSubmit = async () => {
  loading.value = true;
  error.value = '';

  try {
    const leaseData = {
      lease_property: formData.value.property_id,
      unit_number: formData.value.unit_number,
      tenant: formData.value.tenant_id,
      start_date: formData.value.start_date,
      end_date: formData.value.end_date,
      monthly_rent: parseFloat(formData.value.monthly_rent),
      security_deposit: parseFloat(formData.value.security_deposit),
      payment_due_day: parseInt(formData.value.due_date),
      late_fee: parseFloat(formData.value.late_fee),
      grace_period: parseInt(formData.value.grace_period),
      status: 'pending'
    };
    await api.createLease(leaseData);
    emit('success');
    closeModal();
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to create lease';
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

.error-message {
  background: #FEE2E2;
  border: 1px solid #F87171;
  color: #DC2626;
  padding: 0.75rem 1.5rem;
  margin: 1rem 1.5rem 0;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.modal-body {
  padding: 1.5rem;
}

.section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #E5E7EB;
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

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #D1D5DB;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #7C6FDC;
  box-shadow: 0 0 0 3px rgba(124, 111, 220, 0.1);
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
}

.status-badges {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.badge {
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge-active {
  background: #D1FAE5;
  color: #065F46;
}

.badge-expiring {
  background: #FEF3C7;
  color: #92400E;
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
