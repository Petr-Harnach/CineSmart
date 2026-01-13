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
            <div v-if="isSearchFocused && (searchResults.length > 0 || isSearchLoading || searchQuery.length > 0)"
                 class="absolute top-full left-0 right-0 mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md shadow-lg z-20">
              <div v-if="isSearchLoading" class="p-4 text-gray-500">Loading...</div>
              <div v-else-if="searchResults.length === 0 && searchQuery.length > 0" class="p-4 text-gray-500">No results found.</div>
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
            title="Random Pick"
            class="p-3 border rounded-md text-sm bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-600 transition"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v14a1 1 0 01-1 1H5a1 1 0 01-1-1V5z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 9h.01M15 9h.01M9 15h.01M15 15h.01M12 12h.01" />
            </svg>
          </button>

          <!-- Filters Button -->
          <div class="relative">
            <button 
              @click="toggleFilterMenu"
              class="w-full md:w-auto p-3 border rounded-md text-sm bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200 flex items-center justify-center gap-2"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 4h13M3 8h9M3 12h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
              </svg>
              <span>Filters</span>
            </button>

            <!-- Filter Menu (Dropdown logic remains same, but applyFilters navigates) -->
            <div 
              v-if="isFilterMenuOpen"
              class="absolute top-full left-0 md:left-auto md:right-0 mt-2 w-full md:w-80 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md shadow-lg z-20 p-4"
            >
              <div class="space-y-4">
                <!-- TYPE -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Type</label>
                  <select
                    v-model="selectedType"
                    class="w-full mt-1 p-2 border rounded-md text-sm bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200"
                  >
                    <option value="">All</option>
                    <option value="movie">Movies</option>
                    <option value="series">Series</option>
                  </select>
                </div>

                <!-- GENRE -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Genre</label>
                  <select
                    v-model="selectedGenre"
                    class="w-full mt-1 p-2 border rounded-md text-sm bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200"
                  >
                    <option value="">All</option>
                    <option v-for="genre in genres" :key="genre.id" :value="genre.id">
                      {{ genre.name }}
                    </option>
                  </select>
                </div>

                <!-- YEAR -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Year</label>
                  <div class="flex items-center gap-2 mt-1">
                    <input 
                      type="number" 
                      v-model="yearFrom" 
                      placeholder="From" 
                      class="w-full p-2 border rounded-md text-sm bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200"
                    >
                    <span class="text-gray-500">-</span>
                    <input 
                      type="number" 
                      v-model="yearTo" 
                      placeholder="To"
                      class="w-full p-2 border rounded-md text-sm bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200"
                    >
                  </div>
                </div>

                <!-- SORT -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Sort by</label>
                  <select
                    v-model="selectedSort"
                    class="w-full mt-1 p-2 border rounded-md text-sm bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200"
                  >
                    <option value="">Default</option>
                    <option value="-avg_rating">Top Rated</option>
                    <option value="title">Title (A-Z)</option>
                    <option value="-title">Title (Z-A)</option>
                    <option value="-release_date">Newest First</option>
                    <option value="release_date">Oldest First</option>
                  </select>
                </div>
              </div>

              <!-- Actions -->
              <div class="flex justify-end gap-3 mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
                <button @click="resetFilters" class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 bg-gray-100 dark:bg-gray-600 rounded-md hover:bg-gray-200 dark:hover:bg-gray-500">
                  Reset
                </button>
                <button @click="applyFilters" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700">
                  Apply Filters
                </button>
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- RIGHT: AUTH / THEME -->
      <div class="flex items-center space-x-4 flex-shrink-0">
        <template v-if="!authStore.isLoggedIn">
          <a @click.prevent="openAuthModal('login')" href="#" class="text-gray-300 hover:text-white">
            Login
          </a>
          <a @click.prevent="openAuthModal('register')" href="#" class="text-gray-300 hover:text-white">
            Register
          </a>
        </template>

        <template v-else>
          <NuxtLink to="/watchlist" class="text-gray-300 hover:text-white">
            Watchlist
          </NuxtLink>
          <NuxtLink to="/collections" class="text-gray-300 hover:text-white">
            Collections
          </NuxtLink>
          <NuxtLink to="/profile" class="flex items-center gap-2 text-white cursor-pointer">
            <img 
              v-if="authStore.user && authStore.user.profile_picture" 
              :src="authStore.user.profile_picture" 
              alt="Profile" 
              class="h-8 w-8 rounded-full object-cover"
            >
            <span v-if="authStore.user">
              {{ authStore.user.username }}
            </span>
          </NuxtLink>
          <a
            @click.prevent="handleLogout"
            href="#"
            class="text-gray-300 hover:text-red-500 transition-colors"
            title="Logout"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </a>
        </template>

        <!-- THEME TOGGLE -->
        <button @click="toggleTheme" class="text-gray-300 hover:text-white transition-colors" title="Toggle Theme">
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
const { getGenres, getMovies, getRandomMovieId } = useApi();
const openAuthModal = inject('openAuthModal');

// Stavy pro filtry
const searchQuery = ref('');
const selectedGenre = ref('');
const selectedSort = ref('');
const selectedType = ref('');
const yearFrom = ref(null);
const yearTo = ref(null);
const genres = ref([]);

// Stavy pro našeptávač
const searchResults = ref([]);
const isSearchLoading = ref(false);
const isSearchFocused = ref(false);
let debounceTimer = null;

// Stav pro nové menu s filtry
const isFilterMenuOpen = ref(false);

const toggleTheme = () => {
  colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark';
};

const toggleFilterMenu = () => {
  isFilterMenuOpen.value = !isFilterMenuOpen.value;
};

const applyFilters = () => {
  const params = {};
  if (searchQuery.value) params.search = searchQuery.value;
  if (selectedGenre.value) params.genres = selectedGenre.value;
  if (selectedSort.value) params.ordering = selectedSort.value;
  if (selectedType.value) params.type = selectedType.value;
  if (yearFrom.value) params.release_date__year__gte = yearFrom.value;
  if (yearTo.value) params.release_date__year__lte = yearTo.value;

  isFilterMenuOpen.value = false;
  router.push({ path: '/browse', query: params });
};

const resetFilters = () => {
  selectedGenre.value = '';
  selectedSort.value = '';
  selectedType.value = '';
  yearFrom.value = null;
  yearTo.value = null;
  // Ne-resetujeme searchQuery, pokud chceme zachovat kontext, ale zde asi ano?
  // searchResults resetujeme.
  applyFilters(); // Aplikovat resetované filtry
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

const fetchGenres = async () => {
  try {
    const response = await getGenres();
    genres.value = response.data.results;
  } catch (err) {
    console.error('Error fetching genres:', err);
  }
};

onMounted(() => {
  fetchGenres();
});
</script>