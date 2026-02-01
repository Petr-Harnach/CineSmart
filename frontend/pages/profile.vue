<template>
  <div class="bg-gray-100 dark:bg-gray-900 min-h-screen pb-12">
    <!-- Loading State -->
    <div v-if="isLoadingProfile" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>

    <div v-else-if="authStore.user">
      <!-- HERO SECTION (STEAM STYLE) -->
      <div class="relative w-full h-64 md:h-80 bg-gray-800 overflow-hidden group">
        <!-- Cover Image -->
        <img 
          v-if="authStore.user.cover_picture" 
          :src="authStore.user.cover_picture" 
          class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
          alt="Cover"
        >
        <div v-else class="w-full h-full bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center">
          <span class="text-gray-600 dark:text-gray-500 text-lg font-medium">Zatím bez pozadí</span>
        </div>
        
        <!-- Gradient Overlay -->
        <div class="absolute inset-0 bg-gradient-to-t from-gray-900 via-transparent to-transparent"></div>

        <!-- Edit Profile Button (Top Right) -->
        <button 
          @click="openEditModal"
          class="absolute top-4 right-4 bg-black/50 hover:bg-black/70 backdrop-blur-md text-white px-4 py-2 rounded-full text-sm font-medium transition-all flex items-center gap-2 border border-white/10"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
          Upravit profil
        </button>
      </div>

      <!-- PROFILE INFO BAR -->
      <div class="container mx-auto px-4 relative -mt-16 mb-8 flex flex-col md:flex-row items-end md:items-center gap-6">
        <!-- Avatar -->
        <div class="relative">
          <div class="w-32 h-32 md:w-40 md:h-40 rounded-full border-4 border-gray-900 overflow-hidden bg-gray-800 shadow-2xl">
            <img 
              v-if="authStore.user.profile_picture" 
              :src="authStore.user.profile_picture" 
              class="w-full h-full object-cover"
              alt="Avatar"
            >
            <div v-else class="h-9 w-9 rounded-full bg-blue-600 flex items-center justify-center text-white text-4xl font-bold">
              {{ authStore.user.username.charAt(0).toUpperCase() }}
            </div>
          </div>
          <!-- Level Badge (Absolute) -->
          <div class="absolute -bottom-2 -right-2 bg-yellow-500 text-gray-900 font-bold w-10 h-10 rounded-full flex items-center justify-center border-2 border-gray-900 shadow-lg" title="Úroveň">
            {{ userLevel }}
          </div>
        </div>

        <!-- Name -->
        <div class="flex-grow text-center md:text-left pb-2">
          <h1 class="text-3xl md:text-4xl font-black text-white drop-shadow-md">{{ authStore.user.username }}</h1>
        </div>

        <!-- Main Stats (Right) -->
        <div class="flex gap-6 pb-2">
          <div class="text-center">
            <span class="block text-2xl font-bold text-white">{{ stats.totalCount }}</span>
            <span class="text-xs text-gray-400 uppercase tracking-wide">Filmů</span>
          </div>
          <div class="text-center">
            <span class="block text-2xl font-bold text-white">{{ stats.formattedTime }}</span>
            <span class="text-xs text-gray-400 uppercase tracking-wide">Čas</span>
          </div>
        </div>
      </div>

      <!-- MAIN CONTENT LAYOUT (2 COLUMNS) -->
      <div class="container mx-auto px-4 grid grid-cols-1 lg:grid-cols-4 gap-8">
        
        <!-- LEFT COLUMN (MAIN - 3/4) -->
        <div class="lg:col-span-3 space-y-8">
          
          <!-- SHOWCASE: TOP OBLÍBENÉ (Simulated from Watchlist for now) -->
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center bg-gray-50 dark:bg-gray-800/50">
              <h2 class="text-lg font-bold text-gray-800 dark:text-white flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-500" viewBox="0 0 20 20" fill="currentColor"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 g 00.951-.69l1.07-3.292z" /></svg>
                Výstavka: Oblíbené
              </h2>
            </div>
            <div class="p-6">
              <div v-if="topFavorites.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
                <NuxtLink 
                  v-for="item in topFavorites" 
                  :key="item.id" 
                  :to="`/movies/${item.movie.id}`"
                  class="group relative aspect-[2/3] rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-all hover:-translate-y-1"
                >
                  <img :src="item.movie.poster" class="w-full h-full object-cover">
                  <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center p-2 text-center">
                    <span class="text-white text-xs font-bold">{{ item.movie.title }}</span>
                  </div>
                </NuxtLink>
              </div>
              <p v-else class="text-gray-500 italic text-center py-8">Přidejte si filmy do seznamu a označte je jako shlédnuté.</p>
            </div>
          </div>

          <!-- SHOWCASE: KOLEKCE -->
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center bg-gray-50 dark:bg-gray-800/50">
              <h2 class="text-lg font-bold text-gray-800 dark:text-white flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-500" viewBox="0 0 20 20" fill="currentColor"><path d="M7 3a1 1 0 000 2h6a1 1 g 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z" /></svg>
                Moje Kolekce
              </h2>
              <NuxtLink to="/collections" class="text-sm text-blue-600 hover:underline">Všechny kolekce</NuxtLink>
            </div>
            <div class="p-6">
              <div v-if="collections.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div 
                  v-for="collection in collections.slice(0, 4)" 
                  :key="collection.id" 
                  class="flex items-center gap-4 p-3 rounded-lg bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 transition cursor-pointer"
                  @click="navigateTo(`/collections/${collection.id}`)"
                >
                  <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded flex-shrink-0 flex items-center justify-center text-blue-600 dark:text-blue-400">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                  </div>
                  <div class="overflow-hidden">
                    <h4 class="font-bold text-gray-900 dark:text-white truncate">{{ collection.name }}</h4>
                    <p class="text-xs text-gray-500">{{ collection.items.length }} položek</p>
                  </div>
                </div>
              </div>
              <p v-else class="text-gray-500 italic text-center py-4">Zatím žádné kolekce.</p>
            </div>
          </div>

        </div>

        <!-- RIGHT COLUMN (SIDEBAR - 1/4) -->
        <div class="lg:col-span-1 space-y-8">
          
          <!-- Odznaky (Badges) -->
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
            <h3 class="text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4">Odznaky</h3>
            <div class="flex flex-wrap gap-2">
              <!-- Level Badge -->
              <div class="bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400 px-3 py-1 rounded-full text-xs font-bold border border-yellow-200 dark:border-yellow-800" title="Úroveň">
                Lvl {{ userLevel }}
              </div>
              <!-- Cinephile Badge -->
              <div v-if="stats.totalCount >= 50" class="bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400 px-3 py-1 rounded-full text-xs font-bold border border-purple-200 dark:border-purple-800">
                Cinephile
              </div>
              <!-- Newbie Badge -->
              <div v-else class="bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 px-3 py-1 rounded-full text-xs font-bold border border-gray-200 dark:border-gray-600">
                Začátečník
              </div>
              <!-- Genre Badge -->
              <div v-if="stats.favoriteGenre !== 'N/A'" class="bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 px-3 py-1 rounded-full text-xs font-bold border border-blue-200 dark:border-blue-800">
                Fanoušek {{ stats.favoriteGenre }}
              </div>
            </div>
          </div>

          <!-- Quick Links -->
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
            <div class="p-4 space-y-1">
              <NuxtLink to="/watchlist" class="block px-4 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 transition">
                Můj seznam
              </NuxtLink>
              <NuxtLink to="/collections" class="block px-4 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 transition">
                Moje kolekce
              </NuxtLink>
              <!-- Placeholder for Reviews page if it exists separately -->
              <div class="block px-4 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 transition cursor-pointer">
                Recenze
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- EDIT PROFILE MODAL -->
    <transition enter-active-class="duration-300 ease-out" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100" leave-active-class="duration-200 ease-in" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
      <div v-if="isEditModalOpen" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <div class="flex items-center justify-center min-h-screen px-4 text-center">
          <div class="fixed inset-0 bg-gray-900 bg-opacity-75 transition-opacity backdrop-blur-sm" @click="closeEditModal"></div>

          <div class="inline-block align-bottom bg-white dark:bg-gray-800 rounded-2xl text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full border border-gray-200 dark:border-gray-700">
            <div class="px-6 py-6">
              <div class="flex justify-between items-center mb-6">
                <h3 class="text-xl font-bold text-gray-900 dark:text-white">Upravit profil</h3>
                <button @click="closeEditModal" class="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300">
                  <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
              </div>

              <form @submit.prevent="saveProfile" class="space-y-4">
                <!-- Avatar Upload -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Avatar</label>
                  <div class="flex items-center gap-4">
                    <img :src="previewImageUrl || authStore.user.profile_picture || 'https://via.placeholder.com/50'" class="h-12 w-12 rounded-full object-cover border-2 border-gray-300 dark:border-gray-600">
                    <input type="file" @change="handleFileChange" accept="image/*" class="text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 dark:file:bg-gray-700 dark:file:text-gray-300">
                  </div>
                </div>

                <!-- Cover Upload -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Pozadí profilu (Cover)</label>
                  <input type="file" @change="handleCoverChange" accept="image/*" class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 dark:file:bg-gray-700 dark:file:text-gray-300">
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Uživatelské jméno</label>
                  <input type="text" v-model="editForm.username" class="mt-1 block w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 dark:text-white focus:ring-blue-500 focus:border-blue-500">
                </div>
                
                <!-- Password Change Toggle -->
                <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
                  <button type="button" @click="showPasswordSection = !showPasswordSection" class="text-blue-600 text-sm hover:underline">Změnit heslo</button>
                </div>

                <div v-if="showPasswordSection" class="space-y-3 bg-gray-50 dark:bg-gray-700/50 p-3 rounded-lg border border-gray-200 dark:border-gray-600">
                  <input type="password" v-model="passwordForm.old_password" placeholder="Staré heslo" class="block w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 dark:text-white text-sm">
                  <input type="password" v-model="passwordForm.new_password" placeholder="Nové heslo" class="block w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 dark:text-white text-sm">
                  <input type="password" v-model="passwordForm.confirm_password" placeholder="Potvrdit nové heslo" class="block w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 dark:text-white text-sm">
                  <button type="button" @click="handleChangePassword" :disabled="isChangingPassword" class="w-full py-1 bg-red-500 text-white rounded text-sm hover:bg-red-600">Aktualizovat heslo</button>
                </div>

                <div class="flex justify-end pt-4">
                  <button type="submit" :disabled="isSaving" class="px-6 py-2 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 disabled:opacity-50">
                    {{ isSaving ? 'Ukládám...' : 'Uložit změny' }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, reactive } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useApi } from '../composables/useApi';
