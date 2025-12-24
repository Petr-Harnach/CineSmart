<template>
  <nav class="bg-gray-800 dark:bg-gray-950 p-4">
    <div class="container mx-auto flex justify-between items-center">
      <a @click.prevent="$emit('navigate', 'home')" href="#" class="text-white text-lg font-bold">CineSmart</a>
      <div class="space-x-4 flex items-center">
        <a @click.prevent="$emit('navigate', 'home')" href="#" class="text-gray-300 hover:text-white">Home</a>
        
        <template v-if="!authStore.isLoggedIn">
          <a @click.prevent="$emit('navigate', 'login')" href="#" class="text-gray-300 hover:text-white">Login</a>
          <a @click.prevent="$emit('navigate', 'register')" href="#" class="text-gray-300 hover:text-white">Register</a>
        </template>
        
        <template v-else>
          <a @click.prevent="$emit('navigate', 'watchlist')" href="#" class="text-gray-300 hover:text-white">My Watchlist</a>
          <span v-if="authStore.user" class="text-white">Welcome, {{ authStore.user.username }}</span>
          <a @click.prevent="handleLogout" href="#" class="text-white hover:bg-red-700 bg-red-600 px-3 py-1 rounded">Logout</a>
        </template>

        <button @click="toggleTheme" class="text-gray-300 hover:text-white">
          <svg v-if="colorMode.value === 'light'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../stores/auth';

const colorMode = useColorMode();
const emit = defineEmits(['navigate']);
const authStore = useAuthStore();

const toggleTheme = () => {
  colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark';
};

const handleLogout = () => {
  authStore.logout();
  emit('navigate', 'home');
};
</script>