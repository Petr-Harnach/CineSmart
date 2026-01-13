<template>
  <div class="max-w-6xl mx-auto mt-10 p-4">
    <h1 class="text-3xl font-bold mb-8 text-gray-800 dark:text-gray-100">Seznam ke shlédnutí</h1>
    
    <div v-if="loading" class="text-center text-gray-500">
      <p>Načítám seznam...</p>
    </div>
    
    <div v-else-if="error" class="text-center text-red-500">
      <p>Nepodařilo se načíst seznam: {{ error.message }}</p>
    </div>

    <div v-else-if="watchlist.length === 0" class="text-center text-gray-600 dark:text-gray-400 py-12">
      <p class="text-lg">Váš seznam je prázdný. Přidejte nějaké filmy!</p>
      <NuxtLink to="/" class="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition inline-block">
        Procházet filmy
      </NuxtLink>
    </div>

    <div v-else>
      <!-- To Watch Section -->
      <section>
        <h2 class="text-2xl font-semibold mb-4 text-gray-700 dark:text-gray-200 border-b-2 border-blue-500 pb-2">
          Ke shlédnutí
          <span class="text-lg text-gray-500 dark:text-gray-400">({{ moviesToWatch.length }})</span>
        </h2>
        <div v-if="moviesToWatch.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 py-6">
          <div 
            v-for="item in moviesToWatch" 
            :key="item.id" 
            class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer relative"
            @click.self="goToMovie(item.movie.id)"
          >
            <img v-if="item.movie.poster" :src="item.movie.poster" :alt="item.movie.title" class="h-64 w-full object-cover" @click="goToMovie(item.movie.id)">
            <div v-else class="bg-gray-300 dark:bg-gray-700 h-64 w-full" @click="goToMovie(item.movie.id)"></div>
            
            <div class="p-4">
              <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100 truncate">{{ item.movie.title }}</h2>
              <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">{{ item.movie.release_date ? item.movie.release_date.substring(0, 4) : 'TBA' }}</p>
              <button @click.stop="toggleWatched(item)" class="w-full mt-2 text-sm py-2 rounded-md bg-green-500 text-white hover:bg-green-600 transition">
                Označit jako shlédnuté
              </button>
            </div>
          </div>
        </div>
        <p v-else class="text-center text-gray-500 dark:text-gray-400 py-8">Viděli jste všechny filmy ze svého seznamu!</p>
      </section>

      <!-- Divider -->
      <hr class="my-12 border-gray-200 dark:border-gray-700">

      <!-- Already Watched Section -->
      <section>
        <h2 class="text-2xl font-semibold mb-4 text-gray-700 dark:text-gray-200 border-b-2 border-gray-500 pb-2">
          Již shlédnuté
          <span class="text-lg text-gray-500 dark:text-gray-400">({{ moviesWatched.length }})</span>
        </h2>
        <div v-if="moviesWatched.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 py-6">
          <div 
            v-for="item in moviesWatched" 
            :key="item.id" 
            class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer relative"
            @click.self="goToMovie(item.movie.id)"
          >
            <img v-if="item.movie.poster" :src="item.movie.poster" :alt="item.movie.title" class="h-64 w-full object-cover" @click="goToMovie(item.movie.id)">
            <div v-else class="bg-gray-300 dark:bg-gray-700 h-64 w-full" @click="goToMovie(item.movie.id)"></div>
            
            <div class="p-4">
              <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100 truncate">{{ item.movie.title }}</h2>
              <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">{{ item.movie.release_date ? item.movie.release_date.substring(0, 4) : 'TBA' }}</p>
              <button @click.stop="toggleWatched(item)" class="w-full mt-2 text-sm py-2 rounded-md bg-gray-300 text-gray-800 dark:bg-gray-600 dark:text-gray-200 hover:bg-gray-400 dark:hover:bg-gray-500 transition">
                Označit jako neshlédnuté
              </button>
            </div>
          </div>
        </div>
        <p v-else class="text-center text-gray-500 dark:text-gray-400 py-8">Zatím jste neoznačili žádné filmy jako shlédnuté.</p>
      </section>

      <!-- Pagination -->
      <div class="flex justify-center mt-12 space-x-4">
        <button 
          @click="goToPrevPage" 
          :disabled="!prevPageUrl" 
          class="px-4 py-2 bg-blue-600 text-white rounded disabled:bg-blue-400 dark:bg-blue-700 dark:disabled:bg-blue-900 hover:bg-blue-700 dark:hover:bg-blue-600"
        >
          Předchozí
        </button>
        <button 
          @click="goToNextPage" 
          :disabled="!nextPageUrl" 
          class="px-4 py-2 bg-blue-600 text-white rounded disabled:bg-blue-400 dark:bg-blue-700 dark:disabled:bg-blue-900 hover:bg-blue-700 dark:hover:bg-blue-600"
        >
          Další
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useApi } from '../composables/useApi';
import { useAuthStore } from '../stores/auth';

const { getWatchlist, updateWatchlistItem } = useApi();
const authStore = useAuthStore();
const router = useRouter();

const watchlist = ref([]);
const loading = ref(true);
const error = ref(null);
const nextPageUrl = ref(null);
const prevPageUrl = ref(null);

const moviesToWatch = computed(() => watchlist.value.filter(item => !item.watched));
const moviesWatched = computed(() => watchlist.value.filter(item => item.watched));

const fetchWatchlistData = async (url = 'watchlist/') => {
  if (!authStore.isLoggedIn) {
    loading.value = false;
    watchlist.value = [];
    // error.value = new Error("You must be logged in to view your watchlist."); // Don't show error immediately, just empty list
    return;
  }
  
  loading.value = true;
  error.value = null;
  try {
    const response = await getWatchlist(url);
    watchlist.value = response.data.results;
    nextPageUrl.value = response.data.next;
    prevPageUrl.value = response.data.previous;
  } catch (err) {
    error.value = err;
    console.error('Error fetching watchlist:', err);
  } finally {
    loading.value = false;
  }
};

const toggleWatched = async (item) => {
  try {
    const updatedItem = await updateWatchlistItem(item.id, { watched: !item.watched });
    const index = watchlist.value.findIndex(i => i.id === item.id);
    if (index !== -1) {
      watchlist.value[index].watched = updatedItem.data.watched;
    }
  } catch (err) {
    console.error('Failed to update watched status:', err);
  }
};

const goToNextPage = () => {
  if (nextPageUrl.value) {
    fetchWatchlistData(nextPageUrl.value);
  }
};

const goToPrevPage = () => {
  if (prevPageUrl.value) {
    fetchWatchlistData(prevPageUrl.value);
  }
};

const goToMovie = (id) => {
  router.push(`/movies/${id}`);
};

onMounted(() => {
  if (authStore.isInitialized) {
    fetchWatchlistData();
  }
});

watch(() => authStore.isInitialized, (isInit) => {
  if (isInit) {
    fetchWatchlistData();
  }
});

watch(() => authStore.isLoggedIn, (isLoggedIn) => {
  if (isLoggedIn) {
    fetchWatchlistData();
  } else {
    watchlist.value = [];
  }
});
</script>