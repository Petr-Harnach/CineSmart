<template>
  <div>
    <h1 class="text-2xl font-bold mb-4">Movie List</h1>
    
    <div v-if="loading" class="text-gray-500">Loading movies...</div>
    
    <div v-else-if="error" class="text-red-500">Failed to load movies: {{ error.message }}</div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <div v-for="movie in movies" :key="movie.id" class="bg-white p-4 rounded-lg shadow">
        <h2 class="text-lg font-semibold">{{ movie.title }}</h2>
        <p class="text-gray-600 text-sm">{{ movie.release_date }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useApi } from '../composables/useApi';

const { getMovies } = useApi();
const movies = ref([]);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const response = await getMovies();
    movies.value = response.data.results; // Assuming pagination from DRF
  } catch (err) {
    error.value = err;
    console.error('Error fetching movies:', err);
  } finally {
    loading.value = false;
  }
});
</script>
