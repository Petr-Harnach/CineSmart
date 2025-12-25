<template>
  <div class="max-w-md mx-auto mt-10">
    <h1 class="text-2xl font-bold mb-4 dark:text-gray-100">Forgot Password</h1>
    <form @submit.prevent="handleRequest" class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
      <p class="text-gray-600 dark:text-gray-300 mb-4">
        Enter your email address and we will send you a link to reset your password.
      </p>
      <div v-if="successMessage" class="bg-green-100 text-green-700 p-3 mb-4 rounded">{{ successMessage }}</div>
      <div v-if="error" class="bg-red-100 text-red-700 p-3 mb-4 rounded">{{ error }}</div>
      
      <div class="mb-4">
        <label for="email" class="block text-gray-700 dark:text-gray-300">Email</label>
        <input 
          type="email" 
          v-model="email" 
          id="email" 
          class="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200" 
          required
        />
      </div>
      
      <button 
        type="submit" 
        :disabled="loading" 
        class="w-full bg-blue-600 text-white p-2 rounded disabled:bg-blue-300 dark:bg-blue-700 dark:disabled:bg-blue-900 hover:bg-blue-700 dark:hover:bg-blue-600"
      >
        {{ loading ? 'Sending...' : 'Send Password Reset Email' }}
      </button>
    </form>
    <p class="text-center mt-4">
      <a href="#" @click.prevent="$emit('navigate', 'login')" class="text-sm text-blue-500 hover:underline">Back to Login</a>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useApi } from '../composables/useApi';

const { requestPasswordReset } = useApi();

const email = ref('');
const loading = ref(false);
const error = ref(null);
const successMessage = ref('');

const handleRequest = async () => {
  loading.value = true;
  error.value = null;
  successMessage.value = '';
  try {
    await requestPasswordReset(email.value);
    successMessage.value = 'If an account with that email exists, we have sent password reset instructions to it.';
  } catch (err) {
    console.error('Password reset request failed:', err);
    // Zobrazíme obecnou zprávu, i když nastane chyba, abychom neprozradili, které e-maily existují
    successMessage.value = 'If an account with that email exists, we have sent password reset instructions to it.';
  } finally {
    loading.value = false;
  }
};
</script>
