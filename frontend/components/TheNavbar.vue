<template>
  <nav class="bg-gray-800 dark:bg-gray-950 p-4 shadow-md">
    <div class="container mx-auto flex flex-wrap items-center gap-4">

      <!-- LEFT: LOGO -->
      <a
        @click.prevent="$emit('navigate', 'home')"
        href="#"
        class="text-white text-lg font-bold flex-shrink-0"
      >
        CineSmart
      </a>

      <!-- CENTER: SEARCH + FILTERS -->
      <div class="flex-1 flex justify-center">
        <div class="flex flex-col md:flex-row items-center gap-3 w-full md:flex-1">

          <!-- SEARCH -->
          <div class="relative w-full md:flex-1">
            <form @submit.prevent="handleFilterChange">
              <div class="relative">
                <input
                  type="text"
                  v-model="searchQuery"
                  placeholder="Search movies, series..."
                  class="w-full p-3 pr-12 border rounded-md text-sm
                         bg-gray-50 dark:bg-gray-700
                         dark:border-gray-600 dark:text-gray-200"
                  @focus="onSearchFocus"
                  @blur="onSearchBlur"
                  autocomplete="off"
                />
                <button
                  type="submit"
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </button>
              </div>
            </form>
            <!-- Search Results Dropdown -->
            <div v-if="isSearchFocused && (searchResults.length > 0 || isSearchLoading || searchQuery.length > 2)"
                 class="absolute top-full left-0 right-0 mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md shadow-lg z-20">
              <div v-if="isSearchLoading" class="p-4 text-gray-500">Loading...</div>
              <div v-else-if="searchResults.length === 0 && searchQuery.length > 2" class="p-4 text-gray-500">No results found.</div>
              <ul v-else>
                <li v-for="movie in searchResults" :key="movie.id" 
                    @click="selectMovie(movie.id)"
                    class="p-3 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                  <div class="flex items-center">
                    <img v-if="movie.poster" :src="movie.poster" class="h-12 w-8 object-cover rounded-sm mr-3">
                    <div v-else class="h-12 w-8 bg-gray-200 dark:bg-gray-700 rounded-sm mr-3"></div>
                    <div>
                      <p class="font-semibold text-gray-800 dark:text-gray-100">{{ movie.title }}</p>
                      <p v-if="movie.release_date" class="text-sm text-gray-500">{{ movie.release_date.substring(0, 4) }}</p>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
          </div>

          <!-- Filters Button -->
          <div class="relative">
            <button 
              @click="$emit('navigate', 'browse')"
              class="w-full md:w-auto p-3 border rounded-md text-sm bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200 flex items-center justify-center gap-2"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 4h13M3 8h9M3 12h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
              </svg>
              <span>Filters</span>
            </button>
          </div>

        </div>
      </div>

      <!-- RIGHT: AUTH / THEME -->
      <div class="flex items-center space-x-4 flex-shrink-0">
        <template v-if="!authStore.isLoggedIn">
          <a @click.prevent="$emit('navigate', 'login')" href="#" class="text-gray-300 hover:text-white">
            Login
          </a>
          <a @click.prevent="$emit('navigate', 'register')" href="#" class="text-gray-300 hover:text-white">
            Register
          </a>
        </template>

        <template v-else>
          <a @click.prevent="$emit('navigate', 'watchlist')" href="#" class="text-gray-300 hover:text-white">
            Watchlist
          </a>
          <a @click.prevent="$emit('navigate', 'profile')" href="#" class="flex items-center gap-2 text-white cursor-pointer">
            <img 
              v-if="authStore.user && authStore.user.profile_picture" 
              :src="authStore.user.profile_picture" 
              alt="Profile" 
              class="h-8 w-8 rounded-full object-cover"
            >
            <span v-if="authStore.user">
              {{ authStore.user.username }}
            </span>
          </a>
          <a
            @click.prevent="handleLogout"
            href="#"
            class="text-white bg-red-600 hover:bg-red-700 px-3 py-1 rounded"
          >
            Logout
          </a>
        </template>

        <!-- THEME TOGGLE -->
        <button @click="toggleTheme" class="text-gray-300 hover:text-white">
          <svg v-if="colorMode.value === 'light'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21 a9.003 9.003 0 008.354-5.646z" /></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707m6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
        </button>

      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useApi } from '../composables/useApi';

const colorMode = useColorMode();
const emit = defineEmits(['navigate', 'filter-change', 'show-detail']);
const authStore = useAuthStore();
const { getMovies } = useApi();

const searchQuery = ref('');
const searchResults = ref([]);
const isSearchLoading = ref(false);
const isSearchFocused = ref(false);
let debounceTimer = null;

const toggleTheme = () => {
  colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark';
};

const handleLogout = () => {
  authStore.logout();
  emit('navigate', 'home');
};

const handleFilterChange = () => {
  // Tato funkce se nyní volá jen při odeslání vyhledávacího formuláře,
  // aby se zobrazil seznam filmů na nové stránce.
  emit('navigate', 'browse');
  // Parametry se budou předávat jinak, přímo na stránce browse
  emit('filter-change', { search: searchQuery.value });
};

watch(searchQuery, (newValue) => {
  clearTimeout(debounceTimer);
  searchResults.value = [];

  if (newValue.length > 2) {
    isSearchLoading.value = true;
    debounceTimer = setTimeout(async () => {
      try {
        const response = await getMovies({ search: newValue, limit: 5 });
        searchResults.value = response.data.results;
      } catch (err) {
        console.error('Error fetching search results:', err);
      } finally {
        isSearchLoading.value = false;
      }
    }, 300);
  } else {
    isSearchLoading.value = false;
  }
});

const onSearchFocus = () => {
  isSearchFocused.value = true;
};

const onSearchBlur = () => {
  setTimeout(() => {
    isSearchFocused.value = false;
  }, 200);
};

const selectMovie = (movieId) => {
  emit('show-detail', movieId);
  searchQuery.value = '';
  searchResults.value = [];
  isSearchFocused.value = false;
};
</script>
