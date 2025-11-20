<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
    <div class="modal-container">
      <!-- Modal Header -->
      <div class="modal-header">
        <h2 class="modal-title">Add New Tenant</h2>
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
        <!-- Personal Information Section -->
        <div class="section">
          <h3 class="section-title">Personal Information</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="first_name">First Name</label>
              <input
                id="first_name"
                v-model="formData.first_name"
                type="text"
                placeholder="Enter first name"
                required
              />
            </div>

            <div class="form-group">
              <label for="last_name">Last Name</label>
              <input
                id="last_name"
                v-model="formData.last_name"
                type="text"
                placeholder="Enter last name"
                required
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="email">Email</label>
              <input
                id="email"
                v-model="formData.email"
                type="email"
                placeholder="email@example.com"
                required
              />
            </div>

            <div class="form-group">
              <label for="phone">Phone</label>
              <input
                id="phone"
                v-model="formData.phone"
                type="tel"
                placeholder="(555) 123-4567"
                required
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="date_of_birth">Date of Birth</label>
              <input
                id="date_of_birth"
                v-model="formData.date_of_birth"
                type="date"
                required
              />
            </div>

            <div class="form-group">
              <label for="ssn">Social Security Number</label>
              <input
                id="ssn"
                v-model="formData.ssn"
                type="text"
                placeholder="XXX-XX-XXXX"
                maxlength="11"
              />
            </div>
          </div>
        </div>

        <!-- Employment Information Section -->
        <div class="section">
          <h3 class="section-title">Employment Information</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="employer">Employer</label>
              <input
                id="employer"
                v-model="formData.employer"
                type="text"
                placeholder="Company name"
              />
            </div>

            <div class="form-group">
              <label for="job_title">Job Title</label>
              <input
                id="job_title"
                v-model="formData.job_title"
                type="text"
                placeholder="Position"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="monthly_income">Monthly Income</label>
              <input
                id="monthly_income"
                v-model.number="formData.monthly_income"
                type="number"
                placeholder="0.00"
                step="0.01"
              />
            </div>

            <div class="form-group">
              <label for="employment_length">Employment Length</label>
              <select id="employment_length" v-model="formData.employment_length">
                <option value="">Select duration</option>
                <option value="less_than_1">Less than 1 year</option>
                <option value="1_2_years">1-2 years</option>
                <option value="3_5_years">3-5 years</option>
                <option value="5_plus_years">5+ years</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Rental Information Section -->
        <div class="section">
          <h3 class="section-title">Rental Information</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="property">Property</label>
              <select id="property" v-model="formData.property_id">
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
              />
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="modal-footer">
          <button type="button" @click="closeModal" class="btn-cancel">
            Cancel
          </button>
          <button type="submit" class="btn-submit" :disabled="loading">
            {{ loading ? 'Adding...' : 'Add Tenant' }}
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
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  date_of_birth: '',
  ssn: '',
  employer: '',
  job_title: '',
  monthly_income: '',
  employment_length: '',
  property_id: '',
  unit_number: '',
});

const properties = ref([]);
const loading = ref(false);
const error = ref('');

const loadProperties = async () => {
  try {
    const response = await api.getProperties();
    properties.value = response.data.results || response.data;
  } catch (err) {
    console.error('Failed to load properties:', err);
  }
};

const closeModal = () => {
  emit('close');
  resetForm();
};

const resetForm = () => {
  formData.value = {
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    date_of_birth: '',
    ssn: '',
    employer: '',
    job_title: '',
    monthly_income: '',
    employment_length: '',
    property_id: '',
    unit_number: '',
  };
  error.value = '';
};

const handleSubmit = async () => {
  loading.value = true;
  error.value = '';

  try {
    // Prepare tenant data
    const tenantData = {
      first_name: formData.value.first_name,
      last_name: formData.value.last_name,
      email: formData.value.email,
      phone: formData.value.phone,
      date_of_birth: formData.value.date_of_birth || null,
      ssn_last4: formData.value.ssn ? formData.value.ssn.slice(-4) : null,
      employer: formData.value.employer || null,
      job_title: formData.value.job_title || null,
      monthly_income: formData.value.monthly_income || null,
      employment_length: formData.value.employment_length || null,
      property: formData.value.property_id || null,
      unit_number: formData.value.unit_number || null,
      status: 'active'
    };
    
    await api.createTenant(tenantData);
    emit('success');
    closeModal();
  } catch (err) {
    console.error('Tenant creation error:', err);
    error.value = err.response?.data?.detail || err.response?.data?.email?.[0] || 'Failed to create tenant';
  } finally {
    loading.value = false;
  }
};

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    loadProperties();
  } else {
    resetForm();
  }
});

onMounted(() => {
  if (props.isOpen) {
    loadProperties();
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
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
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
