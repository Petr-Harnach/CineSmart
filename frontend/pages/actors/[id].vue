<template>
  <div v-if="loading" class="text-center text-gray-500 py-12">
    <p>Načítám detaily herce...</p>
  </div>
  <div v-else-if="error" class="text-center text-red-500 py-12">
    <p>Nepodařilo se načíst detaily herce: {{ error.message }}</p>
  </div>
  <div v-else-if="actor" class="max-w-6xl mx-auto mt-10 p-4">
    <!-- Hlavní karta s informacemi o herci -->
    <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="flex flex-col md:flex-row gap-6 md:gap-8 p-6">
        <!-- Fotka herce -->
        <div class="flex-shrink-0 w-48 mx-auto md:mx-0">
          <div class="aspect-[2/3] rounded-lg overflow-hidden shadow-md bg-gray-200 dark:bg-gray-700">
            <img v-if="actor.photo" :src="actor.photo" :alt="actor.name" class="w-full h-full object-cover">
            <div v-else class="w-full h-full flex items-center justify-center text-gray-500">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
            </div>
          </div>
        </div>
        
        <!-- Detaily herce -->
        <div class="flex-grow text-center md:text-left">
          <h1 class="text-4xl font-bold text-gray-800 dark:text-gray-100 mb-4">{{ actor.name }}</h1>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-3 text-sm mt-4 border-t border-gray-200 dark:border-gray-700 pt-4">
            <div>
              <span class="font-semibold text-gray-500 dark:text-gray-400 block mb-1">Role</span>
              <span class="text-gray-900 dark:text-white font-medium">Herec</span>
            </div>
            <div v-if="actor.birth_date">
              <span class="font-semibold text-gray-500 dark:text-gray-400 block mb-1">Narozen</span>
              <span class="text-gray-900 dark:text-white font-medium">{{ new Date(actor.birth_date).toLocaleDateString() }}</span>
            </div>
            <div v-if="actor.birth_place">
              <span class="font-semibold text-gray-500 dark:text-gray-400 block mb-1">Místo narození</span>
              <span class="text-gray-900 dark:text-white font-medium">{{ actor.birth_place }}</span>
            </div>
            <div>
              <span class="font-semibold text-gray-500 dark:text-gray-400 block mb-1">Počet filmů/seriálů</span>
              <span class="text-gray-900 dark:text-white font-medium">{{ actor.movies.length }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <hr class="my-8 border-transparent">

    <!-- Přepínač filmografie -->
    <div class="flex justify-center gap-2 mb-8">
      <button 
        @click="selectedFilmographyType = 'movie'" 
        class="px-5 py-2 rounded-full font-medium transition-colors"
        :class="selectedFilmographyType === 'movie' ? 'bg-blue-600 text-white shadow' : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'"
      >
        Filmy ({{ moviesCount }})
      </button>
      <button 
        @click="selectedFilmographyType = 'series'" 
        class="px-5 py-2 rounded-full font-medium transition-colors"
        :class="selectedFilmographyType === 'series' ? 'bg-blue-600 text-white shadow' : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'"
      >
        Seriály ({{ seriesCount }})
      </button>
    </div>

    <!-- Mřížka filmografie -->
    <div>
      <div v-if="filteredFilmography.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div 
          v-for="movie in filteredFilmography" 
          :key="movie.id" 
          class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer group"
          @click="goToDetail(movie)"
        >
          <div class="relative aspect-[2/3] overflow-hidden">
            <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500">
            <div v-else class="w-full h-full bg-gray-300 dark:bg-gray-700 flex items-center justify-center text-gray-500">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
            </div>
            
            <!-- Štítky na plakátu -->
            <div v-if="movie.release_date" class="absolute top-2 left-2 text-white bg-black/70 px-2 py-0.5 rounded-full text-xs font-bold">{{ movie.release_date.substring(0, 4) }}</div>
            <div v-if="movie.avg_rating" class="absolute top-2 right-2 text-white bg-yellow-600 px-2 py-0.5 rounded-full text-xs font-bold flex items-center gap-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" /></svg>
              {{ movie.avg_rating.toFixed(1) }}
            </div>
          </div>
          <div class="p-3">
            <h3 class="text-sm font-semibold text-gray-900 dark:text-gray-100 truncate">{{ movie.title }}</h3>
          </div>
        </div>
      </div>
      <p v-else class="text-center text-gray-500 italic py-8">Pro tento výběr nebyly nalezeny žádné tituly.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { useApi } from '../../composables/useApi';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const actorId = route.params.id;

const { getActorById } = useApi();

const actor = ref(null);
const loading = ref(true);
const error = ref(null);
const selectedFilmographyType = ref('movie'); // 'movie' or 'series'

const fetchActor = async (id) => {
  loading.value = true;
  error.value = null;
  actor.value = null;
  try {
    const response = await getActorById(id);
    actor.value = response.data;
  } catch (err) {
    console.error(`Chyba při načítání herce s id ${id}:`, err);
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

const moviesCount = computed(() => actor.value?.movies.filter(m => m.type === 'movie').length || 0);
const seriesCount = computed(() => actor.value?.movies.filter(m => m.type === 'series').length || 0);

const filteredFilmography = computed(() => {
  if (!actor.value || !actor.value.movies) return [];
  return actor.value.movies.filter(movie => movie.type === selectedFilmographyType.value);
});

onMounted(() => {
  fetchActor(actorId);
});

watch(() => route.params.id, (newId) => {
  if (newId) fetchActor(newId);
});
</script>