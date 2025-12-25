<template>
  <div class="max-w-md mx-auto mt-10">
    <h1 class="text-2xl font-bold mb-4 dark:text-gray-100">Login</h1>
    <form @submit.prevent="handleLogin" class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
      <div v-if="successMessage" class="bg-green-100 text-green-700 p-3 mb-4 rounded">{{ successMessage }}</div>
      <div v-if="error" class="bg-red-100 text-red-700 p-3 mb-4 rounded">{{ error }}</div>
      <div class="mb-4">
        <label for="username" class="block text-gray-700 dark:text-gray-300">Username</label>
        <input type="text" v-model="username" id="username" class="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200" />
      </div>
      <div class="mb-4">
        <label for="password" class="block text-gray-700 dark:text-gray-300">Password</label>
        <input type="password" v-model="password" id="password" class="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200" />
      </div>
      <button type="submit" :disabled="loading" class="w-full bg-blue-600 text-white p-2 rounded disabled:bg-blue-300 dark:bg-blue-700 dark:disabled:bg-blue-900 hover:bg-blue-700 dark:hover:bg-blue-600">
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>
    </form>
    <p class="text-center mt-4 text-gray-700 dark:text-gray-300">
      Don't have an account? 
      <a href="#" @click.prevent="$emit('navigate', 'register')" class="text-blue-500 hover:underline">Register</a>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';

const props = defineProps({
  successMessage: {
    type: String,
    default: null,
  },
});

const emit = defineEmits(['navigate']);
const authStore = useAuthStore();

const username = ref('');
const password = ref('');
const loading = ref(false);
const error = ref(null);

const handleLogin = async () => {
  loading.value = true;
  error.value = null;
  const success = await authStore.login({ username: username.value, password: password.value });
  loading.value = false;

  if (success) {
    emit('navigate', 'home');
  } else {
    error.value = 'Login failed. Please check your credentials.';
  }
};
</script>

