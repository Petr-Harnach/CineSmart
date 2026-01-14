<template>
  <!-- Main Background -->
  <div class="bg-gray-100 dark:bg-gray-900 min-h-screen pb-12 transition-colors duration-500">
    <!-- Loading State -->
    <div v-if="isLoadingProfile" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>

    <div v-else-if="authStore.user">
      <!-- HERO SECTION -->
      <div class="relative w-full h-64 md:h-[400px] bg-gray-800 overflow-hidden group">
        <!-- Cover Image -->
        <div class="absolute inset-0">
          <img 
            v-if="authStore.user.cover_picture" 
            :src="authStore.user.cover_picture" 
            class="w-full h-full object-cover transition-transform duration-[2000ms] group-hover:scale-105"
            alt="Cover"
          >
          <!-- Gradient pro přechod do pozadí -->
          <div class="absolute inset-0 bg-gradient-to-t from-gray-900 via-transparent to-transparent opacity-90"></div>
        </div>

        <button 
          @click="openEditModal"
          class="absolute top-6 right-6 bg-black/50 hover:bg-black/70 backdrop-blur-md text-white px-5 py-2 rounded-full text-sm font-bold transition-all flex items-center gap-2 border border-white/20 shadow-lg z-30"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
          Upravit profil
        </button>
      </div>

      <!-- PROFILE INFO BAR -->
      <div class="container mx-auto px-4 relative -mt-24 mb-12 flex flex-col md:flex-row items-center md:items-end gap-8 z-20">
        <!-- Avatar (Circle + Black Frame) -->
        <div class="relative flex-shrink-0">
          <div class="w-40 h-40 md:w-48 md:h-48 rounded-full p-1 bg-black shadow-2xl relative z-10"> <!-- Černý rámeček -->
            <div class="w-full h-full rounded-full overflow-hidden bg-gray-800 border-4 border-gray-900">
              <img 
                v-if="authStore.user.profile_picture" 
                :src="authStore.user.profile_picture" 
                class="w-full h-full object-cover"
                alt="Avatar"
              >
              <div v-else class="w-full h-full flex items-center justify-center text-white text-5xl font-bold bg-blue-600">
                {{ authStore.user.username.charAt(0).toUpperCase() }}
              </div>
            </div>
          </div>
          <!-- Level Badge -->
          <div class="absolute bottom-2 right-2 z-20 bg-yellow-500 text-gray-900 font-bold w-10 h-10 md:w-12 md:h-12 rounded-full flex items-center justify-center border-4 border-gray-900 shadow-lg cursor-help" :title="'Level ' + userLevel">
            {{ userLevel }}
          </div>
        </div>

        <!-- Name, Bio & Stats -->
        <div class="flex-grow text-center md:text-left pb-4">
          <!-- Standardní font -->
          <h1 class="text-4xl md:text-5xl font-bold text-white drop-shadow-md mb-2">
            {{ authStore.user.username }}
          </h1>
          <p class="text-gray-300 text-sm md:text-base max-w-2xl mx-auto md:mx-0 font-medium leading-relaxed mb-4">
            {{ authStore.user.bio || 'Tento uživatel zatím nemá žádný příběh...' }}
          </p>
          
          <!-- Stats Chips -->
          <div class="flex flex-wrap justify-center md:justify-start gap-3">
            <div class="bg-gray-800/80 backdrop-blur border border-gray-700 px-4 py-2 rounded-lg flex items-center gap-3 shadow-lg">
              <span class="text-white font-bold text-lg">{{ stats.totalCount }}</span>
              <span class="text-xs text-gray-400 uppercase font-bold tracking-wider">Filmů</span>
            </div>
            <div class="bg-gray-800/80 backdrop-blur border border-gray-700 px-4 py-2 rounded-lg flex items-center gap-3 shadow-lg">
              <span class="text-white font-bold text-lg">{{ stats.formattedTime }}</span>
              <span class="text-xs text-gray-400 uppercase font-bold tracking-wider">Čas</span>
            </div>
          </div>
        </div>
      </div>

      <!-- MAIN CONTENT LAYOUT -->
      <div class="container mx-auto px-4 grid grid-cols-1 lg:grid-cols-4 gap-8">
        
        <!-- LEFT COLUMN (Showcases) -->
        <div class="lg:col-span-3 space-y-10">
          
          <!-- SHOWCASE: TOP OBLÍBENÉ (Glassmorphism) -->
          <div class="bg-white/5 dark:bg-gray-900/60 backdrop-blur-xl rounded-xl shadow-xl border border-gray-200 dark:border-gray-700/50 overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700/50 flex justify-between items-center bg-gray-50/50 dark:bg-white/5">
              <h2 class="text-lg font-bold text-gray-800 dark:text-white flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-500" viewBox="0 0 20 20" fill="currentColor"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" /></svg>
                Výstavka: Oblíbené
              </h2>
            </div>
            <div class="p-6">
              <div v-if="topFavorites.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-6">
                <NuxtLink 
                  v-for="item in topFavorites" 
                  :key="item.id" 
                  :to="`/movies/${item.movie.id}`"
                  class="group relative aspect-[2/3] rounded-lg overflow-hidden shadow-lg transition-all duration-300 hover:scale-105 hover:ring-2 hover:ring-blue-500 z-0 hover:z-10"
                >
                  <img :src="item.movie.poster" class="w-full h-full object-cover">
                  <div class="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-2">
                    <span class="text-white text-xs font-bold leading-tight drop-shadow-md">{{ item.movie.title }}</span>
                  </div>
                </NuxtLink>
              </div>
              <div v-else class="flex flex-col items-center justify-center py-12 text-gray-500 dark:text-gray-400/50">
                <p class="text-sm font-medium">Zatím žádné oblíbené filmy</p>
              </div>
            </div>
          </div>

          <!-- SHOWCASE: KOLEKCE (Glassmorphism) -->
          <div class="bg-white/5 dark:bg-gray-900/60 backdrop-blur-xl rounded-xl shadow-xl border border-gray-200 dark:border-gray-700/50 overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700/50 flex justify-between items-center bg-gray-50/50 dark:bg-white/5">
              <h2 class="text-lg font-bold text-gray-800 dark:text-white flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-500" viewBox="0 0 20 20" fill="currentColor"><path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z" /></svg>
                Moje Kolekce
              </h2>
              <NuxtLink to="/collections" class="text-xs font-bold text-blue-500 hover:text-white uppercase tracking-wide transition-colors">Všechny kolekce &rarr;</NuxtLink>
            </div>
            <div class="p-6">
              <div v-if="collections.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div 
                  v-for="collection in collections.slice(0, 4)" 
                  :key="collection.id" 
                  class="flex items-center gap-4 p-4 rounded-lg bg-gray-50 dark:bg-gray-800/40 hover:bg-gray-100 dark:hover:bg-gray-700/60 transition-all cursor-pointer border border-transparent hover:border-gray-300 dark:hover:border-gray-600 group"
                  @click="navigateTo(`/collections/${collection.id}`)"
                >
                  <div class="w-12 h-12 bg-blue-900/30 rounded-lg flex-shrink-0 flex items-center justify-center text-blue-400 group-hover:scale-110 transition-transform">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                  </div>
                  <div class="overflow-hidden">
                    <h4 class="font-bold text-gray-900 dark:text-white truncate group-hover:text-blue-400 transition-colors">{{ collection.name }}</h4>
                    <p class="text-xs text-gray-500">{{ collection.items.length }} položek</p>
                  </div>
                </div>
              </div>
              <div v-else class="flex flex-col items-center justify-center py-8 opacity-50">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 mb-2 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" /></svg>
                <p class="text-sm font-medium text-gray-400">Žádné kolekce</p>
              </div>
            </div>
          </div>

        </div>

        <!-- RIGHT COLUMN (Sidebar) -->
        <div class="lg:col-span-1 space-y-8">
          
          <!-- Odznaky -->
          <div class="bg-white/5 dark:bg-gray-900/60 backdrop-blur-xl rounded-xl shadow-xl border border-gray-200 dark:border-gray-700/50 p-6">
            <h3 class="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-widest mb-4">Odznaky</h3>
            <div class="flex flex-col gap-3">
              <div class="bg-yellow-500/10 p-3 rounded-lg border border-yellow-500/20 flex items-center gap-3">
                <span class="text-xl">👑</span>
                <div>
                  <p class="text-white font-bold text-xs">Úroveň {{ userLevel }}</p>
                  <p class="text-[10px] text-yellow-500 font-bold uppercase">Filmový Mistr</p>
                </div>
              </div>
              <div v-if="stats.totalCount >= 50" class="bg-purple-500/10 p-3 rounded-lg border border-purple-500/20 flex items-center gap-3">
                <span class="text-xl">🎬</span>
                <div>
                  <p class="text-white font-bold text-xs">Cinephile</p>
                  <p class="text-[10px] text-purple-500 font-bold uppercase">50+ zhlédnutí</p>
                </div>
              </div>
              <div v-else class="bg-gray-500/10 p-3 rounded-lg border border-gray-500/20 flex items-center gap-3 opacity-70">
                <span class="text-xl">🐣</span>
                <div>
                  <p class="text-white font-bold text-xs">Začátečník</p>
                  <p class="text-[10px] text-gray-400 font-bold uppercase">Méně než 50 filmů</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Links -->
          <div class="bg-white/5 dark:bg-gray-900/60 backdrop-blur-xl rounded-xl shadow-xl border border-gray-200 dark:border-gray-700/50 overflow-hidden p-2">
            <NuxtLink to="/watchlist" class="flex items-center justify-between px-4 py-3 rounded-lg hover:bg-white/10 text-gray-300 hover:text-white transition-all group">
              <div class="flex items-center gap-3">
                <div class="p-1.5 bg-gray-800 rounded-md text-gray-400 group-hover:text-blue-400 group-hover:bg-gray-700 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" /></svg>
                </div>
                <span class="font-medium text-sm">Můj seznam</span>
              </div>
              <span class="text-xs font-bold bg-gray-800 text-gray-400 px-2 py-0.5 rounded-md">{{ watchlistItems.length }}</span>
            </NuxtLink>
            
            <NuxtLink to="/collections" class="flex items-center justify-between px-4 py-3 rounded-lg hover:bg-white/10 text-gray-300 hover:text-white transition-all group">
              <div class="flex items-center gap-3">
                <div class="p-1.5 bg-gray-800 rounded-md text-gray-400 group-hover:text-purple-400 group-hover:bg-gray-700 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                </div>
                <span class="font-medium text-sm">Kolekce</span>
              </div>
              <span class="text-xs font-bold bg-gray-800 text-gray-400 px-2 py-0.5 rounded-md">{{ collections.length }}</span>
            </NuxtLink>
            
            <div class="flex items-center justify-between px-4 py-3 rounded-lg opacity-50 cursor-not-allowed">
              <div class="flex items-center gap-3">
                <div class="p-1.5 bg-gray-800 rounded-md text-gray-500">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg>
                </div>
                <span class="font-medium text-sm">Recenze</span>
              </div>
              <span class="text-xs font-bold bg-gray-800 text-gray-500 px-2 py-0.5 rounded-md">{{ reviewCount }}</span>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- EDIT PROFILE MODAL -->
    <transition enter-active-class="duration-300 ease-out" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100" leave-active-class="duration-200 ease-in" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
      <div v-if="isEditModalOpen" class="fixed inset-0 z-[100] overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <div class="flex items-center justify-center min-h-screen px-4 text-center">
          <div class="fixed inset-0 bg-black/80 backdrop-blur-sm transition-opacity" @click="closeEditModal"></div>

          <div class="inline-block align-bottom bg-gray-900 rounded-2xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-xl sm:w-full border border-gray-700">
            <div class="px-6 py-6">
              <div class="flex justify-between items-center mb-6 border-b border-gray-800 pb-4">
                <h3 class="text-xl font-bold text-white">Nastavení Profilu</h3>
                <button @click="closeEditModal" class="text-gray-400 hover:text-white">
                  <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
              </div>

              <form @submit.prevent="saveProfile" class="space-y-6">
                
                <!-- COVER IMAGE SETTINGS -->
                <div>
                  <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Pozadí profilu (Cover)</label>
                  <p class="text-[10px] text-gray-500 mb-2">Doporučená velikost: 1920x500 px. Max 2MB.</p>
                  
                  <div class="relative h-32 w-full rounded-lg overflow-hidden bg-gray-800 border-2 border-dashed border-gray-700 hover:border-blue-500 transition-colors group/cover cursor-pointer">
                    <!-- Preview -->
                    <img v-if="coverPreviewUrl || authStore.user.cover_picture" :src="coverPreviewUrl || authStore.user.cover_picture" class="w-full h-full object-cover">
                    
                    <!-- Overlay with input -->
                    <div class="absolute inset-0 bg-black/50 flex flex-col items-center justify-center opacity-0 group-hover/cover:opacity-100 transition-opacity">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                      <span class="text-white text-xs font-bold">Nahrát obrázek</span>
                      <input type="file" @change="handleCoverChange" accept="image/*" class="absolute inset-0 opacity-0 cursor-pointer">
                    </div>
                  </div>
                </div>

                <!-- AVATAR SETTINGS -->
                <div>
                  <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Avatar</label>
                  <p class="text-[10px] text-gray-500 mb-2">Doporučená velikost: 500x500 px (Čtverec). Max 2MB.</p>
                  
                  <div class="flex items-center gap-4">
                    <div class="relative w-20 h-20 rounded-full overflow-hidden border-2 border-gray-700 group/avatar cursor-pointer">
                      <img :src="previewImageUrl || authStore.user.profile_picture || 'https://via.placeholder.com/100'" class="w-full h-full object-cover">
                      <div class="absolute inset-0 bg-black/50 flex items-center justify-center opacity-0 group-hover/avatar:opacity-100 transition-opacity">
                        <input type="file" @change="handleFileChange" accept="image/*" class="absolute inset-0 opacity-0 cursor-pointer">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /></svg>
                      </div>
                    </div>
                    <div class="flex-grow">
                      <p class="text-sm text-gray-300">Kliknutím na obrázek nahrajete nový.</p>
                    </div>
                  </div>
                </div>

                <!-- INFO FIELDS -->
                <div class="grid grid-cols-1 gap-4">
                  <div>
                    <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Uživatelské jméno</label>
                    <input type="text" v-model="editForm.username" class="w-full p-2.5 bg-gray-800 border border-gray-700 rounded-lg text-white text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none">
                  </div>
                  <div>
                    <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Bio (Příběh)</label>
                    <textarea v-model="editForm.bio" rows="3" class="w-full p-2.5 bg-gray-800 border border-gray-700 rounded-lg text-white text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none" placeholder="Napište něco o sobě..."></textarea>
                  </div>
                </div>

                <!-- Password Toggle -->
                <div class="border-t border-gray-800 pt-4">
                  <button type="button" @click="showPasswordSection = !showPasswordSection" class="text-xs font-bold text-blue-400 hover:text-blue-300 uppercase tracking-wider">
                    {{ showPasswordSection ? 'Skrýt změnu hesla' : 'Změnit heslo' }}
                  </button>
                  
                  <div v-if="showPasswordSection" class="mt-4 p-4 bg-gray-800/50 rounded-lg border border-gray-700 space-y-3">
                    <input type="password" v-model="passwordForm.old_password" placeholder="Současné heslo" class="w-full p-2 bg-gray-900 border border-gray-700 rounded text-white text-sm">
                    <div class="grid grid-cols-2 gap-3">
                      <input type="password" v-model="passwordForm.new_password" placeholder="Nové heslo" class="w-full p-2 bg-gray-900 border border-gray-700 rounded text-white text-sm">
                      <input type="password" v-model="passwordForm.confirm_password" placeholder="Potvrdit nové" class="w-full p-2 bg-gray-900 border border-gray-700 rounded text-white text-sm">
                    </div>
                    <button type="button" @click="handleChangePassword" :disabled="isChangingPassword" class="w-full py-2 bg-red-600/20 text-red-400 hover:bg-red-600 hover:text-white rounded border border-red-600/30 text-xs font-bold transition-colors">
                      AKTUALIZOVAT HESLO
                    </button>
                  </div>
                </div>

                <div class="flex justify-end pt-4 border-t border-gray-800">
                  <button type="submit" :disabled="isSaving" class="px-8 py-2.5 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-lg shadow-lg transition-transform hover:scale-105 disabled:opacity-50 disabled:scale-100">
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
const { updateProfile, getWatchlist, getCollections, changePassword, getReviews } = useApi();
const toast = useToast();

