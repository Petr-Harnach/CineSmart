<template>
  <nav class="bg-gray-800 p-4">
    <div class="container mx-auto flex justify-between items-center">
      <a @click.prevent="$emit('navigate', 'home')" href="#" class="text-white text-lg font-bold">CineSmart</a>
      <div class="space-x-4 flex items-center">
        <a @click.prevent="$emit('navigate', 'home')" href="#" class="text-gray-300 hover:text-white">Home</a>
        
        <template v-if="!authStore.isLoggedIn">
          <a @click.prevent="$emit('navigate', 'login')" href="#" class="text-gray-300 hover:text-white">Login</a>
          <a @click.prevent="$emit('navigate', 'register')" href="#" class="text-gray-300 hover:text-white">Register</a>
        </template>
        
        <template v-else>
          <span v-if="authStore.user" class="text-white">Welcome, {{ authStore.user.username }}</span>
          <a @click.prevent="handleLogout" href="#" class="text-gray-300 hover:text-white bg-red-500 px-3 py-1 rounded">Logout</a>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../stores/auth';

const emit = defineEmits(['navigate']);
const authStore = useAuthStore();

const handleLogout = () => {
  authStore.logout();
  emit('navigate', 'home');
};
</script>