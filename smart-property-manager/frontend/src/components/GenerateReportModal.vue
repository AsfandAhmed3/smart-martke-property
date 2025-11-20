<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
    <div class="modal-container">
      <!-- Modal Header -->
      <div class="modal-header">
        <h2 class="modal-title">Generate Report</h2>
        <button @click="closeModal" class="close-button">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Modal Body -->
      <form @submit.prevent="handleGenerate" class="modal-body">
        <!-- Report Configuration Section -->
        <div class="section">
          <h3 class="section-title">Report Configuration</h3>
          
          <div class="form-group">
            <label for="report_type">Report Type</label>
            <select id="report_type" v-model="formData.report_type" required>
              <option value="">Select report type</option>
              <option value="portfolio">Portfolio Performance</option>
              <option value="financial">Financial Summary</option>
              <option value="property">Property Analysis</option>
              <option value="tenant">Tenant Report</option>
              <option value="maintenance">Maintenance Report</option>
              <option value="tax">Tax Report</option>
            </select>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="report_period">Report Period</label>
              <select id="report_period" v-model="formData.report_period" required>
                <option value="">Select period</option>
                <option value="current_month">Current Month</option>
                <option value="last_3_months">Last 3 Months</option>
                <option value="last_6_months">Last 6 Months</option>
                <option value="year_to_date">Year to Date</option>
                <option value="last_12_months">Last 12 Months</option>
                <option value="custom">Custom Range</option>
              </select>
            </div>

            <div class="form-group" v-if="formData.report_period === 'custom'">
              <label>Date Range</label>
              <div class="date-range">
                <input
                  v-model="formData.start_date"
                  type="date"
                  placeholder="Start Date"
                />
                <span class="date-separator">to</span>
                <input
                  v-model="formData.end_date"
                  type="date"
                  placeholder="End Date"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Property Selection Section -->
        <div class="section">
          <h3 class="section-title">Property Selection</h3>
          <div class="checkbox-group">
            <label class="checkbox-label">
              <input
                type="checkbox"
                v-model="formData.all_properties"
                @change="toggleAllProperties"
              />
              <span>All Properties</span>
            </label>
            <label
              v-for="property in properties"
              :key="property.id"
              class="checkbox-label"
            >
              <input
                type="checkbox"
                :value="property.id"
                v-model="formData.selected_properties"
                :disabled="formData.all_properties"
              />
              <span>{{ property.name }}</span>
            </label>
          </div>
        </div>

        <!-- Include Sections -->
        <div class="section">
          <h3 class="section-title">Include Sections</h3>
          <div class="checkbox-grid">
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.include_summary" />
              <span>Executive Summary</span>
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.include_property_details" />
              <span>Property Details</span>
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.include_financials" />
              <span>Financial Performance</span>
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.include_tenants" />
              <span>Tenant Information</span>
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.include_maintenance" />
              <span>Maintenance Records</span>
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.include_market" />
              <span>Market Analysis</span>
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.include_charts" />
              <span>Charts & Graphs</span>
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.include_recommendations" />
              <span>Recommendations</span>
            </label>
          </div>
        </div>

        <!-- Cap Rate Display -->
        <div class="cap-rate-section">
          <div class="cap-rate-header">
            <span class="cap-rate-label">Cap Rate</span>
            <span class="cap-rate-value">6.2%</span>
          </div>
          <div class="cap-rate-bar">
            <div class="cap-rate-fill" style="width: 62%"></div>
          </div>
          <div class="cap-rate-footer">
            <span class="cap-rate-market">Market Average: 5.8%</span>
          </div>
        </div>

        <!-- Delivery Options Section -->
        <div class="section">
          <h3 class="section-title">Delivery Options</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="format">Format</label>
              <select id="format" v-model="formData.format" required>
                <option value="pdf">PDF Report</option>
                <option value="excel">Excel Spreadsheet</option>
                <option value="powerpoint">PowerPoint Presentation</option>
                <option value="all">All Formats</option>
              </select>
            </div>

            <div class="form-group">
              <label for="email">Email Recipients</label>
              <input
                id="email"
                v-model="formData.email_recipients"
                type="email"
                placeholder="email@example.com"
              />
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="modal-footer">
          <button type="button" @click="closeModal" class="btn-cancel">
            Cancel
          </button>
          <button type="button" @click="handlePreview" class="btn-preview">
            Preview Report
          </button>
          <button type="submit" class="btn-generate" :disabled="loading">
            {{ loading ? 'Generating...' : 'Generate Report' }}
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
  report_type: '',
  report_period: '',
  start_date: '',
  end_date: '',
  all_properties: true,
  selected_properties: [],
  include_summary: true,
  include_property_details: true,
  include_financials: true,
  include_tenants: true,
  include_maintenance: false,
  include_market: false,
  include_charts: true,
  include_recommendations: false,
  format: 'pdf',
  email_recipients: '',
});

const properties = ref([]);
const loading = ref(false);

const loadProperties = async () => {
  try {
    const response = await api.getProperties();
    properties.value = response.data.results || response.data;
  } catch (err) {
    console.error('Failed to load properties:', err);
  }
};

const toggleAllProperties = () => {
  if (formData.value.all_properties) {
    formData.value.selected_properties = [];
  }
};

const closeModal = () => {
  emit('close');
  resetForm();
};

const resetForm = () => {
  formData.value = {
    report_type: '',
    report_period: '',
    start_date: '',
    end_date: '',
    all_properties: true,
    selected_properties: [],
    include_summary: true,
    include_property_details: true,
    include_financials: true,
    include_tenants: true,
    include_maintenance: false,
    include_market: false,
    include_charts: true,
    include_recommendations: false,
    format: 'pdf',
    email_recipients: '',
  };
};

const handlePreview = () => {
  console.log('Preview report:', formData.value);
  // TODO: Implement preview functionality
};

const handleGenerate = async () => {
  loading.value = true;

  try {
    // TODO: Replace with actual report API endpoint when backend is ready
    await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate API call
    emit('success');
    closeModal();
  } catch (err) {
    console.error('Failed to generate report:', err);
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
  max-width: 800px;
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

.date-range {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.date-range input {
  flex: 1;
}

.date-separator {
  font-size: 0.875rem;
  color: #6B7280;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.checkbox-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #374151;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 1rem;
  height: 1rem;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"]:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.cap-rate-section {
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 0.5rem;
  padding: 1.25rem;
  margin-bottom: 2rem;
}

.cap-rate-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.cap-rate-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.cap-rate-value {
  font-size: 1.25rem;
  font-weight: 600;
  color: #10B981;
}

.cap-rate-bar {
  width: 100%;
  height: 8px;
  background: #E5E7EB;
  border-radius: 9999px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.cap-rate-fill {
  height: 100%;
  background: linear-gradient(90deg, #10B981 0%, #34D399 100%);
  border-radius: 9999px;
  transition: width 0.3s;
}

.cap-rate-footer {
  display: flex;
  justify-content: flex-end;
}

.cap-rate-market {
  font-size: 0.75rem;
  color: #6B7280;
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

.btn-preview {
  padding: 0.75rem 1.5rem;
  background: #374151;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-preview:hover {
  background: #1F2937;
}

.btn-generate {
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

.btn-generate:hover:not(:disabled) {
  background: #2563EB;
}

.btn-generate:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
