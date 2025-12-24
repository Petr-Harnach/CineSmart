<template>
  <div class="max-w-6xl mx-auto mt-10">
    <h1 class="text-3xl font-bold mb-6 text-gray-800 dark:text-gray-100">My Watchlist</h1>
    
    <div v-if="loading" class="text-center text-gray-500">
      <p>Loading watchlist...</p>
    </div>
    
    <div v-else-if="error" class="text-center text-red-500">
      <p>Failed to load watchlist: {{ error.message }}</p>
    </div>

    <div v-else-if="watchlist.length === 0" class="text-center text-gray-600 dark:text-gray-400">
      <p>Your watchlist is empty. Add some movies!</p>
      <button @click="$emit('navigate', 'home')" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
        Browse Movies
      </button>
    </div>

    <div v-else>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div 
          v-for="item in watchlist" 
          :key="item.id" 
          class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer relative"
          :class="{ 'opacity-60': item.watched }"
          @click.self="$emit('show-detail', item.movie.id)"
        >
          <div v-if="item.watched" class="absolute top-2 right-2 bg-green-500 text-white text-xs font-bold px-2 py-1 rounded-full z-10">
            WATCHED
          </div>
          <img v-if="item.movie.poster" :src="item.movie.poster" :alt="item.movie.title" class="h-64 w-full object-cover" @click="$emit('show-detail', item.movie.id)">
          <div v-else class="bg-gray-300 dark:bg-gray-700 h-64 w-full" @click="$emit('show-detail', item.movie.id)"></div>
          
          <div class="p-4">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100 truncate">{{ item.movie.title }}</h2>
            <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">{{ item.movie.release_date.substring(0, 4) }}</p>
            <button @click.stop="toggleWatched(item)" class="w-full mt-2 text-sm py-1 rounded" :class="item.watched ? 'bg-gray-300 text-gray-800 dark:bg-gray-600 dark:text-gray-200' : 'bg-green-500 text-white'">
              {{ item.watched ? 'Mark as Unwatched' : 'Mark as Watched' }}
            </button>
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
import { useAuthStore } from '../stores/auth';

const emit = defineEmits(['navigate', 'show-detail']);

const { getWatchlist, updateWatchlistItem } = useApi();
const authStore = useAuthStore();
const watchlist = ref([]);
const loading = ref(true);
const error = ref(null);
const nextPageUrl = ref(null);
const prevPageUrl = ref(null);

const fetchWatchlistData = async (url = 'watchlist/') => {
  loading.value = true;
  error.value = null;
  if (!authStore.isLoggedIn) {
    error.value = new Error("You must be logged in to view your watchlist.");
    loading.value = false;
    return;
  }
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
    // Find the item in the local list and update it for immediate UI feedback
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

onMounted(() => {
  fetchWatchlistData();
});
</script>
