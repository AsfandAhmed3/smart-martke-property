<template>
  <div class="dashboard">
    <!-- KPI Cards -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-header">
          <div>
            <p class="kpi-label">Occupancy Rate</p>
            <h2 class="kpi-value green">94.2%</h2>
            <p class="kpi-change positive">↗ +2.1%</p>
          </div>
          <div class="kpi-icon green-bg">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
          </div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-header">
          <div>
            <p class="kpi-label">Monthly Revenue</p>
            <h2 class="kpi-value blue">$386K</h2>
            <p class="kpi-change positive">↗ +8.3%</p>
          </div>
          <div class="kpi-icon blue-bg">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-header">
          <div>
            <p class="kpi-label">Average ROI</p>
            <h2 class="kpi-value purple">12.8%</h2>
            <p class="kpi-change positive">↗ +1.2%</p>
          </div>
          <div class="kpi-icon purple-bg">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-header">
          <div>
            <p class="kpi-label">Active Leases</p>
            <h2 class="kpi-value orange">127</h2>
            <p class="kpi-info">5 expiring soon</p>
          </div>
          <div class="kpi-icon orange-bg">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="charts-grid">
      <div class="chart-card">
        <h3 class="chart-title">Revenue Trend</h3>
        <div class="chart-placeholder">Chart will be implemented with Chart.js</div>
      </div>

      <div class="chart-card">
        <h3 class="chart-title">Property Performance</h3>
        <div class="chart-placeholder">Chart will be implemented with Chart.js</div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="activity-card">
      <h3 class="section-title">Recent Activity</h3>
      
      <div class="activity-list">
        <div class="activity-item">
          <div class="activity-icon success">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div class="activity-content">
            <p class="activity-title">Lease renewed for Sunset Apartments #204</p>
            <p class="activity-time">2 hours ago</p>
          </div>
        </div>

        <div class="activity-item">
          <div class="activity-icon info">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            </svg>
          </div>
          <div class="activity-content">
            <p class="activity-title">Maintenance request completed at Oak Street Complex</p>
            <p class="activity-time">4 hours ago</p>
          </div>
        </div>

        <div class="activity-item">
          <div class="activity-icon warning">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div class="activity-content">
            <p class="activity-title">Payment overdue: Downtown Plaza #1205</p>
            <p class="activity-time">1 day ago</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.dashboard {
  max-width: 1400px;
}

/* KPI Grid */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.kpi-card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
}

.kpi-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.kpi-label {
  font-size: 0.875rem;
  color: #6B7280;
  margin-bottom: 0.5rem;
}

.kpi-value {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.kpi-value.green {
  color: #10B981;
}

.kpi-value.blue {
  color: #3B82F6;
}

.kpi-value.purple {
  color: #A78BFA;
}

.kpi-value.orange {
  color: #F59E0B;
}

.kpi-change {
  font-size: 0.875rem;
  font-weight: 500;
}

.kpi-change.positive {
  color: #10B981;
}

.kpi-info {
  font-size: 0.875rem;
  color: #F59E0B;
}

.kpi-icon {
  width: 48px;
  height: 48px;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.kpi-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

.green-bg {
  background: #10B981;
}

.blue-bg {
  background: #3B82F6;
}

.purple-bg {
  background: #A78BFA;
}

.orange-bg {
  background: #F59E0B;
}

/* Charts Grid */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.chart-card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
}

.chart-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1F2937;
  margin-bottom: 1rem;
}

.chart-placeholder {
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F3F4F6;
  border-radius: 0.5rem;
  color: #6B7280;
}

/* Activity Section */
.activity-card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
}

.section-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1F2937;
  margin-bottom: 1.5rem;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border-radius: 0.5rem;
  transition: background 0.2s;
}

.activity-item:hover {
  background: #F9FAFB;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-icon svg {
  width: 20px;
  height: 20px;
}

.activity-icon.success {
  background: #D1FAE5;
  color: #10B981;
}

.activity-icon.info {
  background: #DBEAFE;
  color: #3B82F6;
}

.activity-icon.warning {
  background: #FEF3C7;
  color: #F59E0B;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-size: 0.938rem;
  font-weight: 500;
  color: #1F2937;
  margin-bottom: 0.25rem;
}

.activity-time {
  font-size: 0.813rem;
  color: #9CA3AF;
}
</style>