import { useToast } from '../composables/useToast';
import { navigateTo } from '#app';

const authStore = useAuthStore();
const { updateProfile, getWatchlist, getCollections, changePassword } = useApi();
const toast = useToast();

const isLoadingProfile = ref(true);
const isEditModalOpen = ref(false);
const isSaving = ref(false);
const showPasswordSection = ref(false);
const isChangingPassword = ref(false);

const editForm = reactive({
  username: '',
});
const profilePictureFile = ref(null);
const coverPictureFile = ref(null);
const previewImageUrl = ref('');

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
});

const watchlistItems = ref([]);
const collections = ref([]);

const openEditModal = () => {
  editForm.username = authStore.user.username;
  isEditModalOpen.value = true;
};

const closeEditModal = () => {
  isEditModalOpen.value = false;
  showPasswordSection.value = false;
  passwordForm.old_password = '';
  passwordForm.new_password = '';
  passwordForm.confirm_password = '';
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    profilePictureFile.value = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImageUrl.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const handleCoverChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    coverPictureFile.value = file;
  }
};

const saveProfile = async () => {
  isSaving.value = true;
  const formData = new FormData();
  formData.append('username', editForm.username);
  if (profilePictureFile.value) {
    formData.append('profile_picture', profilePictureFile.value);
  }
  if (coverPictureFile.value) {
    formData.append('cover_picture', coverPictureFile.value);
  }

  try {
    await updateProfile(formData);
    await authStore.fetchProfile();
    toast.success('Profil uložen!');
    closeEditModal();
  } catch (err) {
    console.error('Error:', err);
    toast.error('Chyba při ukládání profilu.');
  } finally {
    isSaving.value = false;
  }
};

