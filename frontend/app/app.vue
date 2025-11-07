<template>
  <div class="bg-gray-100 min-h-screen">
    <TheNavbar @navigate="navigateTo" />
    <main class="container mx-auto p-4">
      <PageHome v-if="currentPage === 'home'" />
      <PageLogin v-else-if="currentPage === 'login'" />
      <PageRegister v-else-if="currentPage === 'register'" />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import TheNavbar from '../components/TheNavbar.vue';
import PageHome from '../components/PageHome.vue';
import PageLogin from '../components/PageLogin.vue';
import PageRegister from '../components/PageRegister.vue';

const currentPage = ref('home');

const navigateTo = (page) => {
  currentPage.value = page;
};
</script>
