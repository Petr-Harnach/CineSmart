<template>
  <div class="bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-200 min-h-screen transition-colors duration-300">
    <TheNavbar />
    
    <!-- Backend Wake Up Notification -->
    <transition
      enter-active-class="transform transition ease-out duration-300"
      enter-from-class="-translate-y-full"
      enter-to-class="translate-y-0"
      leave-active-class="transform transition ease-in duration-200"
      leave-from-class="translate-y-0"
      leave-to-class="-translate-y-full"
    >
      <div v-if="isBackendWakingUp" class="fixed top-16 left-0 right-0 z-[100] flex justify-center px-4">
        <div class="bg-blue-600 text-white px-6 py-2 rounded-b-xl shadow-2xl flex items-center gap-3 text-sm font-bold animate-pulse">
          <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
          Probouzíme servery, strpení prosím...
        </div>
      </div>
    </transition>

    <main class="py-8">
      <NuxtPage />
    </main>
    <TheFooter />
    
    <!-- Auth Modal - globally available -->
    <AuthModal :is-open="isAuthModalOpen" :initial-view="authModalView" @close="closeAuthModal" />
  </div>
</template>

<script setup>
import { ref, provide } from 'vue';
import { isBackendWakingUp } from './composables/useApi';

const isAuthModalOpen = ref(false);
const authModalView = ref('login'); // 'login' or 'register'

const openAuthModal = (view = 'login') => {
  authModalView.value = view;
  isAuthModalOpen.value = true;
};

const closeAuthModal = () => {
  isAuthModalOpen.value = false;
};

// Make the openAuthModal function available to all child components
provide('openAuthModal', openAuthModal);

useHead({
  titleTemplate: (titleChunk) => {
    return titleChunk ? `${titleChunk} - CineSmart` : 'CineSmart';
  },
  bodyAttrs: {
    class: 'bg-gray-100 dark:bg-gray-900' // Ensure body has a base color
  }
});
</script>
