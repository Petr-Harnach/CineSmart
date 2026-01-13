<template>
  <div class="bg-gray-100 dark:bg-gray-900 min-h-screen flex flex-col">
    <TheNavbar />
    <main class="container mx-auto p-4 flex-grow">
      <NuxtPage />

      <!-- Auth Modal (Global) -->
      <AuthModal 
        :is-open="isAuthModalOpen" 
        :initial-view="authModalView"
        @close="closeAuthModal"
        @forgot-password="router.push('/forgot-password')" 
      />
    </main>
    <TheFooter />
  </div>
</template>

<script setup>
import { ref, onMounted, provide } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from './stores/auth'; // Import store
import TheNavbar from './components/TheNavbar.vue';
import TheFooter from './components/TheFooter.vue';
import AuthModal from './components/AuthModal.vue';

const router = useRouter();
const authStore = useAuthStore(); // Use store

// Global Auth Modal State
const isAuthModalOpen = ref(false);
const authModalView = ref('login');

const openAuthModal = (view = 'login') => {
  authModalView.value = view;
  isAuthModalOpen.value = true;
};

const closeAuthModal = () => {
  isAuthModalOpen.value = false;
};

// Provide the openAuthModal function to all descendants
provide('openAuthModal', openAuthModal);

onMounted(() => {
  authStore.initialize(); // Initialize auth state
});
</script>