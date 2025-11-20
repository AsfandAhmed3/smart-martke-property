<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
    <div class="modal-container">
      <!-- Modal Header -->
      <div class="modal-header">
        <h2 class="modal-title">Add New Property</h2>
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
        <div class="form-group">
          <label for="name">Property Name</label>
          <input
            id="name"
            v-model="formData.name"
            type="text"
            placeholder="Enter property name"
            required
          />
        </div>

        <div class="form-group">
          <label for="property_type">Property Type</label>
          <select id="property_type" v-model="formData.property_type" required>
            <option value="">Select type</option>
            <option value="residential">Apartment Complex</option>
            <option value="commercial">Commercial</option>
            <option value="mixed">Single Family</option>
            <option value="industrial">Industrial</option>
            <option value="land">Land</option>
          </select>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="purchase_price">Purchase Price</label>
            <input
              id="purchase_price"
              v-model.number="formData.purchase_price"
              type="number"
              placeholder="0.00"
              step="0.01"
              required
            />
          </div>

          <div class="form-group">
            <label for="total_units">Number of Units</label>
            <input
              id="total_units"
              v-model.number="formData.total_units"
              type="number"
              placeholder="0"
              required
            />
          </div>
        </div>

        <div class="form-group">
          <label for="address">Address</label>
          <textarea
            id="address"
            v-model="formData.address"
            rows="3"
            placeholder="Enter full address"
            required
          ></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="city">City</label>
            <input
              id="city"
              v-model="formData.city"
              type="text"
              placeholder="City"
              required
            />
          </div>

          <div class="form-group">
            <label for="state">State</label>
            <input
              id="state"
              v-model="formData.state"
              type="text"
              placeholder="State"
              required
            />
          </div>

          <div class="form-group">
            <label for="zip_code">Zip Code</label>
            <input
              id="zip_code"
              v-model="formData.zip_code"
              type="text"
              placeholder="00000"
              required
            />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="current_value">Current Value</label>
            <input
              id="current_value"
              v-model.number="formData.current_value"
              type="number"
              placeholder="0.00"
              step="0.01"
            />
          </div>

          <div class="form-group">
            <label for="monthly_revenue">Monthly Revenue</label>
            <input
              id="monthly_revenue"
              v-model.number="formData.monthly_revenue"
              type="number"
              placeholder="0.00"
              step="0.01"
            />
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="modal-footer">
          <button type="button" @click="closeModal" class="btn-cancel">
            Cancel
          </button>
          <button type="submit" class="btn-submit" :disabled="loading">
            {{ loading ? 'Adding...' : 'Add Property' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import api from '../services/api';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['close', 'success']);

const formData = ref({
  name: '',
  property_type: '',
  purchase_price: '',
  current_value: '',
  total_units: '',
  occupied_units: 0,
  address: '',
  city: '',
  state: '',
  zip_code: '',
  monthly_revenue: '',
  monthly_expenses: 0,
  status: 'active',
});

const loading = ref(false);
const error = ref('');

const closeModal = () => {
  emit('close');
  resetForm();
};

const resetForm = () => {
  formData.value = {
    name: '',
    property_type: '',
    purchase_price: '',
    current_value: '',
    total_units: '',
    occupied_units: 0,
    address: '',
    city: '',
    state: '',
    zip_code: '',
    monthly_revenue: '',
    monthly_expenses: 0,
    status: 'active',
  };
  error.value = '';
};

const handleSubmit = async () => {
  loading.value = true;
  error.value = '';

  try {
    await api.createProperty(formData.value);
    emit('success');
    closeModal();
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to create property';
  } finally {
    loading.value = false;
  }
};

watch(() => props.isOpen, (newVal) => {
  if (!newVal) {
    resetForm();
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
  max-width: 600px;
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
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #D1D5DB;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #7C6FDC;
  box-shadow: 0 0 0 3px rgba(124, 111, 220, 0.1);
}

.form-group textarea {
  resize: vertical;
  font-family: inherit;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
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
