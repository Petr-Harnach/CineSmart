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
          v-model="username"
          class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-900 dark:border-gray-600 dark:text-gray-200"
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

    <!-- Security Section -->
    <hr class="my-8 border-gray-200 dark:border-gray-700">
    <section class="mt-8">
      <h2 class="text-2xl font-bold mb-4 text-gray-800 dark:text-gray-100">Security</h2>
      <form @submit.prevent="handleChangePassword" class="bg-gray-50 dark:bg-gray-700 p-6 rounded-lg">
        <div v-if="passwordSuccess" class="mb-4 text-green-600 dark:text-green-400">{{ passwordSuccess }}</div>
        <div v-if="passwordError" class="mb-4 text-red-600 dark:text-red-400">{{ passwordError }}</div>

        <div class="mb-4">
          <label for="old_password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Old Password</label>
          <input 
            type="password" 
            id="old_password" 
            v-model="passwordForm.old_password" 
            required
            class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-600 dark:border-gray-500 dark:text-white"
          >
        </div>
        <div class="mb-4">
          <label for="new_password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">New Password</label>
          <input 
            type="password" 
            id="new_password" 
            v-model="passwordForm.new_password" 
            required
            minlength="8"
            class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-600 dark:border-gray-500 dark:text-white"
          >
        </div>
        <div class="mb-4">
          <label for="confirm_password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Confirm New Password</label>
          <input 
            type="password" 
            id="confirm_password" 
            v-model="passwordForm.confirm_password" 
            required
            class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-600 dark:border-gray-500 dark:text-white"
          >
        </div>
        <div class="flex justify-end">
          <button 
            type="submit" 
            :disabled="isChangingPassword"
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:bg-red-400"
          >
            {{ isChangingPassword ? 'Changing...' : 'Change Password' }}
          </button>
        </div>
      </form>
    </section>

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

    <!-- Collections Section -->
    <hr class="my-8 border-gray-200 dark:border-gray-700">
    <section class="mt-8">
      <h2 class="text-2xl font-bold mb-4 text-gray-800 dark:text-gray-100">My Collections</h2>
      
      <!-- Create New Collection Form -->
      <form @submit.prevent="handleCreateCollection" class="mb-8 bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
        <h3 class="text-lg font-semibold mb-3 text-gray-700 dark:text-gray-200">Create New Collection</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <input 
            type="text" 
            v-model="newCollection.name" 
            placeholder="Collection Name" 
            class="p-2 border rounded bg-white dark:bg-gray-600 dark:text-white dark:border-gray-500" 
            required
          >
          <input 
            type="text" 
            v-model="newCollection.description" 
            placeholder="Description (optional)" 
            class="p-2 border rounded bg-white dark:bg-gray-600 dark:text-white dark:border-gray-500"
          >
        </div>
        <div class="flex items-center justify-between mt-3">
          <label class="flex items-center space-x-2 text-gray-700 dark:text-gray-300">
            <input type="checkbox" v-model="newCollection.is_public" class="form-checkbox">
            <span>Public</span>
          </label>
          <button 
            type="submit" 
            :disabled="isCreatingCollection"
            class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:bg-green-400"
          >
            {{ isCreatingCollection ? 'Creating...' : 'Create' }}
          </button>
        </div>
      </form>

      <!-- List of Collections -->
      <div v-if="collections.length > 0" class="space-y-4">
        <div 
          v-for="collection in collections" 
          :key="collection.id" 
          class="flex justify-between items-center bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700"
        >
          <div>
            <h3 class="text-lg font-bold text-gray-800 dark:text-gray-100">{{ collection.name }}</h3>
            <p class="text-gray-600 dark:text-gray-400 text-sm">{{ collection.description }}</p>
            <div class="flex gap-2 mt-1 text-xs">
              <span :class="collection.is_public ? 'text-green-600' : 'text-yellow-600'">
                {{ collection.is_public ? 'Public' : 'Private' }}
              </span>
              <span class="text-gray-400">• {{ collection.items.length }} items</span>
            </div>
          </div>
          <button @click="handleDeleteCollection(collection.id)" class="text-red-500 hover:text-red-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
      <p v-else class="text-center text-gray-500 italic">No collections yet.</p>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, reactive, nextTick } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useApi } from '../composables/useApi';

