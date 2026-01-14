<template>
  <!-- Main Background: Dark gradient for better glassmorphism contrast -->
  <div class="bg-gray-100 dark:bg-gradient-to-br dark:from-gray-900 dark:to-gray-950 min-h-screen pb-12 transition-colors duration-500">
    <!-- Loading State -->
    <div v-if="isLoadingProfile" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>

    <div v-else-if="authStore.user">
      <!-- HERO SECTION -->
      <div class="relative w-full h-64 md:h-96 bg-gray-800 overflow-hidden group">
        <img 
          v-if="authStore.user.cover_picture" 
          :src="authStore.user.cover_picture" 
          class="w-full h-full object-cover transition-transform duration-1000 group-hover:scale-105"
          alt="Cover"
        >
        <div v-else class="w-full h-full bg-gradient-to-r from-slate-900 via-gray-800 to-slate-900 flex items-center justify-center">
          <span class="text-white/20 text-xl font-bold tracking-widest uppercase">CineSmart Profile</span>
        </div>
        
        <!-- Gradient Overlay -->
        <div class="absolute inset-0 bg-gradient-to-t from-gray-900 via-gray-900/40 to-transparent"></div>

        <button 
          @click="openEditModal"
          class="absolute top-4 right-4 bg-black/40 hover:bg-black/60 backdrop-blur-md text-white px-4 py-2 rounded-full text-sm font-medium transition-all flex items-center gap-2 border border-white/10 group/btn shadow-lg"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 group-hover/btn:rotate-12 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
          Upravit
        </button>
      </div>

      <!-- PROFILE INFO BAR -->
      <div class="container mx-auto px-4 relative -mt-24 mb-12 flex flex-col md:flex-row items-center md:items-end gap-8">
        <!-- Avatar with Frame -->
        <div class="relative flex-shrink-0 group">
          <div class="w-36 h-36 md:w-48 md:h-48 rounded-full p-1 bg-gradient-to-tr from-blue-500 via-purple-500 to-pink-500 shadow-2xl relative z-10">
            <div class="w-full h-full rounded-full overflow-hidden bg-gray-800 border-4 border-gray-900">
              <img 
                v-if="authStore.user.profile_picture" 
                :src="authStore.user.profile_picture" 
                class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                alt="Avatar"
              >
              <div v-else class="w-full h-full flex items-center justify-center text-white text-5xl font-bold bg-gray-700">
                {{ authStore.user.username.charAt(0).toUpperCase() }}
              </div>
            </div>
          </div>
          <!-- Level Badge -->
          <div class="absolute bottom-2 right-2 md:bottom-4 md:right-4 z-20 bg-gradient-to-br from-yellow-400 to-yellow-600 text-gray-900 font-black w-10 h-10 md:w-14 md:h-14 rounded-full flex items-center justify-center border-4 border-gray-900 shadow-xl text-sm md:text-lg cursor-help transform hover:scale-110 transition-transform" :title="'Level ' + userLevel">
            {{ userLevel }}
          </div>
        </div>

        <!-- Name, Bio & Stats -->
        <div class="flex-grow text-center md:text-left pb-2 w-full md:w-auto">
          <h1 class="text-4xl md:text-6xl font-black text-white drop-shadow-lg tracking-tight mb-2">{{ authStore.user.username }}</h1>
          <p class="text-gray-300/90 text-sm md:text-lg max-w-2xl mx-auto md:mx-0 font-medium leading-relaxed mb-4">{{ authStore.user.bio || 'Filmový nadšenec' }}</p>
          
          <!-- Stats Chips -->
          <div class="flex flex-wrap justify-center md:justify-start gap-3">
            <div class="bg-gray-900/60 backdrop-blur-md border border-gray-700/50 px-4 py-2 rounded-xl flex items-center gap-3 shadow-lg">
              <div class="p-1.5 bg-blue-500/20 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor"><path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z" /></svg>
              </div>
              <div class="flex flex-col items-start">
                <span class="text-white font-bold text-lg leading-none">{{ stats.totalCount }}</span>
                <span class="text-[10px] text-gray-400 uppercase font-bold tracking-wider">Filmů</span>
              </div>
            </div>
            <div class="bg-gray-900/60 backdrop-blur-md border border-gray-700/50 px-4 py-2 rounded-xl flex items-center gap-3 shadow-lg">
              <div class="p-1.5 bg-green-500/20 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" /></svg>
              </div>
              <div class="flex flex-col items-start">
                <span class="text-white font-bold text-lg leading-none">{{ stats.formattedTime }}</span>
                <span class="text-[10px] text-gray-400 uppercase font-bold tracking-wider">Čas</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- MAIN CONTENT LAYOUT -->
      <div class="container mx-auto px-4 grid grid-cols-1 lg:grid-cols-4 gap-8">
        
        <!-- LEFT COLUMN (Main - 3/4) -->
        <div class="lg:col-span-3 space-y-8">
          
          <!-- SHOWCASE: TOP OBLÍBENÉ (Glassmorphism) -->
          <div class="bg-white/80 dark:bg-gray-900/60 backdrop-blur-xl rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700/50 overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700/50 flex justify-between items-center bg-gray-50/50 dark:bg-white/5">
              <h2 class="text-lg font-bold text-gray-800 dark:text-white flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-500" viewBox="0 0 20 20" fill="currentColor"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" /></svg>
                Výstavka: Oblíbené
              </h2>
            </div>
            <div class="p-6">
              <div v-if="topFavorites.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
                <NuxtLink 
                  v-for="item in topFavorites" 
                  :key="item.id" 
                  :to="`/movies/${item.movie.id}`"
                  class="group relative aspect-[2/3] rounded-xl overflow-hidden shadow-lg transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:ring-2 hover:ring-blue-500 z-0 hover:z-10"
                >
                  <img :src="item.movie.poster" class="w-full h-full object-cover">
                  <!-- Overlay gradient on hover -->
                  <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-3">
                    <span class="text-white text-xs font-bold leading-tight">{{ item.movie.title }}</span>
                    <div class="w-full bg-gray-700 h-1 mt-2 rounded-full overflow-hidden">
                      <div class="bg-green-500 h-full w-full"></div>
                    </div>
                  </div>
                </NuxtLink>
              </div>
              <div v-else class="flex flex-col items-center justify-center py-12 text-gray-500 dark:text-gray-400/50">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mb-3 opacity-20" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
                <p class="text-sm font-medium">Zatím žádné oblíbené filmy</p>
              </div>
            </div>
          </div>

          <!-- SHOWCASE: KOLEKCE (Glassmorphism) -->
          <div class="bg-white/80 dark:bg-gray-900/60 backdrop-blur-xl rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700/50 overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700/50 flex justify-between items-center bg-gray-50/50 dark:bg-white/5">
              <h2 class="text-lg font-bold text-gray-800 dark:text-white flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-500" viewBox="0 0 20 20" fill="currentColor"><path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z" /></svg>
                Moje Kolekce
              </h2>
              <NuxtLink to="/collections" class="text-xs font-bold text-blue-600 hover:text-blue-400 uppercase tracking-wide transition-colors">Všechny kolekce</NuxtLink>
            </div>
            <div class="p-6">
              <div v-if="collections.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div 
                  v-for="collection in collections.slice(0, 4)" 
                  :key="collection.id" 
                  class="flex items-center gap-4 p-4 rounded-xl bg-gray-50 dark:bg-gray-800/40 hover:bg-gray-100 dark:hover:bg-gray-700/60 transition-all cursor-pointer border border-transparent hover:border-gray-300 dark:hover:border-gray-600 group"
                  @click="navigateTo(`/collections/${collection.id}`)"
                >
                  <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex-shrink-0 flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition-transform">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                  </div>
                  <div class="overflow-hidden">
                    <h4 class="font-bold text-gray-900 dark:text-white truncate group-hover:text-blue-400 transition-colors">{{ collection.name }}</h4>
                    <p class="text-xs text-gray-500">{{ collection.items.length }} položek</p>
                  </div>
                </div>
              </div>
              <div v-else class="flex flex-col items-center justify-center py-8 text-gray-500 dark:text-gray-400/50">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 mb-2 opacity-20" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" /></svg>
                <p class="text-sm">Žádné kolekce</p>
              </div>
            </div>
          </div>

        </div>

        <!-- RIGHT COLUMN (SIDEBAR - 1/4) -->
        <div class="lg:col-span-1 space-y-8">
          
          <!-- Odznaky (Glassmorphism) -->
          <div class="bg-white/80 dark:bg-gray-900/60 backdrop-blur-xl rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700/50 p-6">
            <h3 class="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-widest mb-4">Odznaky</h3>
            <div class="flex flex-wrap gap-2">
              <div class="bg-yellow-500/10 text-yellow-600 dark:text-yellow-400 px-3 py-1.5 rounded-lg text-xs font-bold border border-yellow-500/20 cursor-help transition-transform hover:scale-105" title="Získáno za aktivitu">
                🏆 Lvl {{ userLevel }}
              </div>
              <div v-if="stats.totalCount >= 50" class="bg-purple-500/10 text-purple-600 dark:text-purple-400 px-3 py-1.5 rounded-lg text-xs font-bold border border-purple-500/20">
                🎬 Cinephile
              </div>
              <div v-else class="bg-gray-500/10 text-gray-600 dark:text-gray-400 px-3 py-1.5 rounded-lg text-xs font-bold border border-gray-500/20">
                🐣 Začátečník
              </div>
              <div v-if="stats.favoriteGenre !== 'N/A'" class="bg-blue-500/10 text-blue-600 dark:text-blue-400 px-3 py-1.5 rounded-lg text-xs font-bold border border-blue-500/20">
                💙 {{ stats.favoriteGenre }}
              </div>
            </div>
          </div>

          <!-- Quick Links (Glassmorphism) -->
          <div class="bg-white/80 dark:bg-gray-900/60 backdrop-blur-xl rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700/50 overflow-hidden">
            <div class="p-2 space-y-1">
              <NuxtLink to="/watchlist" class="flex items-center justify-between px-4 py-3 rounded-xl hover:bg-white/50 dark:hover:bg-white/5 text-gray-700 dark:text-gray-200 transition group">
                <div class="flex items-center gap-3">
                  <div class="p-1.5 bg-gray-200 dark:bg-gray-800 rounded-lg group-hover:bg-blue-500 group-hover:text-white transition-colors text-gray-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" /></svg>
                  </div>
                  <span class="font-medium text-sm">Můj seznam</span>
                </div>
                <span class="text-xs font-bold bg-gray-200 dark:bg-gray-800 text-gray-600 dark:text-gray-400 px-2 py-0.5 rounded-md min-w-[24px] text-center">{{ watchlistItems.length }}</span>
              </NuxtLink>
              
              <NuxtLink to="/collections" class="flex items-center justify-between px-4 py-3 rounded-xl hover:bg-white/50 dark:hover:bg-white/5 text-gray-700 dark:text-gray-200 transition group">
                <div class="flex items-center gap-3">
                  <div class="p-1.5 bg-gray-200 dark:bg-gray-800 rounded-lg group-hover:bg-purple-500 group-hover:text-white transition-colors text-gray-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                  </div>
                  <span class="font-medium text-sm">Kolekce</span>
                </div>
                <span class="text-xs font-bold bg-gray-200 dark:bg-gray-800 text-gray-600 dark:text-gray-400 px-2 py-0.5 rounded-md min-w-[24px] text-center">{{ collections.length }}</span>
              </NuxtLink>
              
              <div class="flex items-center justify-between px-4 py-3 rounded-xl hover:bg-white/50 dark:hover:bg-white/5 text-gray-700 dark:text-gray-200 transition group cursor-not-allowed opacity-70">
                <div class="flex items-center gap-3">
                  <div class="p-1.5 bg-gray-200 dark:bg-gray-800 rounded-lg text-gray-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg>
                  </div>
                  <span class="font-medium text-sm">Recenze</span>
                </div>
                <span class="text-xs font-bold bg-gray-200 dark:bg-gray-800 text-gray-600 dark:text-gray-400 px-2 py-0.5 rounded-md min-w-[24px] text-center">{{ reviewCount }}</span>
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
          <div class="fixed inset-0 bg-gray-900/80 backdrop-blur-sm transition-opacity" @click="closeEditModal"></div>

          <div class="inline-block align-bottom bg-white dark:bg-gray-800 rounded-2xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full border border-gray-200 dark:border-gray-700">
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
                    <img :src="previewImageUrl || authStore.user.profile_picture || 'https://via.placeholder.com/50'" class="h-16 w-16 rounded-full object-cover border-2 border-gray-300 dark:border-gray-600">
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
                  <input type="text" v-model="editForm.username" class="mt-1 block w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 dark:text-white focus:ring-blue-500 focus:border-blue-500 transition-colors">
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Bio</label>
                  <textarea v-model="editForm.bio" rows="3" class="mt-1 block w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 dark:text-white focus:ring-blue-500 focus:border-blue-500 transition-colors"></textarea>
                </div>

                <!-- Password Change Toggle -->
                <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
                  <button type="button" @click="showPasswordSection = !showPasswordSection" class="text-blue-600 text-sm hover:underline font-medium">Změnit heslo</button>
                </div>

                <transition enter-active-class="duration-200 ease-out" enter-from-class="opacity-0 -translate-y-2" enter-to-class="opacity-100 translate-y-0" leave-active-class="duration-150 ease-in" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 -translate-y-2">
                  <div v-if="showPasswordSection" class="space-y-3 bg-gray-50 dark:bg-gray-700/50 p-4 rounded-lg border border-gray-200 dark:border-gray-600">
                    <input type="password" v-model="passwordForm.old_password" placeholder="Staré heslo" class="block w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 dark:text-white text-sm">
                    <input type="password" v-model="passwordForm.new_password" placeholder="Nové heslo" class="block w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 dark:text-white text-sm">
                    <input type="password" v-model="passwordForm.confirm_password" placeholder="Potvrdit nové heslo" class="block w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 dark:text-white text-sm">
                    <button type="button" @click="handleChangePassword" :disabled="isChangingPassword" class="w-full py-2 bg-red-500/10 text-red-600 border border-red-500/20 rounded text-sm hover:bg-red-500 hover:text-white transition-colors font-bold">Aktualizovat heslo</button>
                  </div>
                </transition>

                <div class="flex justify-end pt-4 border-t border-gray-200 dark:border-gray-700 mt-4">
                  <button type="submit" :disabled="isSaving" class="px-6 py-2.5 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-500 shadow-lg shadow-blue-500/30 disabled:opacity-50 transition-all transform hover:scale-105 active:scale-95">
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