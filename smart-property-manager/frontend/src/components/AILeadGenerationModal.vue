<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
    <div class="modal-container">
      <!-- Modal Header -->
      <div class="modal-header">
        <div class="header-content">
          <div class="success-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="#10B981" stroke-width="2" fill="#D1FAE5" />
              <path d="M8 12l2 2 4-4" stroke="#10B981" stroke-width="2" stroke-linecap="round" />
            </svg>
          </div>
          <div>
            <h2 class="modal-title">AI Lead Generation Complete!</h2>
            <p class="modal-subtitle">Analysis finished successfully</p>
          </div>
        </div>
        <button @click="closeModal" class="close-button">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Modal Body -->
      <div class="modal-body">
        <!-- Analysis Results -->
        <div class="section">
          <h3 class="section-title">Analysis Results</h3>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-value">2,847</div>
              <div class="stat-label">Properties Analyzed</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">23</div>
              <div class="stat-label">Potential Leads Found</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">8</div>
              <div class="stat-label">High-Priority Contacts</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">7</div>
              <div class="stat-label">Investment Opportunities</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">8</div>
              <div class="stat-label">Distressed Properties</div>
            </div>
          </div>
        </div>

        <!-- Lead Quality Scores -->
        <div class="section">
          <h3 class="section-title">Lead Quality Scores</h3>
          <div class="quality-scores">
            <div class="score-row">
              <div class="score-range">90-100%</div>
              <div class="score-bar-container">
                <div class="score-bar" style="width: 15%; background: #10B981;"></div>
              </div>
              <div class="score-count">3 leads</div>
            </div>
            <div class="score-row">
              <div class="score-range">80-89%</div>
              <div class="score-bar-container">
                <div class="score-bar" style="width: 25%; background: #34D399;"></div>
              </div>
              <div class="score-count">5 leads</div>
            </div>
            <div class="score-row">
              <div class="score-range">70-79%</div>
              <div class="score-bar-container">
                <div class="score-bar" style="width: 40%; background: #6EE7B7;"></div>
              </div>
              <div class="score-count">8 leads</div>
            </div>
            <div class="score-row">
              <div class="score-range">60-69%</div>
              <div class="score-bar-container">
                <div class="score-bar" style="width: 35%; background: #A7F3D0;"></div>
              </div>
              <div class="score-count">7 leads</div>
            </div>
          </div>
        </div>

        <!-- Market Insights -->
        <div class="section">
          <h3 class="section-title">Market Insights</h3>
          <div class="insights-grid">
            <div class="insight-card">
              <div class="insight-icon" style="background: #DBEAFE; color: #1E40AF;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="insight-content">
                <div class="insight-label">Average Days on Market</div>
                <div class="insight-value">45 days</div>
              </div>
            </div>
            <div class="insight-card">
              <div class="insight-icon" style="background: #FEE2E2; color: #991B1B;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <div class="insight-content">
                <div class="insight-label">Price Reduction Trends</div>
                <div class="insight-value">+12%</div>
              </div>
            </div>
            <div class="insight-card">
              <div class="insight-icon" style="background: #FEF3C7; color: #92400E;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div class="insight-content">
                <div class="insight-label">Foreclosure Risk Properties</div>
                <div class="insight-value">8 properties</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Completion Checklist -->
        <div class="section">
          <h3 class="section-title">Completed Actions</h3>
          <div class="checklist">
            <div class="checklist-item">
              <div class="check-icon">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                  <path d="M5 12l5 5L20 7" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </div>
              <span>Contact information updated</span>
            </div>
            <div class="checklist-item">
              <div class="check-icon">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                  <path d="M5 12l5 5L20 7" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </div>
              <span>Email templates generated</span>
            </div>
            <div class="checklist-item">
              <div class="check-icon">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                  <path d="M5 12l5 5L20 7" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </div>
              <span>Call scripts prepared</span>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="modal-footer">
          <button type="button" @click="exportLeads" class="btn-export">
            Export Leads
          </button>
          <button type="button" @click="closeModal" class="btn-close">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['close']);

const closeModal = () => {
  emit('close');
};

const exportLeads = () => {
  console.log('Exporting leads...');
  // TODO: Implement export functionality
};
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
  max-width: 900px;
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

.header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.success-icon {
  flex-shrink: 0;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 0.25rem;
}

.modal-subtitle {
  font-size: 0.875rem;
  color: #6B7280;
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 0.5rem;
  padding: 1rem;
  text-align: center;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 600;
  color: #7C6FDC;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.75rem;
  color: #6B7280;
  font-weight: 500;
}

.quality-scores {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.score-row {
  display: grid;
  grid-template-columns: 100px 1fr 80px;
  align-items: center;
  gap: 1rem;
}

.score-range {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.score-bar-container {
  background: #E5E7EB;
  height: 24px;
  border-radius: 0.375rem;
  overflow: hidden;
}

.score-bar {
  height: 100%;
  border-radius: 0.375rem;
  transition: width 0.3s;
}

.score-count {
  font-size: 0.875rem;
  color: #6B7280;
  text-align: right;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.insight-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 0.5rem;
  padding: 1rem;
}

.insight-icon {
  width: 40px;
  height: 40px;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.insight-content {
  flex: 1;
}

.insight-label {
  font-size: 0.75rem;
  color: #6B7280;
  margin-bottom: 0.25rem;
}

.insight-value {
  font-size: 1rem;
  font-weight: 600;
  color: #1A1A1A;
}

.checklist {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.checklist-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #374151;
}

.check-icon {
  width: 24px;
  height: 24px;
  background: #D1FAE5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.check-icon svg {
  stroke: #10B981;
}

.modal-footer {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  padding-top: 1.5rem;
  border-top: 1px solid #E5E7EB;
  margin-top: 1.5rem;
}

.btn-export {
  padding: 0.75rem 1.5rem;
  background: #7C6FDC;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-export:hover {
  background: #6B5FCD;
}

.btn-close {
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

.btn-close:hover {
  background: #2563EB;
}
</style>
