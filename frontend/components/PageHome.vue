<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800 dark:text-gray-100">Featured Movies</h1>
    </div>

    <!-- Filter and Search Bar -->
    <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md mb-6 flex items-center space-x-4">
      <form @submit.prevent="handleFilterChange" class="flex-grow">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search for a movie..."
          class="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200"
        />
      </form>
      <select v-model="selectedGenre" @change="handleFilterChange" class="appearance-none w-full md:w-auto p-2 pr-8 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200" style="background-image: url('data:image/svg+xml;charset=UTF-8,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 fill=%27none%27 viewBox=%270 0 20 20%27%3e%3cpath stroke=%27%236b7280%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%271.5%27 d=%27m6 8 4 4 4-4%27/%3e%3c/svg%3e'); background-position: right 0.5rem center; background-repeat: no-repeat; background-size: 1.5em 1.5em;">
        <option value="">All Genres</option>
        <option v-for="genre in genres" :key="genre.id" :value="genre.id">
          {{ genre.name }}
        </option>
      </select>
      <select v-model="selectedSort" @change="handleFilterChange" class="appearance-none w-full md:w-auto p-2 pr-8 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200" style="background-image: url('data:image/svg+xml;charset=UTF-8,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 fill=%27none%27 viewBox=%270 0 20 20%27%3e%3cpath stroke=%27%236b7280%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%271.5%27 d=%27m6 8 4 4 4-4%27/%3e%3c/svg%3e'); background-position: right 0.5rem center; background-repeat: no-repeat; background-size: 1.5em 1.5em;">
        <option value="">Sort by</option>
        <option value="title">Title (A-Z)</option>
        <option value="-title">Title (Z-A)</option>
        <option value="-release_date">Newest First</option>
        <option value="release_date">Oldest First</option>
      </select>
    </div>
    
    <div v-if="loading" class="text-center text-gray-500">
      <p>Loading movies...</p>
    </div>
    
    <div v-else-if="error" class="text-center text-red-500">
      <p>Failed to load movies: {{ error.message }}</p>
    </div>

    <div v-else-if="movies.length === 0" class="text-center text-gray-600 dark:text-gray-400">
      <p>No movies found matching your criteria.</p>
    </div>

    <div v-else>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div 
          v-for="movie in movies" 
          :key="movie.id" 
          class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer"
          @click="showMovieDetail(movie.id)"
        >
          <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" class="h-64 w-full object-cover">
          <div v-else class="bg-gray-300 dark:bg-gray-700 h-64 w-full"></div>
          
          <div class="p-4">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100 truncate">{{ movie.title }}</h2>
            <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">{{ movie.release_date.substring(0, 4) }}</p>
          </div>
        </div>
      </div>

      <div class="flex justify-center mt-8 space-x-4">
        <button 
          @click="goToPrevPage" 
          :disabled="!prevPageUrl" 
          class="px-4 py-2 bg-blue-600 text-white rounded disabled:bg-blue-300 dark:bg-blue-700 dark:disabled:bg-blue-900 hover:bg-blue-700 dark:hover:bg-blue-600"
        >
          Previous
        </button>
        <button 
          @click="goToNextPage" 
          :disabled="!nextPageUrl" 
          class="px-4 py-2 bg-blue-600 text-white rounded disabled:bg-blue-300 dark:bg-blue-700 dark:disabled:bg-blue-900 hover:bg-blue-700 dark:hover:bg-blue-600"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useApi } from '../composables/useApi';

const emit = defineEmits(['show-detail']);

const { getMovies, getGenres } = useApi();
const movies = ref([]);
const genres = ref([]);
const loading = ref(true);
const error = ref(null);
const nextPageUrl = ref(null);
const prevPageUrl = ref(null);

const searchQuery = ref('');
const selectedGenre = ref('');
const selectedSort = ref('');

const fetchMovies = async (urlOrParams) => {
  loading.value = true;
  error.value = null;
  try {
    const response = await getMovies(urlOrParams);
    movies.value = response.data.results;
    nextPageUrl.value = response.data.next;
    prevPageUrl.value = response.data.previous;
  } catch (err) {
    error.value = err;
    console.error('Error fetching movies:', err);
  } finally {
    loading.value = false;
  }
};

const fetchGenres = async () => {
  try {
    const response = await getGenres();
    genres.value = response.data.results;
  } catch (err) {
    console.error('Error fetching genres:', err);
  }
};

const handleFilterChange = () => {
  const params = {};
  if (searchQuery.value) {
    params.search = searchQuery.value;
  }
  if (selectedGenre.value) {
    params.genres = selectedGenre.value;
  }
  if (selectedSort.value) {
    params.ordering = selectedSort.value;
  }
  fetchMovies(params);
};

const goToNextPage = () => {
  if (nextPageUrl.value) {
    fetchMovies(nextPageUrl.value);
  }
};

const goToPrevPage = () => {
  if (prevPageUrl.value) {
    fetchMovies(prevPageUrl.value);
  }
};

onMounted(() => {
  fetchMovies();
  fetchGenres();
});

const showMovieDetail = (movieId) => {
  emit('show-detail', movieId);
};
</script>
