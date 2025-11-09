<template>
  <div>
    <h1 class="text-3xl font-bold mb-6 text-gray-800">Featured Movies</h1>
    
    <div v-if="loading" class="text-center text-gray-500">
      <p>Loading movies...</p>
    </div>
    
    <div v-else-if="error" class="text-center text-red-500">
      <p>Failed to load movies: {{ error.message }}</p>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div 
        v-for="movie in movies" 
        :key="movie.id" 
        class="bg-white rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer"
        @click="showMovieDetail(movie.id)"
      >
        <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" class="h-64 w-full object-cover">
        <div v-else class="bg-gray-300 h-64 w-full"></div>
        
        <div class="p-4">
          <h2 class="text-lg font-semibold text-gray-900 truncate">{{ movie.title }}</h2>
          <p class="text-gray-600 text-sm mt-1">{{ movie.release_date }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useApi } from '../composables/useApi';

const emit = defineEmits(['show-detail']);

const { getMovies } = useApi();
const movies = ref([]);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const response = await getMovies();
    movies.value = response.data.results;
  } catch (err) {
    error.value = err;
  } finally {
    loading.value = false;
  }
});

const showMovieDetail = (movieId) => {
  emit('show-detail', movieId);
};
</script>
