<template>
  <div class="max-w-2xl mx-auto mt-10 p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
    <h1 class="text-3xl font-bold mb-6 text-gray-800 dark:text-gray-100">My Profile</h1>
    
    <div v-if="!authStore.user" class="text-center text-gray-500">
      Loading user data...
    </div>

    <form v-else @submit.prevent="saveProfile">
      <div class="flex flex-col items-center space-y-4 mb-8">
        <img 
          v-if="previewImageUrl || authStore.user.profile_picture"
          :src="previewImageUrl || authStore.user.profile_picture" 
          alt="Profile Picture"
          class="h-32 w-32 rounded-full object-cover border-4 border-gray-200 dark:border-gray-600"
        >
        <div v-else class="h-32 w-32 rounded-full object-cover border-4 border-gray-200 dark:border-gray-600 flex items-center justify-center bg-gray-300 dark:bg-gray-700">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
        </div>
        <div class="relative">
          <input 
            type="file" 
            @change="handleFileChange" 
            accept="image/*"
            class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            id="file-upload"
          >
          <label for="file-upload" class="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600 cursor-pointer">
            Change Picture
          </label>
        </div>
      </div>

      <div class="mb-6">
        <label for="username" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Username</label>
        <input 
          type="text" 
          id="username"
          :value="authStore.user.username"
          disabled
          class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm bg-gray-100 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-400"
        >
      </div>

      <div class="mb-6">
        <label for="bio" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Bio</label>
        <textarea 
          id="bio" 
          v-model="bio"
          rows="4"
          class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-900 dark:border-gray-600 dark:text-gray-200"
          placeholder="Tell us something about yourself..."
        ></textarea>
      </div>

      <div v-if="successMessage" class="mb-4 text-green-600 dark:text-green-400">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="mb-4 text-red-600 dark:text-red-400">
        {{ errorMessage }}
      </div>

      <div class="flex justify-end">
        <button 
          type="submit" 
          :disabled="isSaving"
          class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-blue-400"
        >
          {{ isSaving ? 'Saving...' : 'Save Profile' }}
        </button>
      </div>
    </form>

    <!-- Stats Section -->
    <hr class="my-8 border-gray-200 dark:border-gray-700">
    <section class="mt-8">
      <h2 class="text-2xl font-bold mb-2 text-gray-800 dark:text-gray-100">Your Stats</h2>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
        Stats are calculated from movies in your watchlist that you've marked as "watched".
      </p>
      <div v-if="isLoadingStats" class="text-center text-gray-500">
        Loading stats...
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
        <!-- Stat Card: Movies Watched -->
        <div class="bg-gray-100 dark:bg-gray-700 p-6 rounded-lg">
          <p class="text-sm text-gray-500 dark:text-gray-400">Movies Watched</p>
          <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ stats.totalCount }}</p>
        </div>
        <!-- Stat Card: Time on Screen -->
        <div class="bg-gray-100 dark:bg-gray-700 p-6 rounded-lg">
          <p class="text-sm text-gray-500 dark:text-gray-400">Time on Screen</p>
          <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ stats.formattedTime }}</p>
        </div>
        <!-- Stat Card: Favorite Genre -->
        <div class="bg-gray-100 dark:bg-gray-700 p-6 rounded-lg">
          <p class="text-sm text-gray-500 dark:text-gray-400">Favorite Genre</p>
          <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ stats.favoriteGenre }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useApi } from '../composables/useApi';

const authStore = useAuthStore();
const { updateProfile, getWatchlist } = useApi();

const bio = ref('');
const profilePictureFile = ref(null);
const previewImageUrl = ref('');

const isSaving = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

// Pro statistiky
const watchlistItems = ref([]);
const isLoadingStats = ref(true);

// Computed properties pro statistiky
const watchedMovies = computed(() => watchlistItems.value.filter(item => item.watched));

const stats = computed(() => {
  if (isLoadingStats.value || watchedMovies.value.length === 0) {
    return {
      totalCount: 0,
      totalMinutes: 0,
      favoriteGenre: 'N/A',
      formattedTime: '0h 0m',
    };
  }

  // 1. Celkový počet
  const totalCount = watchedMovies.value.length;

  // 2. Celkový čas
  const totalMinutes = watchedMovies.value.reduce((total, item) => total + (item.movie.duration_minutes || 0), 0);
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  const formattedTime = `${hours}h ${minutes}m`;

  // 3. Nejoblíbenější žánr
  const genreCounts = watchedMovies.value
    .flatMap(item => item.movie.genres)
    .reduce((counts, genre) => {
      counts[genre.name] = (counts[genre.name] || 0) + 1;
      return counts;
    }, {});
  
  let favoriteGenre = 'N/A';
  let maxCount = 0;
  for (const genre in genreCounts) {
    if (genreCounts[genre] > maxCount) {
      maxCount = genreCounts[genre];
      favoriteGenre = genre;
    }
  }

  return {
    totalCount,
    totalMinutes,
    favoriteGenre,
    formattedTime,
  };
});

onMounted(() => {
  if (authStore.user) {
    bio.value = authStore.user.bio || '';
  }
  fetchWatchlistData();
});

const fetchWatchlistData = async () => {
  isLoadingStats.value = true;
  try {
    const response = await getWatchlist();
    watchlistItems.value = response.data.results;
  } catch (err) {
    console.error('Error fetching watchlist for stats:', err);
  } finally {
    isLoadingStats.value = false;
  }
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    profilePictureFile.value = file;
    // Vytvoření náhledu obrázku
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImageUrl.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const saveProfile = async () => {
  isSaving.value = true;
  successMessage.value = '';
  errorMessage.value = '';

  const formData = new FormData();
  formData.append('bio', bio.value);
  if (profilePictureFile.value) {
    formData.append('profile_picture', profilePictureFile.value);
  }

  try {
    await updateProfile(formData);
    await authStore.fetchProfile(); // Obnovení dat uživatele ve storu
    successMessage.value = 'Profile updated successfully!';
  } catch (err) {
    console.error('Error updating profile:', err);
    errorMessage.value = 'Failed to update profile. Please try again.';
  } finally {
    isSaving.value = false;
  }
};
</script>
