<template>
  <nav class="bg-gray-800 dark:bg-gray-950 p-4 shadow-md">
    <div class="container mx-auto flex flex-wrap items-center gap-4">

      <!-- LEFT: LOGO -->
      <NuxtLink to="/" class="text-white text-lg font-bold flex-shrink-0">
        CineSmart
      </NuxtLink>

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
                  placeholder="Hledat filmy, seriály..."
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
            <div v-if="isSearchFocused && (searchResults.length > 0 || isSearchLoading || searchQuery.length > 0)"
                 class="absolute top-full left-0 right-0 mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md shadow-lg z-20">
              <div v-if="isSearchLoading" class="p-4 text-gray-500">Načítání...</div>
              <div v-else-if="searchResults.length === 0 && searchQuery.length > 0" class="p-4 text-gray-500">Žádné výsledky.</div>
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

          <!-- Random Pick Button -->
          <button 
            @click="handleRandomPick"
            title="Zkusit štěstí"
            class="p-3 border rounded-md text-sm bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-600 transition"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v14a1 1 0 01-1 1H5a1 1 0 01-1-1V5z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 9h.01M15 9h.01M9 15h.01M15 15h.01M12 12h.01" />
            </svg>
          </button>

          <!-- Filters Button -->
          <NuxtLink 
            to="/browse"
            class="w-full md:w-auto p-3 border rounded-md text-sm bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200 flex items-center justify-center gap-2 hover:bg-gray-100 dark:hover:bg-gray-600 transition"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 4h13M3 8h9M3 12h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
            </svg>
            <span>Filtry</span>
          </NuxtLink>
        </div>
      </div>

      <!-- RIGHT: AUTH / THEME -->
      <div class="flex items-center space-x-4 flex-shrink-0">
        <template v-if="!authStore.isLoggedIn">
          <a @click.prevent="openAuthModal('login')" href="#" class="text-gray-300 hover:text-white">
            Přihlásit
          </a>
          <a @click.prevent="openAuthModal('register')" href="#" class="text-gray-300 hover:text-white">
            Registrovat
          </a>
        </template>

        <template v-else>
          <NuxtLink to="/watchlist" class="text-gray-300 hover:text-white">
            Chci vidět
          </NuxtLink>
          <NuxtLink to="/collections" class="text-gray-300 hover:text-white">
            Kolekce
          </NuxtLink>
          <NuxtLink to="/profile" class="flex items-center gap-2 text-white cursor-pointer">
            <img 
              v-if="authStore.user && authStore.user.profile_picture" 
              :src="authStore.user.profile_picture" 
              alt="Profile" 
              class="h-8 w-8 rounded-full object-cover"
            >
            <span v-if="authStore.user" class="hidden md:inline">
              {{ authStore.user.username }}
            </span>
          </NuxtLink>
          <a
            @click.prevent="handleLogout"
            href="#"
            class="text-gray-300 hover:text-red-500 transition-colors"
            title="Odhlásit se"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </a>
        </template>

        <!-- THEME TOGGLE -->
        <button @click="toggleTheme" class="text-gray-300 hover:text-white transition-colors" title="Přepnout motiv">
          <svg v-if="colorMode.value === 'dark'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707m-12.728 0l-.707-.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21 a9.003 9.003 0 008.354-5.646z" />
          </svg>
        </button>

      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, watch, inject } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useApi } from '../composables/useApi';
import { useRouter } from 'vue-router';

const colorMode = useColorMode();
const router = useRouter();
const authStore = useAuthStore();
const { getMovies, getRandomMovieId } = useApi();
const openAuthModal = inject('openAuthModal');

const searchQuery = ref('');
const searchResults = ref([]);
const isSearchLoading = ref(false);
const isSearchFocused = ref(false);
let debounceTimer = null;

const toggleTheme = () => {
  colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark';
};

const handleRandomPick = async () => {
  try {
    const randomId = await getRandomMovieId();
    if (randomId) {
      router.push(`/movies/${randomId}`);
    }
  } catch (err) {
    console.error('Error during random pick:', err);
  }
};

const handleLogout = () => {
  authStore.logout();
  router.push('/');
};

const handleFilterChange = () => {
  router.push({ path: '/browse', query: { search: searchQuery.value } });
};

watch(searchQuery, (newValue) => {
  clearTimeout(debounceTimer);
  searchResults.value = [];

  if (newValue.length > 0) {
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
  searchQuery.value = '';
  searchResults.value = [];
  isSearchFocused.value = false;
  router.push(`/movies/${movieId}`);
};
</script>