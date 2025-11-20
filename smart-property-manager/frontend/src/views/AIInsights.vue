<template>
  <div class="ai-insights-page">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">AI Insights</h1>
        <p class="page-subtitle">Artificial intelligence-powered analytics and recommendations</p>
      </div>
      <button @click="showAILeadModal = true" class="btn-primary">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
        Generate AI Leads
      </button>
    </div>

    <!-- Insights Grid -->
    <div class="insights-grid">
      <div class="insight-card featured">
        <div class="insight-icon" style="background: #DBEAFE;">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2">
            <path d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
        </div>
        <h3 class="insight-title">Market Opportunities</h3>
        <p class="insight-description">AI has identified 7 potential investment opportunities in your target markets based on price trends and demand analysis.</p>
        <button class="insight-btn">View Details</button>
      </div>

      <div class="insight-card">
        <div class="insight-icon" style="background: #D1FAE5;">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 class="insight-title">Rent Optimization</h3>
        <p class="insight-description">3 properties could increase rent by 5-8% based on market analysis</p>
      </div>

      <div class="insight-card">
        <div class="insight-icon" style="background: #FEF3C7;">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2">
            <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 class="insight-title">Maintenance Prediction</h3>
        <p class="insight-description">HVAC maintenance recommended for 2 units within next 30 days</p>
      </div>

      <div class="insight-card">
        <div class="insight-icon" style="background: #FEE2E2;">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#EF4444" stroke-width="2">
            <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h3 class="insight-title">Risk Alert</h3>
        <p class="insight-description">8 properties identified with potential foreclosure risk in area</p>
      </div>
    </div>

    <!-- Recommendations Section -->
    <div class="recommendations-section">
      <h2 class="section-title">AI Recommendations</h2>
      <div class="recommendations-list">
        <div v-for="rec in recommendations" :key="rec.id" class="recommendation-card">
          <div class="rec-header">
            <span :class="['rec-badge', rec.priority]">{{ rec.priority }}</span>
            <span class="rec-category">{{ rec.category }}</span>
          </div>
          <h3 class="rec-title">{{ rec.title }}</h3>
          <p class="rec-description">{{ rec.description }}</p>
          <div class="rec-metrics">
            <div class="metric">
              <span class="metric-label">Potential Impact</span>
              <span class="metric-value">{{ rec.impact }}</span>
            </div>
            <div class="metric">
              <span class="metric-label">Confidence</span>
              <span class="metric-value">{{ rec.confidence }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- AI Lead Generation Modal -->
    <AILeadGenerationModal
      :isOpen="showAILeadModal"
      @close="showAILeadModal = false"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import AILeadGenerationModal from '../components/AILeadGenerationModal.vue';

const showAILeadModal = ref(false);

const recommendations = ref([
  {
    id: 1,
    priority: 'high',
    category: 'Revenue',
    title: 'Increase Rent at Sunset Apartments',
    description: 'Market analysis shows similar properties charge 7% more. Consider gradual increase for renewals.',
    impact: '+$3,360/month',
    confidence: 92,
  },
  {
    id: 2,
    priority: 'medium',
    category: 'Maintenance',
    title: 'Schedule Preventive HVAC Service',
    description: 'Units #204 and #305 are due for maintenance based on usage patterns and age.',
    impact: 'Prevent $8K repair',
    confidence: 87,
  },
  {
    id: 3,
    priority: 'high',
    category: 'Investment',
    title: 'Acquisition Opportunity: Oak Street Area',
    description: 'Property values expected to rise 12% in next 18 months due to new development.',
    impact: '+15% ROI potential',
    confidence: 85,
  },
]);
</script>

<style scoped>
.ai-insights-page {
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
  background: #7C6FDC;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  background: #6B5FCD;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.insight-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 0.75rem;
  padding: 1.5rem;
  transition: all 0.2s;
}

.insight-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

.insight-card.featured {
  grid-column: span 2;
}

.insight-icon {
  width: 56px;
  height: 56px;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.insight-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 0.75rem;
}

.insight-description {
  font-size: 0.875rem;
  color: #6B7280;
  line-height: 1.5;
}

.insight-btn {
  margin-top: 1rem;
  padding: 0.625rem 1.25rem;
  background: #7C6FDC;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.insight-btn:hover {
  background: #6B5FCD;
}

.recommendations-section {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 0.75rem;
  padding: 2rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 1.5rem;
}

.recommendations-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.recommendation-card {
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.rec-header {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.rec-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: capitalize;
}

.rec-badge.high {
  background: #FEE2E2;
  color: #991B1B;
}

.rec-badge.medium {
  background: #FEF3C7;
  color: #92400E;
}

.rec-category {
  padding: 0.25rem 0.75rem;
  background: #E5E7EB;
  color: #374151;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.rec-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 0.75rem;
}

.rec-description {
  font-size: 0.875rem;
  color: #6B7280;
  margin-bottom: 1.25rem;
  line-height: 1.5;
}

.rec-metrics {
  display: flex;
  gap: 2rem;
}

.metric {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.metric-label {
  font-size: 0.75rem;
  color: #9CA3AF;
  font-weight: 500;
}

.metric-value {
  font-size: 0.875rem;
  color: #1A1A1A;
  font-weight: 600;
}
</style>
