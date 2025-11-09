<template>
  <div class="bg-gray-100 min-h-screen">
    <TheNavbar @navigate="navigateTo" />
    <main class="container mx-auto p-4">
      <PageHome v-if="currentPage === 'home'" @show-detail="showMovieDetail" />
      <PageLogin v-else-if="currentPage === 'login'" @navigate="navigateTo" />
      <PageRegister v-else-if="currentPage === 'register'" @navigate="navigateTo" />
      <PageMovieDetail v-else-if="currentPage === 'movie-detail'" :movie-id="selectedMovieId" @navigate="navigateTo" />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import TheNavbar from '../components/TheNavbar.vue';
import PageHome from '../components/PageHome.vue';
import PageLogin from '../components/PageLogin.vue';
import PageRegister from '../components/PageRegister.vue';
import PageMovieDetail from '../components/PageMovieDetail.vue';

const currentPage = ref('home');
const selectedMovieId = ref(null);

const navigateTo = (page) => {
  currentPage.value = page;
  selectedMovieId.value = null; // Clear selected movie when navigating to other pages
};

const showMovieDetail = (id) => {
  selectedMovieId.value = id;
  currentPage.value = 'movie-detail';
};
</script>