const isLoadingProfile = ref(true);
const isEditModalOpen = ref(false);
const isSaving = ref(false);
const showPasswordSection = ref(false);
const isChangingPassword = ref(false);

const editForm = reactive({
  username: '',
  bio: '',
});
const profilePictureFile = ref(null);
const coverPictureFile = ref(null);
const previewImageUrl = ref('');
const coverPreviewUrl = ref('');

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
});

const watchlistItems = ref([]);
const collections = ref([]);
const reviewCount = ref(0);

const openEditModal = () => {
  editForm.username = authStore.user.username;
  editForm.bio = authStore.user.bio;
  previewImageUrl.value = '';
  coverPreviewUrl.value = '';
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
    const reader = new FileReader();
    reader.onload = (e) => {
      coverPreviewUrl.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const saveProfile = async () => {
  isSaving.value = true;
  const formData = new FormData();
  formData.append('username', editForm.username);
  formData.append('bio', editForm.bio);
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
    const [wRes, cRes, rRes] = await Promise.all([
      getWatchlist(),
      getCollections(),
      getReviews({ user: authStore.user?.id })
    ]);
    watchlistItems.value = wRes.data.results;
    collections.value = cRes.data.results.filter(c => c.user.id === authStore.user?.id);
    reviewCount.value = rRes.data.count || 0;
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
  return Math.floor(count / 5) + 1;
});

const topFavorites = computed(() => {
  return [...watchlistItems.value].reverse().slice(0, 5);
});

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.backdrop-blur-xl {
  backdrop-filter: blur(24px);
}
</style>