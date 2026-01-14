<template>
  <nav class="bg-gray-900/95 backdrop-blur-md border-b border-gray-800 sticky top-0 z-50 transition-colors duration-300">
    <div class="container mx-auto px-4 h-16 flex items-center justify-between gap-4">

      <!-- 1. LOGO & BRANDING -->
      <NuxtLink to="/" class="flex-shrink-0 group">
        <span class="text-3xl font-black tracking-tighter text-white group-hover:text-blue-400 transition-all duration-300">
          Cine<span class="text-blue-600">Smart</span>
        </span>
      </NuxtLink>

      <!-- 2. SEARCH BAR (CENTERED) -->
      <div class="hidden md:flex flex-1 max-w-xl items-center justify-center px-4">
        <div class="relative w-full group">
          <form @submit.prevent="handleFilterChange">
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 group-focus-within:text-blue-500 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <input
                type="text"
                v-model="searchQuery"
                placeholder="Hledat filmy, seriály..."
                class="w-full pl-10 pr-20 py-2.5 bg-gray-800 border border-gray-700 text-gray-200 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all placeholder-gray-500 text-sm"
                @focus="onSearchFocus"
                @blur="onSearchBlur"
                autocomplete="off"
              />
              
              <!-- Ikony uvnitř vyhledávání -->
              <div class="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
                <!-- Random Button (Icon) -->
                <button 
                  @click.prevent="handleRandomPick"
                  title="Zkusit štěstí"
                  type="button"
                  class="p-1.5 text-gray-400 hover:text-white hover:bg-gray-700 rounded-full transition-colors"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                  </svg>
                </button>
                <!-- Filters Link (Icon) -->
                <NuxtLink 
                  to="/browse"
                  title="Filtry"
                  class="p-1.5 text-gray-400 hover:text-white hover:bg-gray-700 rounded-full transition-colors"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
                  </svg>
                </NuxtLink>
              </div>
            </div>
          </form>

          <!-- Search Results Dropdown -->
          <div v-if="isSearchFocused && (searchResults.length > 0 || isSearchLoading || searchQuery.length > 0)"
               class="absolute top-full left-0 right-0 mt-2 bg-gray-800 border border-gray-700 rounded-xl shadow-2xl z-50 overflow-hidden">
            <div v-if="isSearchLoading" class="p-4 text-gray-400 text-center text-sm">Načítání...</div>
            <div v-else-if="searchResults.length === 0 && searchQuery.length > 0" class="p-4 text-gray-400 text-center text-sm">Žádné výsledky.</div>
            <ul v-else class="max-h-96 overflow-y-auto">
              <li v-for="movie in searchResults" :key="movie.id" 
                  @click="selectMovie(movie)"
                  class="p-3 hover:bg-gray-700/50 cursor-pointer border-b border-gray-700/50 last:border-b-0 flex gap-3 items-center transition-colors">
                <img v-if="movie.poster" :src="movie.poster" class="h-14 w-10 object-cover rounded shadow-sm flex-shrink-0">
                <div v-else class="h-14 w-10 bg-gray-700 rounded shadow-sm flex-shrink-0"></div>
                <div class="min-w-0">
                  <p class="font-bold text-gray-100 text-sm truncate">{{ movie.title }}</p>
                  <div class="flex items-center gap-2 mt-0.5">
                    <span class="text-[10px] uppercase font-bold px-1.5 py-0.5 rounded bg-gray-700 text-gray-300">
                      {{ movie.type === 'series' ? 'TV' : 'Film' }}
                    </span>
                    <p v-if="movie.release_date" class="text-xs text-gray-500">{{ movie.release_date.substring(0, 4) }}</p>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 3. RIGHT SIDE: ACTIONS -->
      <div class="flex items-center gap-6">
        
        <!-- Mobile Search Toggle (Visible only on small screens) -->
        <button class="md:hidden text-gray-300 hover:text-white" @click="toggleMobileSearch">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </button>

        <!-- AUTH STATE: LOGGED OUT -->
        <template v-if="!authStore.isLoggedIn">
          <div class="flex items-center gap-4">
            <a @click.prevent="openAuthModal('login')" href="#" class="text-sm font-medium text-gray-300 hover:text-white transition-colors hidden sm:block">
              Přihlásit
            </a>
            <button @click="openAuthModal('register')" class="px-5 py-2 bg-blue-600 hover:bg-blue-500 text-white text-sm font-bold rounded-full transition-all transform hover:scale-105 shadow-lg shadow-blue-900/20">
              Registrovat
            </button>
          </div>
        </template>

        <!-- AUTH STATE: LOGGED IN (DROPDOWN) -->
        <template v-else>
          <div class="relative" ref="dropdownRef">
            <button 
              @click="toggleUserDropdown" 
              class="flex items-center gap-2 group focus:outline-none"
            >
              <img 
                v-if="authStore.user && authStore.user.profile_picture" 
                :src="authStore.user.profile_picture" 
                alt="Profile" 
                class="h-9 w-9 rounded-full object-cover border-2 border-transparent group-hover:border-blue-500 transition-all"
              >
              <div v-else class="h-9 w-9 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold text-sm">
                {{ authStore.user?.username?.charAt(0).toUpperCase() }}
              </div>
              
              <span class="hidden lg:block text-sm font-medium text-gray-200 group-hover:text-white transition-colors max-w-[100px] truncate">
                {{ authStore.user?.username }}
              </span>
              
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400 group-hover:text-white transition-colors transform" :class="{'rotate-180': isUserDropdownOpen}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <!-- DROPDOWN MENU -->
            <transition
              enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <div v-if="isUserDropdownOpen" class="absolute right-0 mt-2 w-56 bg-gray-800 rounded-xl shadow-2xl border border-gray-700 py-2 z-50 overflow-hidden">
                <div class="px-4 py-3 border-b border-gray-700 mb-1">
                  <p class="text-xs text-gray-400">Přihlášen jako</p>
                  <p class="text-sm font-bold text-white truncate">{{ authStore.user?.username }}</p>
                </div>
                
                <NuxtLink to="/profile" class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-300 hover:bg-gray-700 hover:text-white transition-colors" @click="isUserDropdownOpen = false">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 opacity-70" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
                  Můj profil
                </NuxtLink>
                
                <NuxtLink to="/watchlist" class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-300 hover:bg-gray-700 hover:text-white transition-colors" @click="isUserDropdownOpen = false">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 opacity-70" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" /></svg>
                  Můj seznam
                </NuxtLink>
                
                <NuxtLink to="/collections" class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-300 hover:bg-gray-700 hover:text-white transition-colors" @click="isUserDropdownOpen = false">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 opacity-70" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                  Kolekce
                </NuxtLink>

                <div class="border-t border-gray-700 my-1"></div>
                
                <a @click.prevent="handleLogout" href="#" class="flex items-center gap-3 px-4 py-2.5 text-sm text-red-400 hover:bg-gray-700 hover:text-red-300 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 opacity-70" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
                  Odhlásit se
                </a>
              </div>
            </transition>
          </div>
        </template>

        <!-- THEME TOGGLE (Visible always) -->
        <button 
          @click="toggleTheme" 
          class="p-2 text-gray-400 hover:text-yellow-400 hover:bg-gray-800 rounded-full transition-colors" 
          title="Přepnout motiv"
        >
          <svg v-if="colorMode.value === 'dark'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707m-12.728 0l-.707-.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21 a9.003 9.003 0 008.354-5.646z" />
          </svg>
        </button>

      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, watch, inject, onUnmounted } from 'vue';
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
const isUserDropdownOpen = ref(false);
const dropdownRef = ref(null);
let debounceTimer = null;

const toggleTheme = () => {
  colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark';
};

const toggleUserDropdown = () => {
  isUserDropdownOpen.value = !isUserDropdownOpen.value;
};

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isUserDropdownOpen.value = false;
  }
};

const toggleMobileSearch = () => {
  // TODO: Implement mobile search overlay if needed
  alert("Vyhledávání na mobilu bude brzy dostupné.");
};

const handleRandomPick = async () => {
  try {
    const randomId = await getRandomMovieId();
    if (randomId) {
      router.push(`/movies/${randomId}`); // Fallback logic in detail page handles redirection if needed
    }
  } catch (err) {
    console.error('Error during random pick:', err);
  }
};

const handleLogout = () => {
  isUserDropdownOpen.value = false;
  authStore.logout();
  router.push('/');
};

const handleFilterChange = () => {
  if (!searchQuery.value) return;
  router.push({ path: '/browse', query: { search: searchQuery.value } });
  isSearchFocused.value = false;
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

const selectMovie = (movie) => {
  searchQuery.value = '';
  searchResults.value = [];
  isSearchFocused.value = false;
  if (movie.type === 'series') {
    router.push(`/series/${movie.id}`);
  } else {
    router.push(`/movies/${movie.id}`);
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>