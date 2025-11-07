<template>
  <div class="max-w-md mx-auto mt-10">
    <h1 class="text-2xl font-bold mb-4">Login</h1>
    <form @submit.prevent="handleLogin" class="bg-white p-6 rounded-lg shadow-md">
      <div v-if="error" class="bg-red-100 text-red-700 p-3 mb-4 rounded">{{ error }}</div>
      <div class="mb-4">
        <label for="username" class="block text-gray-700">Username</label>
        <input type="text" v-model="username" id="username" class="w-full p-2 border rounded" />
      </div>
      <div class="mb-4">
        <label for="password" class="block text-gray-700">Password</label>
        <input type="password" v-model="password" id="password" class="w-full p-2 border rounded" />
      </div>
      <button type="submit" :disabled="loading" class="w-full bg-blue-500 text-white p-2 rounded disabled:bg-blue-300">
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';

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
