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

      <!-- CENTER: SEARCH + FILTERS (OPRAVDU UPROSTŘED) -->
      <div class="flex-1 flex justify-center">
        <div class="flex flex-col md:flex-row items-center gap-3 w-full md:w-auto">

          <!-- SEARCH (JEŠTĚ VĚTŠÍ) -->
          <form @submit.prevent="handleFilterChange" class="w-full md:w-[28rem]">
            <div class="relative">
              <input
                type="text"
                v-model="searchQuery"
                placeholder="Search movies, series..."
                class="w-full p-3 pr-12 border rounded-md text-sm
                       bg-gray-50 dark:bg-gray-700
                       dark:border-gray-600 dark:text-gray-200"
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

          <!-- TYPE -->
          <select
            v-model="selectedType"
            @change="handleFilterChange"
            class="w-full md:w-28 p-3 border rounded-md text-sm
                   bg-gray-50 dark:bg-gray-700
                   dark:border-gray-600 dark:text-gray-200 appearance-none"
          >
            <option value="">Type</option>
            <option value="movie">Movies</option>
            <option value="series">Series</option>
          </select>

          <!-- GENRE -->
          <select
            v-model="selectedGenre"
            @change="handleFilterChange"
            class="w-full md:w-28 p-3 border rounded-md text-sm
                   bg-gray-50 dark:bg-gray-700
                   dark:border-gray-600 dark:text-gray-200 appearance-none"
          >
            <option value="">Genre</option>
            <option v-for="genre in genres" :key="genre.id" :value="genre.id">
              {{ genre.name }}
            </option>
          </select>

          <!-- SORT -->
          <select
            v-model="selectedSort"
            @change="handleFilterChange"
            class="w-full md:w-32 p-3 border rounded-md text-sm
                   bg-gray-50 dark:bg-gray-700
                   dark:border-gray-600 dark:text-gray-200 appearance-none"
          >
            <option value="">Sort</option>
            <option value="-avg_rating">Top Rated</option>
            <option value="title">Title (A-Z)</option>
            <option value="-title">Title (Z-A)</option>
            <option value="-release_date">Newest First</option>
            <option value="release_date">Oldest First</option>
          </select>

        </div>
      </div>

      <!-- RIGHT: NAV / AUTH / THEME -->
      <div class="flex items-center space-x-4 flex-shrink-0">

        <a
          @click.prevent="$emit('navigate', 'home')"
          href="#"
          class="text-gray-300 hover:text-white"
        >
          Home
        </a>

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
          <span v-if="authStore.user" class="text-white hidden md:inline">
            Welcome, {{ authStore.user.username }}
          </span>
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
          <svg v-if="colorMode.value === 'light'" xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M20.354 15.354A9 9 0 018.646 3.646
                 9.003 9.003 0 0012 21
                 a9.003 9.003 0 008.354-5.646z" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 3v1m0 16v1m9-9h-1M4 12H3
                 m15.364 6.364l-.707-.707
                 M6.343 6.343l-.707-.707
                 m12.728 0l-.707.707
                 M6.343 17.657l-.707.707
                 M16 12a4 4 0 11-8 0
                 4 4 0 018 0z" />
          </svg>
        </button>

      </div>
    </div>
  </nav>
</template>




<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useApi } from '../composables/useApi';

const colorMode = useColorMode();
const emit = defineEmits(['navigate', 'filter-change']);
const authStore = useAuthStore();
const { getGenres } = useApi();

const searchQuery = ref('');
const selectedGenre = ref('');
const selectedSort = ref('');
const selectedType = ref('');
const genres = ref([]);

const toggleTheme = () => {
  colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark';
};

const handleLogout = () => {
  authStore.logout();
  emit('navigate', 'home');
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
  if (selectedType.value) {
    params.type = selectedType.value;
  }
  emit('filter-change', params);
};

onMounted(() => {
  fetchGenres();
});
</script>
