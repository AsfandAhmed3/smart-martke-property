<template>
  <div class="documents-page">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Documents</h1>
        <p class="page-subtitle">Manage property documents and files</p>
      </div>
      <button class="btn-primary">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        Upload Document
      </button>
    </div>

    <!-- Document Stats -->
    <div class="stats-grid">
      <div class="stat-card">
        <svg class="stat-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2">
          <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <div>
          <h3 class="stat-value">{{ stats.total_documents }}</h3>
          <p class="stat-label">Total Documents</p>
        </div>
      </div>
      <div class="stat-card">
        <svg class="stat-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2">
          <path d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
        </svg>
        <div>
          <h3 class="stat-value">{{ stats.total_folders }}</h3>
          <p class="stat-label">Folders</p>
        </div>
      </div>
      <div class="stat-card">
        <svg class="stat-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2">
          <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
        </svg>
        <div>
          <h3 class="stat-value">{{ stats.storage_used }}</h3>
          <p class="stat-label">Storage Used</p>
        </div>
      </div>
    </div>

    <!-- Folders -->
    <div class="folders-section">
      <h2 class="section-title">Folders</h2>
      <div v-if="!loading && folders.length > 0" class="folders-grid">
        <div v-for="folder in folders" :key="folder.id" class="folder-card">
          <svg class="folder-icon" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
          </svg>
          <h3 class="folder-name">{{ folder.name }}</h3>
          <p class="folder-count">{{ folder.document_count || 0 }} files</p>
        </div>
      </div>
      <div v-else-if="loading" class="loading-state">
        <p>Loading folders...</p>
      </div>
      <div v-else class="empty-state">
        <p>No folders found</p>
      </div>
    </div>

    <!-- Recent Documents -->
    <div class="documents-section">
      <h2 class="section-title">Recent Documents</h2>
      <div v-if="!loading && documents.length > 0" class="documents-list">
        <div v-for="doc in documents" :key="doc.id" class="document-row">
          <div class="doc-icon" :style="{ background: '#E0E7FF' }">
            {{ getFileType(doc.file_name) }}
          </div>
          <div class="doc-info">
            <h4 class="doc-name">{{ doc.file_name }}</h4>
            <p class="doc-meta">{{ formatFileSize(doc.file_size) }} • {{ formatDate(doc.uploaded_at) }}</p>
          </div>
          <div class="doc-actions">
            <button class="action-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
            </button>
            <button class="action-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      <div v-else-if="loading" class="loading-state">
        <p>Loading documents...</p>
      </div>
      <div v-else class="empty-state">
        <p>No documents found</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';

const folders = ref([]);
const documents = ref([]);
const stats = ref({
  total_documents: 0,
  total_folders: 0,
  storage_used: '0 GB'
});
const loading = ref(true);

const fetchFolders = async () => {
  try {
    const response = await api.getFolders();
    folders.value = Array.isArray(response.data) ? response.data : (response.data.results || []);
  } catch (error) {
    console.error('Failed to fetch folders:', error);
    folders.value = [];
  }
};

const fetchDocuments = async () => {
  try {
    const response = await api.getDocuments({ limit: 10 });
    documents.value = Array.isArray(response.data) ? response.data : (response.data.results || []);
  } catch (error) {
    console.error('Failed to fetch documents:', error);
    documents.value = [];
  }
};

const fetchDocumentStats = async () => {
  try {
    const response = await api.getDocumentStatistics();
    const totalSize = response.data.total_size || 0;
    const sizeInGB = (totalSize / (1024 * 1024 * 1024)).toFixed(1);
    
    stats.value = {
      total_documents: response.data.total_documents || 0,
      total_folders: response.data.total_folders || 0,
      storage_used: `${sizeInGB} GB`
    };
  } catch (error) {
    console.error('Failed to fetch document stats:', error);
  }
};

const formatDate = (date) => {
  if (!date) return '';
  return new Date(date).toLocaleDateString();
};

const formatFileSize = (bytes) => {
  if (!bytes) return '0 KB';
  const kb = bytes / 1024;
  if (kb < 1024) return `${kb.toFixed(1)} KB`;
  const mb = kb / 1024;
  return `${mb.toFixed(1)} MB`;
};

const getFileType = (filename) => {
  if (!filename) return 'DOC';
  const ext = filename.split('.').pop().toUpperCase();
  return ext.substring(0, 3);
};

onMounted(async () => {
  loading.value = true;
  await Promise.all([
    fetchFolders(),
    fetchDocuments(),
    fetchDocumentStats()
  ]);
  loading.value = false;
});
</script>

<style scoped>
.documents-page {
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
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 0.75rem;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  flex-shrink: 0;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1A1A1A;
}

.stat-label {
  font-size: 0.875rem;
  color: #6B7280;
}

.folders-section, .documents-section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 1.5rem;
}

.folders-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

.folder-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 0.75rem;
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.folder-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

.folder-icon {
  color: #7C6FDC;
  margin-bottom: 1rem;
}

.folder-name {
  font-size: 1rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 0.25rem;
}

.folder-count {
  font-size: 0.875rem;
  color: #6B7280;
}

.documents-list {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 0.75rem;
  overflow: hidden;
}

.document-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #E5E7EB;
  transition: all 0.2s;
}

.document-row:last-child {
  border-bottom: none;
}

.document-row:hover {
  background: #F9FAFB;
}

.doc-icon {
  width: 40px;
  height: 40px;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  color: #374151;
  flex-shrink: 0;
}

.doc-info {
  flex: 1;
}

.doc-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 0.25rem;
}

.doc-meta {
  font-size: 0.75rem;
  color: #6B7280;
}

.doc-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.5rem;
  background: none;
  border: 1px solid #D1D5DB;
  border-radius: 0.375rem;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #F3F4F6;
  color: #374151;
}
</style>
