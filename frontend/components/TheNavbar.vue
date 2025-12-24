<template>
  <nav class="bg-gray-800 dark:bg-gray-950 p-4">
    <div class="container mx-auto flex justify-between items-center flex-wrap">
      <a @click.prevent="$emit('navigate', 'home')" href="#" class="text-white text-lg font-bold mb-2 md:mb-0">CineSmart</a>
      <div class="flex items-center space-x-4 flex-grow md:flex-grow-0">
        <a @click.prevent="$emit('navigate', 'home')" href="#" class="text-gray-300 hover:text-white">Home</a>
        
        <template v-if="!authStore.isLoggedIn">
          <a @click.prevent="$emit('navigate', 'login')" href="#" class="text-gray-300 hover:text-white">Login</a>
          <a @click.prevent="$emit('navigate', 'register')" href="#" class="text-gray-300 hover:text-white">Register</a>
        </template>
        
        <template v-else>
          <a @click.prevent="$emit('navigate', 'watchlist')" href="#" class="text-gray-300 hover:text-white">My Watchlist</a>
          <span v-if="authStore.user" class="text-white">Welcome, {{ authStore.user.username }}</span>
          <a @click.prevent="handleLogout" href="#" class="text-white hover:bg-red-700 bg-red-600 px-3 py-1 rounded">Logout</a>
        </template>

        <button @click="toggleTheme" class="text-gray-300 hover:text-white">
          <svg v-if="colorMode.value === 'light'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
        </button>
      </div>

      <!-- Filter and Search Bar -->
      <div class="w-full mt-4 md:mt-0 flex flex-col md:flex-row space-y-2 md:space-y-0 md:space-x-2 items-center">
        <form @submit.prevent="handleFilterChange" class="w-full md:w-auto flex-grow">
          <div class="relative">
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Search movies..."
              class="w-full p-2 pr-8 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200"
            />
            <button type="submit" class="absolute right-0 top-0 mt-2 mr-2 text-gray-400 hover:text-white">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            </button>
          </div>
        </form>
        <select v-model="selectedType" @change="handleFilterChange" class="w-full md:w-auto p-2 pr-8 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200 appearance-none" style="background-image: url('data:image/svg+xml;charset=UTF-8,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 fill=%27none%27 viewBox=%270 0 20 20%27%3e%3cpath stroke=%27%236b7280%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%271.5%27 d=%27m6 8 4 4 4-4%27/%3e%3c/svg%3e'); background-position: right 0.5rem center; background-repeat: no-repeat; background-size: 1.5em 1.5em;">
          <option value="">All Types</option>
          <option value="movie">Movies</option>
          <option value="series">Series</option>
        </select>
        <select v-model="selectedGenre" @change="handleFilterChange" class="w-full md:w-auto p-2 pr-8 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200 appearance-none" style="background-image: url('data:image/svg+xml;charset=UTF-8,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 fill=%27none%27 viewBox=%270 0 20 20%27%3e%3cpath stroke=%27%236b7280%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%271.5%27 d=%27m6 8 4 4 4-4%27/%3e%3c/svg%3e'); background-position: right 0.5rem center; background-repeat: no-repeat; background-size: 1.5em 1.5em;">
          <option value="">All Genres</option>
          <option v-for="genre in genres" :key="genre.id" :value="genre.id">
            {{ genre.name }}
          </option>
        </select>
        <select v-model="selectedSort" @change="handleFilterChange" class="w-full md:w-auto p-2 pr-8 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200 appearance-none" style="background-image: url('data:image/svg+xml;charset=UTF-8,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 fill=%27none%27 viewBox=%270 0 20 20%27%3e%3cpath stroke=%27%236b7280%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%271.5%27 d=%27m6 8 4 4 4-4%27/%3e%3c/svg%3e'); background-position: right 0.5rem center; background-repeat: no-repeat; background-size: 1.5em 1.5em;">
          <option value="">Sort by</option>
          <option value="-avg_rating">Top Rated</option>
          <option value="title">Title (A-Z)</option>
          <option value="-title">Title (Z-A)</option>
          <option value="-release_date">Newest First</option>
          <option value="release_date">Oldest First</option>
        </select>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useApi } from '../composables/useApi';

const colorMode = useColorMode();
const emit = defineEmits(['navigate', 'filter-change']); // Add 'filter-change' event
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
  emit('filter-change', params); // Emit filter-change event
};

onMounted(() => {
  fetchGenres();
});
</script>