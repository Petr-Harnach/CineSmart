<template>
  <div>
    <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
      <!-- Left Column: Filters -->
      <aside class="md:col-span-1 bg-gray-50 dark:bg-gray-800/50 p-6 rounded-xl shadow-lg h-fit sticky top-4">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold text-gray-800 dark:text-white">Filters</h2>
          <button @click="resetFilters" class="text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-200 transition-colors">Reset</button>
        </div>
        
        <div class="space-y-6">
          <!-- SEARCH -->
          <div>
            <label class="block text-sm font-semibold text-gray-600 dark:text-gray-300 mb-1">Search</label>
            <input
              type="text"
              v-model="filters.search"
              placeholder="Movie title..."
              class="w-full mt-1 p-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm bg-white dark:bg-gray-700 dark:text-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
            />
          </div>
          <!-- TYPE -->
          <div>
            <label class="block text-sm font-semibold text-gray-600 dark:text-gray-300 mb-1">Type</label>
            <select v-model="filters.type" class="w-full mt-1 p-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm bg-white dark:bg-gray-700 dark:text-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition">
              <option :value="null">All</option>
              <option value="movie">Movies</option>
              <option value="series">Series</option>
            </select>
          </div>
          <!-- GENRE -->
          <div>
            <label class="block text-sm font-semibold text-gray-600 dark:text-gray-300 mb-1">Genre</label>
            <div class="mt-1 grid grid-cols-2 gap-2 text-sm max-h-48 overflow-y-auto p-2 bg-white dark:bg-gray-700 rounded-md border border-gray-300 dark:border-gray-600">
              <div v-for="genre in genres" :key="genre.id" class="flex items-center">
                <input type="checkbox" :id="`genre-${genre.id}`" :value="genre.id" v-model="selectedGenres" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-offset-gray-800 transition">
                <label :for="`genre-${genre.id}`" class="ml-2 text-gray-700 dark:text-gray-200 select-none">{{ genre.name }}</label>
              </div>
            </div>
          </div>
          <!-- YEAR -->
          <div>
            <label class="block text-sm font-semibold text-gray-600 dark:text-gray-300 mb-1">Year</label>
            <div class="flex items-center gap-2 mt-1">
              <input type="number" v-model="filters.release_date__year__gte" placeholder="From" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm bg-white dark:bg-gray-700 dark:text-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition">
              <span class="text-gray-500">-</span>
              <input type="number" v-model="filters.release_date__year__lte" placeholder="To" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm bg-white dark:bg-gray-700 dark:text-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition">
            </div>
          </div>
          <!-- SORT -->
          <div>
            <label class="block text-sm font-semibold text-gray-600 dark:text-gray-300 mb-1">Sort by</label>
            <select v-model="filters.ordering" class="w-full mt-1 p-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm bg-white dark:bg-gray-700 dark:text-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition">
              <option :value="null">Default</option>
              <option value="-avg_rating">Top Rated</option>
              <option value="title">Title (A-Z)</option>
              <option value="-title">Title (Z-A)</option>
              <option value="-release_date">Newest First</option>
              <option value="release_date">Oldest First</option>
            </select>
          </div>
        </div>
      </aside>

      <!-- Right Column: Movie Grid -->
      <main class="md:col-span-3">
        <div v-if="loading" class="text-center text-gray-500"><p>Loading movies...</p></div>
        <div v-else-if="error" class="text-center text-red-500"><p>Failed to load movies: {{ error.message }}</p></div>
        <div v-else-if="movies.length === 0" class="text-center text-gray-600 dark:text-gray-400"><p>No movies found matching your criteria.</p></div>
        <div v-else>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <div 
              v-for="movie in movies" 
              :key="movie.id" 
              class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer" 
              @click="goToMovie(movie.id)"
            >
              <div class="aspect-w-2 aspect-h-3"> <!-- Typical poster aspect ratio (2:3) -->
                <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" class="object-cover w-full h-full">
                <div v-else class="bg-gray-300 dark:bg-gray-700 flex items-center justify-center text-gray-500 dark:text-gray-400">
                  No Poster
                </div>
              </div>
              <div class="p-4">
                <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100 truncate">{{ movie.title }}</h2>
                <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">{{ movie.release_date ? movie.release_date.substring(0, 4) : 'TBA' }}</p>
              </div>
            </div>
          </div>
          <!-- Pagination -->
          <div class="flex justify-center mt-8 space-x-4">
            <button @click="goToPrevPage" :disabled="!prevPageUrl" class="px-4 py-2 bg-blue-600 text-white rounded disabled:bg-blue-300 dark:bg-blue-700 dark:disabled:bg-blue-900 hover:bg-blue-700 dark:hover:bg-blue-600">Previous</button>
            <button @click="goToNextPage" :disabled="!nextPageUrl" class="px-4 py-2 bg-blue-600 text-white rounded disabled:bg-blue-300 dark:bg-blue-700 dark:disabled:bg-blue-900 hover:bg-blue-700 dark:hover:bg-blue-600">Next</button>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, watch, computed } from 'vue';
import { useApi } from '../composables/useApi';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();
const { getMovies, getGenres } = useApi();

const movies = ref([]);
const loading = ref(true);
const error = ref(null);
const nextPageUrl = ref(null);
const prevPageUrl = ref(null);
const genres = ref([]);
const selectedGenres = ref([]);

const filters = reactive({
  search: '',
  type: null,
  genres: computed(() => selectedGenres.value), // Propojení s checkboxy
  ordering: null,
  release_date__year__gte: null,
  release_date__year__lte: null,
});

const resetFilters = () => {
  filters.search = '';
  filters.type = null;
  filters.ordering = null;
  filters.release_date__year__gte = null;
  filters.release_date__year__lte = null;
  selectedGenres.value = [];
  
  // Clear URL params
  router.push({ query: {} });
};

let debounceTimer = null;

const fetchMovies = async (urlOrParams) => {
  loading.value = true;
  error.value = null;
  try {
    const response = typeof urlOrParams === 'string' 
      ? await getMovies(urlOrParams)
      : await getMovies(urlOrParams);
      
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

const goToNextPage = () => nextPageUrl.value && fetchMovies(nextPageUrl.value);
const goToPrevPage = () => prevPageUrl.value && fetchMovies(prevPageUrl.value);

const goToMovie = (id) => {
  router.push(`/movies/${id}`);
};

watch(filters, (newFilters) => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    // Odstranění prázdných hodnot
    const cleanFilters = Object.fromEntries(
      Object.entries(newFilters).filter(([, value]) => {
        if (Array.isArray(value)) return value.length > 0;
        return value !== null && value !== '';
      })
    );
    
    // Update URL query params without reloading
    router.replace({ query: { ...route.query, ...cleanFilters } });
    
    fetchMovies(cleanFilters);
  }, 500); // 500ms prodleva
}, { deep: true });

onMounted(() => {
  fetchGenres();
  
  // Load filters from URL query
  if (route.query.search) filters.search = route.query.search;
  // (Add logic for other filters if needed from URL)
  
  fetchMovies(filters);
});
</script>