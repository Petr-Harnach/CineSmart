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
import { ref, provide } from 'vue';
import { useRouter } from 'vue-router';
// Nuxt 3 auto-imports components from components/ directory, 
// but if we keep explicit imports, we should use the correct path or alias.
// Using explicit imports with alias ~ which points to srcDir (root)
import TheNavbar from '~/components/TheNavbar.vue';
import TheFooter from '~/components/TheFooter.vue';
import AuthModal from '~/components/AuthModal.vue';

const router = useRouter();

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
</script>