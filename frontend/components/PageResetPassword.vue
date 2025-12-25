<template>
  <div class="max-w-md mx-auto mt-10">
    <h1 class="text-2xl font-bold mb-4 dark:text-gray-100">Reset Password</h1>
    <form @submit.prevent="handleReset" class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
      <div v-if="error" class="bg-red-100 text-red-700 p-3 mb-4 rounded">{{ error }}</div>
      
      <div class="mb-4">
        <label for="password" class="block text-gray-700 dark:text-gray-300">New Password</label>
        <input 
          type="password" 
          v-model="password" 
          id="password" 
          class="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200" 
          required
        />
      </div>

      <div class="mb-4">
        <label for="password-confirm" class="block text-gray-700 dark:text-gray-300">Confirm New Password</label>
        <input 
          type="password" 
          v-model="passwordConfirm" 
          id="password-confirm" 
          class="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200" 
          required
        />
      </div>
      
      <button 
        type="submit" 
        :disabled="loading" 
        class="w-full bg-blue-600 text-white p-2 rounded disabled:bg-blue-300 dark:bg-blue-700 dark:disabled:bg-blue-900 hover:bg-blue-700 dark:hover:bg-blue-600"
      >
        {{ loading ? 'Resetting...' : 'Reset Password' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useApi } from '../composables/useApi';

const props = defineProps({
  token: {
    type: String,
    required: true,
  }
});

const emit = defineEmits(['navigate']);

const { confirmPasswordReset } = useApi();

const password = ref('');
const passwordConfirm = ref('');
const loading = ref(false);
const error = ref(null);

const handleReset = async () => {
  if (password.value !== passwordConfirm.value) {
    error.value = "Passwords do not match.";
    return;
  }

  loading.value = true;
  error.value = null;
  try {
    await confirmPasswordReset(props.token, password.value);
    emit('navigate', 'login', 'Your password has been successfully reset. Please log in.');
  } catch (err) {
    console.error('Password reset failed:', err);
    error.value = err.response?.data?.detail || 'Failed to reset password. The link might be expired or invalid.';
  } finally {
    loading.value = false;
  }
};
</script>
