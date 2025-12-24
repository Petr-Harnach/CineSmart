<template>
  <div class="max-w-md mx-auto mt-10">
    <h1 class="text-2xl font-bold mb-4 dark:text-gray-100">Register</h1>
    <form @submit.prevent="handleRegister" class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
      <div v-if="error" class="bg-red-100 text-red-700 p-3 mb-4 rounded">{{ error }}</div>
      <div class="mb-4">
        <label for="username" class="block text-gray-700 dark:text-gray-300">Username</label>
        <input type="text" v-model="username" id="username" class="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200" />
      </div>
      <div class="mb-4">
        <label for="email" class="block text-gray-700 dark:text-gray-300">Email</label>
        <input type="email" v-model="email" id="email" class="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200" />
      </div>
      <div class="mb-4">
        <label for="password" class="block text-gray-700 dark:text-gray-300">Password</label>
        <input type="password" v-model="password" id="password" class="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200" />
      </div>
      <button type="submit" :disabled="loading" class="w-full bg-green-600 text-white p-2 rounded disabled:bg-green-300 dark:bg-green-700 dark:disabled:bg-green-900 hover:bg-green-700 dark:hover:bg-green-600">
        {{ loading ? 'Registering...' : 'Register' }}
      </button>
    </form>
    <p class="text-center mt-4 text-gray-700 dark:text-gray-300">
      Already have an account? 
      <a href="#" @click.prevent="$emit('navigate', 'login')" class="text-blue-500 hover:underline">Log in</a>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';

const emit = defineEmits(['navigate']);
const authStore = useAuthStore();

const username = ref('');
const email = ref('');
const password = ref('');
const loading = ref(false);
const error = ref(null);

const handleRegister = async () => {
  loading.value = true;
  error.value = null;
  const success = await authStore.register({ 
    username: username.value, 
    email: email.value, 
    password: password.value 
  });
  loading.value = false;

  if (success) {
    emit('navigate', 'login');
  } else {
    error.value = 'Registration failed. Please try again.';
  }
};
</script>
