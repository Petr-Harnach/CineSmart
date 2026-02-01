<template>
  <div class="bg-gray-100 dark:bg-gray-900 pb-12">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center h-screen">
      <div class="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center text-red-500 py-24">
      <h2 class="text-2xl font-bold">Chyba</h2>
      <p>Nepodařilo se načíst detaily režiséra: {{ error.message }}</p>
    </div>

    <!-- MAIN CONTENT -->
    <div v-else-if="director" class="container mx-auto px-4 mt-8">
      
      <!-- MAIN CARD (Header) -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 md:p-8 flex flex-col md:flex-row gap-8">
        <!-- Left: Photo -->
        <div class="md:w-1/3 lg:w-1/4 flex-shrink-0">
          <div class="aspect-[2/3] rounded-xl overflow-hidden shadow-md">
            <img v-if="director.photo" :src="director.photo" :alt="director.name" class="w-full h-full object-cover">
            <div v-else class="w-full h-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-gray-400">
               <svg xmlns="http://www.w3.org/2000/svg" class="h-20 w-20" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
            </div>
          </div>
        </div>

        <!-- Right: Details -->
        <div class="flex-grow">
          <h1 class="text-4xl md:text-5xl font-black text-gray-900 dark:text-white tracking-tight">{{ director.name }}</h1>
          
          <div v-if="director.bio" class="mt-4 prose prose-sm dark:prose-invert text-gray-600 dark:text-gray-300 max-h-48 overflow-y-auto pr-2">
            <p>{{ director.bio }}</p>
          </div>
          <p v-else class="mt-4 text-gray-500 italic">Životopis není k dispozici.</p>

          <!-- Meta Info Grid -->
          <div class="mt-6 grid grid-cols-2 gap-4 text-sm border-t border-gray-200 dark:border-gray-700 pt-6">
            <div class="flex items-start gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
              <div>
                <span class="block text-xs text-gray-500">Narození</span>
                <span class="font-bold text-gray-800 dark:text-white">N/A</span>
              </div>
            </div>
            <div class="flex items-start gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4" /></svg>
              <div>
                <span class="block text-xs text-gray-500">Počet filmů</span>
                <span class="font-bold text-gray-800 dark:text-white">{{ movies.length + series.length }}</span>
              </div>
            </div>
            <div class="flex items-start gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" /></svg>
              <div>
                <span class="block text-xs text-gray-500">Známý pro</span>
                <span class="font-bold text-gray-800 dark:text-white">{{ mostFamousFor }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- FILMOGRAPHY TABS & CONTENT -->
      <div class="mt-12">
        <div class="border-b border-gray-200 dark:border-gray-700">
          <nav class="-mb-px flex space-x-6" aria-label="Tabs">
            <button @click="activeTab = 'movies'" :class="[activeTab === 'movies' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:hover:text-gray-200 dark:hover:border-gray-500', 'whitespace-nowrap py-3 px-1 border-b-2 font-medium text-lg']">
              Filmy <span class="text-xs bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded-full px-2 py-0.5 ml-1">{{ movies.length }}</span>
            </button>
            <button @click="activeTab = 'series'" :class="[activeTab === 'series' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:hover:text-gray-200 dark:hover:border-gray-500', 'whitespace-nowrap py-3 px-1 border-b-2 font-medium text-lg']">
              Seriály <span class="text-xs bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded-full px-2 py-0.5 ml-1">{{ series.length }}</span>
            </button>
          </nav>
        </div>

        <!-- Grid of movies/series -->
        <div class="mt-8 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-6">
          <div 
            v-for="item in activeContent" 
            :key="item.id" 
            class="group"
            @click="goToDetail(item)"
          >
            <div class="relative aspect-[2/3] bg-gray-200 dark:bg-gray-800 rounded-lg overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer shadow-md hover:shadow-xl">
              <img v-if="item.poster" :src="item.poster" :alt="item.title" class="w-full h-full object-cover">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <span v-if="item.release_date" class="absolute top-2 left-2 bg-black/50 text-white text-xs font-bold px-2 py-0.5 rounded backdrop-blur-sm">{{ item.release_date.substring(0, 4) }}</span>
              <div v-if="item.avg_rating" class="absolute top-2 right-2 bg-black/50 text-white text-xs font-bold px-2 py-0.5 rounded backdrop-blur-sm flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-yellow-400" viewBox="0 0 20 20" fill="currentColor"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" /></svg>
                {{ item.avg_rating.toFixed(1) }}
              </div>
            </div>
            <h3 class="mt-2 text-sm font-semibold text-gray-800 dark:text-white line-clamp-2">{{ item.title }}</h3>
          </div>
        </div>
        <p v-if="activeContent.length === 0" class="text-center text-gray-500 italic py-10">Žádné tituly k zobrazení v této kategorii.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { useApi } from '../../composables/useApi';
import { useRoute, useRouter } from 'vue-router';
import AvgRating from '../../components/AvgRating.vue'; // Potřeba pro hodnocení

const route = useRoute();
const router = useRouter();
const directorId = route.params.id;

const { getDirectorById } = useApi();

const director = ref(null);
const loading = ref(true);
const error = ref(null);
const activeTab = ref('movies');

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

const movies = computed(() => director.value?.movies.filter(m => m.type === 'movie') || []);
const series = computed(() => director.value?.movies.filter(m => m.type === 'series') || []);

const activeContent = computed(() => {
  return activeTab.value === 'movies' ? movies.value : series.value;
});

const mostFamousFor = computed(() => {
    if (!director.value?.movies || director.value.movies.length === 0) return 'N/A';
    const allGenres = director.value.movies.flatMap(m => m.genres?.map(g => g.name) || []);
    if (allGenres.length === 0) return 'N/A';

    const genreCounts = allGenres.reduce((acc, genre) => {
        acc[genre] = (acc[genre] || 0) + 1;
        return acc;
    }, {});

    return Object.keys(genreCounts).reduce((a, b) => genreCounts[a] > genreCounts[b] ? a : b);
});

onMounted(() => {
  fetchDirector(directorId);
});

watch(() => route.params.id, (newId) => {
  if (newId) fetchDirector(newId);
});
</script>