<template>
  <footer class="bg-gray-800 dark:bg-gray-950 text-white p-8 mt-12">
    <div class="container mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
      <div>
        <h3 class="text-xl font-bold mb-4">CineSmart</h3>
        <p class="text-gray-400">Nejlepší místo pro objevování filmů a seriálů na jednom místě.</p>
      </div>
      <div>
        <h4 class="text-lg font-semibold mb-4">Rychlé odkazy</h4>
        <ul class="space-y-2 text-gray-400">
          <li><NuxtLink to="/" class="hover:text-white">Domů</NuxtLink></li>
          <li><NuxtLink to="/browse" class="hover:text-white">Procházet filmy</NuxtLink></li>
          <li v-if="!isLoggedIn"><a href="#" @click.prevent="openAuthModal('login')" class="hover:text-white">Přihlásit</a></li>
        </ul>
      </div>
      <div>
        <h4 class="text-lg font-semibold mb-4">Informace</h4>
        <ul class="space-y-2 text-gray-400">
          <li><a href="#" class="hover:text-white">Ochrana soukromí</a></li>
          <li><a href="#" class="hover:text-white">Podmínky použití</a></li>
        </ul>
      </div>
    </div>
    <div class="border-t border-gray-700 mt-8 pt-8 text-center text-gray-500">
      &copy; {{ new Date().getFullYear() }} CineSmart. Všechna práva vyhrazena.
    </div>
  </footer>
</template>

<script setup>
import { inject, computed } from 'vue';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const openAuthModal = inject('openAuthModal');
const isLoggedIn = computed(() => authStore.isLoggedIn);
</script>