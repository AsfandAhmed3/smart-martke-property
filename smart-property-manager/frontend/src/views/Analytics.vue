<template>
  <div class="analytics-page">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Analytics & ROI</h1>
        <p class="page-subtitle">Performance metrics and return on investment</p>
      </div>
      <button @click="showGenerateReportModal = true" class="btn-primary">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        Generate Report
      </button>
    </div>

    <!-- KPI Cards -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-header">
          <span class="kpi-label">Total Revenue</span>
          <span class="kpi-change positive">+8.3%</span>
        </div>
        <h2 class="kpi-value">$386,000</h2>
        <p class="kpi-subtitle">Monthly</p>
      </div>

      <div class="kpi-card">
        <div class="kpi-header">
          <span class="kpi-label">Average ROI</span>
          <span class="kpi-change positive">+2.1%</span>
        </div>
        <h2 class="kpi-value">12.8%</h2>
        <p class="kpi-subtitle">Across all properties</p>
      </div>

      <div class="kpi-card">
        <div class="kpi-header">
          <span class="kpi-label">Occupancy Rate</span>
          <span class="kpi-change positive">+2.4%</span>
        </div>
        <h2 class="kpi-value">94.2%</h2>
        <p class="kpi-subtitle">Above target (90%)</p>
      </div>

      <div class="kpi-card">
        <div class="kpi-header">
          <span class="kpi-label">Net Operating Income</span>
          <span class="kpi-change positive">+5.7%</span>
        </div>
        <h2 class="kpi-value">$318,000</h2>
        <p class="kpi-subtitle">Monthly</p>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="charts-section">
      <div class="chart-card large">
        <h3 class="chart-title">Revenue Trend</h3>
        <div class="chart-placeholder">
          <svg width="100" height="100" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
          </svg>
          <p>Chart visualization coming soon</p>
        </div>
      </div>

      <div class="chart-card">
        <h3 class="chart-title">Property Performance</h3>
        <div class="chart-placeholder">
          <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
          </svg>
          <p>Pie chart coming soon</p>
        </div>
      </div>
    </div>

    <!-- Property Performance Table -->
    <div class="performance-section">
      <h3 class="section-title">Property ROI Breakdown</h3>
      <div class="performance-table">
        <div class="performance-row header">
          <div class="performance-cell">Property</div>
          <div class="performance-cell">Investment</div>
          <div class="performance-cell">Monthly Revenue</div>
          <div class="performance-cell">Monthly Expenses</div>
          <div class="performance-cell">NOI</div>
          <div class="performance-cell">ROI</div>
        </div>
        <div v-for="property in properties" :key="property.id" class="performance-row">
          <div class="performance-cell">
            <strong>{{ property.name }}</strong>
          </div>
          <div class="performance-cell">${{ property.investment }}</div>
          <div class="performance-cell">${{ property.revenue }}</div>
          <div class="performance-cell">${{ property.expenses }}</div>
          <div class="performance-cell">${{ property.noi }}</div>
          <div class="performance-cell">
            <span :class="['roi-badge', property.roi_class]">{{ property.roi }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Generate Report Modal -->
    <GenerateReportModal
      :isOpen="showGenerateReportModal"
      @close="showGenerateReportModal = false"
      @success="handleReportGenerated"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import GenerateReportModal from '../components/GenerateReportModal.vue';

const showGenerateReportModal = ref(false);

const properties = ref([
  {
    id: 1,
    name: 'Sunset Apartments',
    investment: '3,200,000',
    revenue: '48,000',
    expenses: '14,000',
    noi: '34,000',
    roi: '13.5',
    roi_class: 'high',
  },
  {
    id: 2,
    name: 'Oak Street Complex',
    investment: '2,100,000',
    revenue: '32,400',
    expenses: '9,200',
    noi: '23,200',
    roi: '13.4',
    roi_class: 'high',
  },
  {
    id: 3,
    name: 'Downtown Plaza',
    investment: '5,800,000',
    revenue: '72,000',
    expenses: '18,000',
    noi: '54,000',
    roi: '11.2',
    roi_class: 'medium',
  },
]);

const handleReportGenerated = () => {
  console.log('Report generated successfully');
};
</script>

<style scoped>
.analytics-page {
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

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.kpi-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.kpi-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.kpi-label {
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
}

.kpi-change {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
}

.kpi-change.positive {
  background: #D1FAE5;
  color: #065F46;
}

.kpi-value {
  font-size: 2rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 0.25rem;
}

.kpi-subtitle {
  font-size: 0.75rem;
  color: #6B7280;
}

.charts-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.chart-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.chart-card.large {
  grid-column: span 1;
}

.chart-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 1.5rem;
}

.chart-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  color: #9CA3AF;
}

.chart-placeholder svg {
  margin-bottom: 1rem;
}

.chart-placeholder p {
  font-size: 0.875rem;
}

.performance-section {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.section-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 1.5rem;
}

.performance-table {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.performance-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr;
  gap: 1rem;
  padding: 1rem;
  border-radius: 0.5rem;
}

.performance-row.header {
  background: #F9FAFB;
  font-weight: 600;
  color: #6B7280;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.performance-row:not(.header) {
  background: #F9FAFB;
  font-size: 0.875rem;
  color: #374151;
}

.performance-cell {
  display: flex;
  align-items: center;
}

.roi-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.roi-badge.high {
  background: #D1FAE5;
  color: #065F46;
}

.roi-badge.medium {
  background: #DBEAFE;
  color: #1E40AF;
}

.roi-badge.low {
  background: #FEF3C7;
  color: #92400E;
}
</style>
