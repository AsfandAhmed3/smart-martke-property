<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-container">
      <div class="modal-header">
        <h2 class="modal-title">{{ title }}</h2>
        <button @click="$emit('close')" class="close-btn">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div class="modal-body">
        <slot></slot>
      </div>
      <div class="modal-footer" v-if="cancelText !== '' || confirmText">
        <button v-if="cancelText !== ''" @click="$emit('close')" class="btn-cancel">{{ cancelText || 'Cancel' }}</button>
        <button @click="$emit('confirm')" :class="['btn-confirm', confirmType]">{{ confirmText || 'Confirm' }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  isOpen: Boolean,
  title: String,
  confirmText: String,
  cancelText: String,
  confirmType: {
    type: String,
    default: 'primary' // primary, danger
  }
});

defineEmits(['close', 'confirm']);
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
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
  max-width: 500px;
  box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.2);
  animation: slideUp 0.2s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid #E5E7EB;
}

.modal-title {
  font-size: 1.25rem;
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
  display: flex;
  align-items: center;
}

.close-btn:hover {
  color: #1A1A1A;
}

.modal-body {
  padding: 1.5rem;
  max-height: 60vh;
  overflow-y: auto;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1.5rem;
  border-top: 1px solid #E5E7EB;
}

.btn-cancel, .btn-confirm {
  padding: 0.625rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  font-size: 0.875rem;
}

.btn-cancel {
  background: #F3F4F6;
  color: #374151;
}

.btn-cancel:hover {
  background: #E5E7EB;
}

.btn-confirm.primary {
  background: #3B82F6;
  color: white;
}

.btn-confirm.primary:hover {
  background: #2563EB;
}

.btn-confirm.danger {
  background: #EF4444;
  color: white;
}

.btn-confirm.danger:hover {
  background: #DC2626;
}
</style>
