<template>
  <div class="bg-gray-100 dark:bg-gray-900 min-h-screen flex flex-col">
    <TheNavbar 
      @navigate="navigateTo" 
      @filter-change="handleFilterChange" 
      @show-detail="showMovieDetail"
      :show-filters="currentPage === 'home'" 
    />
    <main class="container mx-auto p-4 flex-grow">
      <PageHome 
        v-if="currentPage === 'home'" 
        @show-detail="showMovieDetail"
        @show-actor-detail="showActorDetail" 
        :filters="activeFilters" 
        @navigate="navigateTo"
      />
      <PageLogin v-else-if="currentPage === 'login'" @navigate="navigateTo" />
      <PageRegister v-else-if="currentPage === 'register'" @navigate="navigateTo" />
      <PageMovieDetail 
        v-else-if="currentPage === 'movie-detail'" 
        :movie-id="selectedMovieId" 
        @navigate="navigateTo" 
        @show-actor-detail="showActorDetail"
        @show-detail="showMovieDetail"
      />
      <PageActorDetail 
        v-else-if="currentPage === 'actor-detail'"
        :actor-id="selectedActorId"
        @navigate="navigateTo"
        @show-detail="showMovieDetail"
      />
      <PageWatchlist 
        v-else-if="currentPage === 'watchlist'" 
        @navigate="navigateTo" 
        @show-detail="showMovieDetail" 
      />
    </main>
    <TheFooter />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import TheNavbar from '../components/TheNavbar.vue';
import PageHome from '../components/PageHome.vue';
import PageLogin from '../components/PageLogin.vue';
import PageRegister from '../components/PageRegister.vue';
import PageMovieDetail from '../components/PageMovieDetail.vue';
import PageActorDetail from '../components/PageActorDetail.vue'; // Import
import PageWatchlist from '../components/PageWatchlist.vue';
import TheFooter from '../components/TheFooter.vue';

const currentPage = ref('home');
const selectedMovieId = ref(null);
const selectedActorId = ref(null); // Nový stav
const activeFilters = ref({});

const navigateTo = (page) => {
  currentPage.value = page;
  selectedMovieId.value = null; 
  selectedActorId.value = null;
};

const showMovieDetail = (id) => {
  selectedMovieId.value = id;
  currentPage.value = 'movie-detail';
};

const showActorDetail = (id) => { // Nová funkce
  selectedActorId.value = id;
  currentPage.value = 'actor-detail';
};

const handleFilterChange = (filters) => {
  activeFilters.value = filters;
};
</script>