const authStore = useAuthStore();
const { updateProfile, getWatchlist, getCollections, createCollection, deleteCollection, changePassword } = useApi();

const username = ref('');
const bio = ref('');
const profilePictureFile = ref(null);
const previewImageUrl = ref('');

const isSaving = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

// Změna hesla
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
});
const isChangingPassword = ref(false);
const passwordSuccess = ref('');
const passwordError = ref('');

// Pro statistiky
const watchlistItems = ref([]);
const isLoadingStats = ref(true);

// Pro kolekce
const collections = ref([]);
const newCollection = reactive({
  name: '',
  description: '',
  is_public: true
});
const isCreatingCollection = ref(false);

onMounted(() => {
  if (authStore.user) {
    username.value = authStore.user.username || '';
    bio.value = authStore.user.bio || '';
  }
  fetchWatchlistData();
  fetchCollections();
});

const fetchWatchlistData = async () => {
  isLoadingStats.value = true;
  try {
    const response = await getWatchlist();
    // Bezpečný přístup k datům
    watchlistItems.value = response.data?.results || [];
  } catch (err) {
    console.error('Error fetching watchlist for stats:', err);
    watchlistItems.value = [];
  } finally {
    isLoadingStats.value = false;
  }
};

const fetchCollections = async () => {
  try {
    const response = await getCollections();
    // Filtrovat pouze kolekce přihlášeného uživatele
    collections.value = (response.data?.results || []).filter(c => c.user.id === authStore.user?.id);
  } catch (err) {
    console.error('Error fetching collections:', err);
    collections.value = [];
  }
};

const handleCreateCollection = async () => {
  isCreatingCollection.value = true;
  try {
    await createCollection(newCollection);
    newCollection.name = '';
    newCollection.description = '';
    newCollection.is_public = true;
    await fetchCollections();
  } catch (err) {
    console.error('Error creating collection:', err);
    alert('Failed to create collection.');
  } finally {
    isCreatingCollection.value = false;
  }
};

const handleDeleteCollection = async (id) => {
  if (!confirm('Are you sure you want to delete this collection?')) return;
  try {
    await deleteCollection(id);
    await fetchCollections();
  } catch (err) {
    console.error('Error deleting collection:', err);
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
  formData.append('username', username.value);
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
    errorMessage.value = 'Failed to update profile. Username might be taken.';
  } finally {
    isSaving.value = false;
  }
};

const handleChangePassword = async () => {
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    passwordError.value = "New passwords do not match.";
    return;
  }
  
  isChangingPassword.value = true;
  passwordError.value = '';
  passwordSuccess.value = '';

  try {
    await changePassword({
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password
    });
    passwordSuccess.value = "Password changed successfully.";
    passwordForm.old_password = '';
    passwordForm.new_password = '';
    passwordForm.confirm_password = '';
  } catch (err) {
    console.error('Password change failed:', err);
    passwordError.value = err.response?.data?.detail || "Failed to change password. Please check your old password.";
  } finally {
    isChangingPassword.value = false;
  }
};

// Computed properties pro statistiky
const watchedMovies = computed(() => {
    if (!Array.isArray(watchlistItems.value)) return [];
    return watchlistItems.value.filter(item => item.watched);
});

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
  const totalMinutes = watchedMovies.value.reduce((total, item) => total + (item.movie?.duration_minutes || 0), 0);
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  const formattedTime = `${hours}h ${minutes}m`;

  // 3. Nejoblíbenější žánr
  const genreCounts = watchedMovies.value
    .flatMap(item => item.movie?.genres || [])
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
</script>