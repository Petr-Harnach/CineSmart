<template>
  <div v-if="loading" class="text-center text-gray-500 py-12">
    <p>Načítám detaily režiséra...</p>
  </div>
  <div v-else-if="error" class="text-center text-red-500 py-12">
    <p>Nepodařilo se načíst detaily režiséra: {{ error.message }}</p>
  </div>
  <div v-else-if="director" class="max-w-6xl mx-auto mt-10 p-4 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700">
    <!-- Director Header Card -->
    <div class="flex flex-col md:flex-row gap-6 p-6">
      <div class="flex-shrink-0 w-36 md:w-48">
        <img v-if="director.photo" :src="director.photo" :alt="director.name" class="w-full h-auto rounded-lg shadow-md">
        <div v-else class="w-full h-48 md:h-64 bg-gray-300 dark:bg-gray-700 rounded-lg flex items-center justify-center text-gray-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
        </div>
      </div>
      <div class="flex-grow">
        <h1 class="text-4xl font-bold text-gray-800 dark:text-gray-100 mb-4">{{ director.name }}</h1>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-2 text-sm text-gray-600 dark:text-gray-300">
          <div>
            <span class="font-semibold text-gray-900 dark:text-gray-200">Role:</span> Režisér
          </div>
          <div v-if="director.birth_date">
            <span class="font-semibold text-gray-900 dark:text-gray-200">Narozen:</span> {{ new Date(director.birth_date).toLocaleDateString() }}
          </div>
          <div v-if="director.birth_place">
            <span class="font-semibold text-gray-900 dark:text-gray-200">Místo narození:</span> {{ director.birth_place }}
          </div>
        </div>
      </div>
    </div>

    <hr class="my-8 border-gray-200 dark:border-gray-700">

    <!-- Filmography Tabs -->
    <div class="flex gap-2 mb-6">
      <button 
        @click="selectedFilmographyType = 'movie'" 
        class="px-4 py-2 rounded-lg font-medium transition-colors"
        :class="selectedFilmographyType === 'movie' 
          ? 'bg-blue-600 text-white' 
          : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'"
      >
        Filmy
      </button>
      <button 
        @click="selectedFilmographyType = 'series'" 
        class="px-4 py-2 rounded-lg font-medium transition-colors"
        :class="selectedFilmographyType === 'series' 
          ? 'bg-blue-600 text-white' 
          : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'"
      >
        Seriály
      </button>
    </div>

    <!-- Filmography Grid -->
    <div>
      <h2 class="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-100">Filmografie</h2>
      <div v-if="filteredFilmography.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div 
          v-for="movie in filteredFilmography" 
          :key="movie.id" 
          class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer group"
          @click="goToDetail(movie)"
        >
          <div class="relative aspect-[2/3] overflow-hidden">
            <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500">
            <div v-else class="w-full h-full bg-gray-300 dark:bg-gray-700 flex items-center justify-center text-gray-500">Žádný plakát</div>
            <div class="absolute top-2 right-2 text-white bg-blue-600 px-2 py-0.5 rounded-full text-xs font-bold">{{ movie.avg_rating?.toFixed(1) || 'N/A' }} ⭐</div>
            <div class="absolute top-2 left-2 text-white bg-black/60 px-2 py-0.5 rounded-full text-xs font-bold">{{ movie.release_date.substring(0, 4) }}</div>
          </div>
          <div class="p-4">
            <h3 class="text-md font-semibold text-gray-900 dark:text-gray-100 truncate">{{ movie.title }}</h3>
          </div>
        </div>
      </div>
      <p v-else class="text-center text-gray-500 italic py-8">V naší databázi nebyly nalezeny žádné {{ selectedFilmographyType === 'movie' ? 'filmy' : 'seriály' }} pro tohoto režiséra.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { useApi } from '../../composables/useApi';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const directorId = route.params.id;

const { getDirectorById } = useApi();

const director = ref(null);
const loading = ref(true);
const error = ref(null);
const selectedFilmographyType = ref('movie'); // 'movie' or 'series'

const fetchDirector = async (id) => {
  loading.value = true;
  error.value = null;
  director.value = null;
  try {
    const response = await getDirectorById(id);
    director.value = response.data;
  } catch (err) {
    console.error(`Chyba při načítání režiséra s id ${id}:`, err);
    error.value = err;
  } finally {
    loading.value = false;
  }
};

const goToDetail = (item) => {
  if (item.type === 'series') {
    router.push(`/series/${item.id}`);
  } else {
    router.push(`/movies/${item.id}`);
  }
};

const filteredFilmography = computed(() => {
  if (!director.value || !director.value.movies) return [];
  return director.value.movies.filter(movie => movie.type === selectedFilmographyType.value);
});

onMounted(() => {
  fetchDirector(directorId);
});

watch(() => route.params.id, (newId) => {
  if (newId) fetchDirector(newId);
});
</script>