const handleChangePassword = async () => {
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    toast.error("Hesla se neshodují.");
    return;
  }
  isChangingPassword.value = true;
  try {
    await changePassword({
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password
    });
    toast.success("Heslo změněno.");
    passwordForm.old_password = '';
    passwordForm.new_password = '';
    passwordForm.confirm_password = '';
    showPasswordSection.value = false;
  } catch (err) {
    toast.error(err.response?.data?.detail || "Chyba při změně hesla.");
  } finally {
    isChangingPassword.value = false;
  }
};

const fetchData = async () => {
  isLoadingProfile.value = true;
  try {
    if (!authStore.user) {
        await authStore.initialize();
    }
    const [wRes, cRes] = await Promise.all([
      getWatchlist(),
      getCollections()
    ]);
    watchlistItems.value = wRes.data.results;
    collections.value = cRes.data.results.filter(c => c.user.id === authStore.user?.id);
  } catch (err) {
    console.error(err);
  } finally {
    isLoadingProfile.value = false;
  }
};

// Computed Stats
const watchedMovies = computed(() => watchlistItems.value.filter(item => item.watched));

const stats = computed(() => {
  const totalCount = watchedMovies.value.length;
  const totalMinutes = watchedMovies.value.reduce((acc, item) => acc + (item.movie?.duration_minutes || 0), 0);
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  
  const genreCounts = {};
  watchedMovies.value.forEach(item => {
    item.movie?.genres?.forEach(g => {
      genreCounts[g.name] = (genreCounts[g.name] || 0) + 1;
    });
  });
  
  let favoriteGenre = 'N/A';
  let max = 0;
  for (const [genre, count] of Object.entries(genreCounts)) {
    if (count > max) {
      max = count;
      favoriteGenre = genre;
    }
  }

  return {
    totalCount,
    formattedTime: `${hours}h ${minutes}m`,
    favoriteGenre
  };
});

const userLevel = computed(() => {
  const count = stats.value.totalCount;
  return Math.floor(count / 5) + 1; // Level up every 5 movies
});

const topFavorites = computed(() => {
  // Prozatím bereme posledních 5 zhlédnutých jako "Top". 
  // V budoucnu můžeme brát podle hodnocení (5 hvězd).
  return [...watchedMovies.value].reverse().slice(0, 5);
});

onMounted(() => {
  fetchData();
});
</script>