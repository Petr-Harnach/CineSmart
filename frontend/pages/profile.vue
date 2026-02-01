<template>
  <!-- Main Background: Dark gradient restored -->
  <div class="bg-gray-100 dark:bg-gradient-to-br dark:from-gray-900 dark:via-gray-950 dark:to-black min-h-screen pb-12 transition-colors duration-500">
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
          <div v-else class="w-full h-full bg-gray-800 flex items-center justify-center">
            <span class="text-gray-600 text-lg">Bez pozadí</span>
          </div>
          <!-- Gradient pro čitelnost -->
          <div class="absolute inset-0 bg-gradient-to-t from-[#141419] via-transparent to-transparent opacity-90"></div>
        </div>

        <button 
          @click="openEditModal"
          class="absolute top-6 right-6 bg-black/50 hover:bg-black/70 backdrop-blur-md text-white px-5 py-2 rounded-full text-sm font-semibold transition-all flex items-center gap-2 border border-white/20 shadow-lg z-30"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
          Upravit profil
        </button>
      </div>

      <!-- PROFILE INFO BAR -->
      <div class="container mx-auto px-4 relative -mt-24 mb-12 flex flex-col md:flex-row items-center md:items-end gap-8 z-20">
        <!-- Avatar (Circle + Thin Black Frame) -->
        <div class="relative flex-shrink-0">
          <div class="w-40 h-40 md:w-48 md:h-48 rounded-full p-0.5 bg-black shadow-2xl relative z-10">
            <div class="w-full h-full rounded-full overflow-hidden bg-gray-800 border-2 border-gray-900">
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
          <div class="absolute bottom-2 right-2 z-20 bg-yellow-500 text-gray-900 font-bold w-8 h-8 md:w-10 md:h-10 rounded-full flex items-center justify-center border-2 border-gray-900 shadow-lg cursor-help text-sm" :title="'Level ' + userLevel">
            {{ userLevel }}
          </div>
        </div>

        <!-- Name, Bio & Stats -->
        <div class="flex-grow text-center md:text-left pb-4">
          <!-- Standardní font, Bold (ne Black/Italic) -->
          <h1 class="text-4xl md:text-5xl font-bold text-white drop-shadow-md mb-2">
            {{ authStore.user.username }}
          </h1>
          <p class="text-gray-300 text-sm md:text-base max-w-2xl mx-auto md:mx-0 leading-relaxed mb-4 font-medium">
            Tento uživatel zatím nemá žádný příběh...
          </p>
          
          <!-- Stats Chips -->
          <div class="flex flex-wrap justify-center md:justify-start gap-3">
            <div class="bg-gray-800/80 backdrop-blur border border-gray-700 px-4 py-2 rounded-lg flex items-center gap-3 shadow-lg">
              <span class="text-white font-bold text-lg">{{ stats.totalCount }}</span>
              <span class="text-xs text-gray-400 font-semibold tracking-wide">Filmů</span>
            </div>
            <div class="bg-gray-800/80 backdrop-blur border border-gray-700 px-4 py-2 rounded-lg flex items-center gap-3 shadow-lg">
              <span class="text-white font-bold text-lg">{{ stats.formattedTime }}</span>
              <span class="text-xs text-gray-400 font-semibold tracking-wide">Čas</span>
            </div>
          </div>
        </div>
      </div>

      <!-- MAIN CONTENT LAYOUT -->
      <div class="container mx-auto px-4 grid grid-cols-1 lg:grid-cols-4 gap-8">
        
        <!-- LEFT COLUMN (Showcases) -->
        <div class="lg:col-span-3 space-y-10">
          
          <!-- SHOWCASE: TOP OBLÍBENÉ -->
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

          <!-- SHOWCASE: KOLEKCE -->
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
                  <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex-shrink-0 flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition-transform">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                  </div>
                  <div class="overflow-hidden">
                    <h4 class="font-bold text-gray-900 dark:text-white truncate group-hover:text-blue-400 transition-colors">{{ collection.name }}</h4>
                    <p class="text-xs text-gray-500">{{ collection.items.length }} položek</p>
                  </div>
                </div>
              </div>
              <div v-else class="flex flex-col items-center justify-center py-8 opacity-50">
                <p class="text-sm font-medium text-gray-400">Žádné kolekce</p>
              </div>
            </div>
          </div>

        </div>

        <!-- RIGHT COLUMN (Sidebar) -->
        <div class="lg:col-span-1 space-y-8">
          
          <!-- Odznaky -->
          <div class="bg-white/5 dark:bg-gray-900/60 backdrop-blur-xl rounded-xl shadow-xl border border-gray-200 dark:border-gray-700/50 p-6">
            <h3 class="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-widest mb-4">Úspěchy</h3>
            <div class="flex flex-col gap-3">
              <div class="bg-yellow-500/10 p-3 rounded-lg border border-yellow-500/20 flex items-center gap-3">
                <span class="text-xl">⭐</span>
                <div>
                  <p class="text-white font-bold text-xs">Úroveň {{ userLevel }}</p>
                  <p class="text-[10px] text-yellow-500 font-bold uppercase">{{ levelTitle }}</p>
                </div>
              </div>
              <div v-if="stats.totalCount >= 50" class="bg-purple-500/10 p-3 rounded-lg border border-purple-500/20 flex items-center gap-3">
                <span class="text-xl">🎬</span>
                <div>
                  <p class="text-white font-bold text-xs">Cinephile</p>
                  <p class="text-[10px] text-purple-500 font-bold uppercase">50+ zhlédnutí</p>
                </div>
              </div>
              <div v-if="stats.favoriteGenre !== 'N/A'" class="bg-blue-500/10 p-3 rounded-lg border border-blue-500/20 flex items-center gap-3">
                <span class="text-xl">💙</span>
                <div>
                  <p class="text-white font-bold text-sm">{{ stats.favoriteGenre }}</p>
                  <p class="text-[10px] text-blue-500 font-bold uppercase">Oblíbený žánr</p>
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

    <!-- EDIT PROFILE MODAL (VRÁCENO ZPĚT + STANDARDNÍ FONT) -->
    <transition enter-active-class="duration-300 ease-out" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100" leave-active-class="duration-200 ease-in" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
      <div v-if="isEditModalOpen" class="fixed inset-0 z-[100] overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <div class="flex items-center justify-center min-h-screen px-4 text-center">
          <div class="fixed inset-0 bg-black/90 backdrop-blur-md transition-opacity" @click="closeEditModal"></div>

          <div class="inline-block align-bottom bg-[#111827] rounded-[2rem] text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full border border-white/10">
            <div class="px-8 py-8">
              <div class="flex justify-between items-center mb-8">
                <!-- Standardní font -->
                <h3 class="text-2xl font-bold text-white">Nastavení Profilu</h3>
                <button @click="closeEditModal" class="p-2 text-gray-400 hover:text-white hover:bg-white/5 rounded-full transition-all">
                  <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
              </div>

              <form @submit.prevent="saveProfile" class="space-y-6">
                
                <!-- COVER IMAGE SETTINGS (Vizuální editor vrácen) -->
                <div>
                  <label class="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Pozadí profilu (Cover)</label>
                  <p class="text-xs text-gray-500 mb-2">Doporučená velikost: 1920x500 px. Max 2MB.</p>
                  
                  <div class="relative h-32 w-full rounded-2xl overflow-hidden bg-gray-800 border-2 border-dashed border-white/10 hover:border-blue-500 transition-colors group/cover cursor-pointer">
                    <!-- Preview -->
                    <img v-if="coverPreviewUrl || authStore.user.cover_picture" :src="coverPreviewUrl || authStore.user.cover_picture" class="w-full h-full object-cover">
                    
                    <!-- Overlay with input -->
                    <div class="absolute inset-0 bg-black/40 flex flex-col items-center justify-center opacity-0 group-hover/cover:opacity-100 transition-opacity">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                      <span class="text-white text-xs font-bold">Nahrát obrázek</span>
                      <input type="file" @change="handleCoverChange" accept="image/*" class="absolute inset-0 opacity-0 cursor-pointer">
                    </div>
                  </div>
                </div>

                <!-- AVATAR SETTINGS (Vizuální editor vrácen) -->
                <div>
                  <label class="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Avatar</label>
                  <p class="text-xs text-gray-500 mb-2">Doporučená velikost: 500x500 px (Čtverec). Max 2MB.</p>
                  
                  <div class="flex items-end gap-6">
                    <div class="relative group/avatar flex-shrink-0">
                      <div class="w-24 h-24 rounded-full overflow-hidden bg-gray-800 border-4 border-[#1a1a21] shadow-2xl relative">
                        <img :src="previewImageUrl || authStore.user.profile_picture || 'https://via.placeholder.com/100'" class="w-full h-full object-cover">
                        <div class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover/avatar:opacity-100 transition-opacity">
                          <input type="file" @change="handleFileChange" accept="image/*" class="absolute inset-0 opacity-0 cursor-pointer">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                        </div>
                      </div>
                    </div>
                    <div class="flex-grow">
                      <label class="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Uživatelské jméno</label>
                      <input type="text" v-model="editForm.username" class="w-full p-3 bg-white/5 border border-white/10 rounded-xl text-white font-bold focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all">
                    </div>
                  </div>
                </div>

                <!-- Password Toggle -->
                <div class="border-t border-gray-800 pt-4">
                  <button type="button" @click="showPasswordSection = !showPasswordSection" class="text-xs font-bold text-blue-400 hover:text-blue-300 uppercase tracking-wider">
                    {{ showPasswordSection ? 'Skrýt změnu hesla' : 'Změnit heslo' }}
                  </button>
                  
                  <div v-if="showPasswordSection" class="mt-4 p-6 bg-black/20 rounded-2xl border border-white/5 space-y-4">
                    <input type="password" v-model="passwordForm.old_password" placeholder="Současné heslo" class="w-full p-3 bg-white/5 border border-white/10 rounded-xl text-white text-sm focus:ring-2 focus:ring-red-500/50 focus:outline-none transition-all">
                    <div class="grid grid-cols-2 gap-4">
                      <input type="password" v-model="passwordForm.new_password" placeholder="Nové heslo" class="w-full p-3 bg-white/5 border border-white/10 rounded-xl text-white text-sm focus:ring-2 focus:ring-red-500/50 focus:outline-none transition-all">
                      <input type="password" v-model="passwordForm.confirm_password" placeholder="Potvrdit nové" class="w-full p-3 bg-white/5 border border-white/10 rounded-xl text-white text-sm focus:ring-2 focus:ring-red-500/50 focus:outline-none transition-all">
                    </div>
                    <button type="button" @click="handleChangePassword" :disabled="isChangingPassword" class="w-full py-3 bg-red-600/10 hover:bg-red-600 text-red-500 hover:text-white font-bold uppercase tracking-widest rounded-xl transition-all border border-red-600/20 text-xs">
                      Aktualizovat heslo
                    </button>
                  </div>
                </div>

                <div class="flex justify-end pt-6 border-t border-gray-800 mt-4">
                  <button type="submit" :disabled="isSaving" class="px-10 py-4 bg-blue-600 hover:bg-blue-500 text-white font-bold uppercase tracking-widest rounded-2xl shadow-2xl shadow-blue-600/20 transition-all transform hover:scale-105 active:scale-95 disabled:opacity-50">
                    {{ isSaving ? 'Ukládám...' : 'Uložit Profil' }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- CROPPER MODAL -->
    <transition enter-active-class="duration-300 ease-out" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100" leave-active-class="duration-200 ease-in" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
      <div v-if="isCropperModalOpen" class="fixed inset-0 z-[101] overflow-y-auto" aria-labelledby="cropper-modal-title" role="dialog" aria-modal="true">
        <div class="flex items-center justify-center min-h-screen px-4 text-center">
          <div class="fixed inset-0 bg-black/90 backdrop-blur-md transition-opacity" @click="closeCropperModal"></div>

          <div class="inline-block align-bottom bg-[#111827] rounded-[2rem] text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full md:max-w-3xl border border-white/10">
            <div class="px-8 py-8">
              <div class="flex justify-between items-center mb-8">
                <h3 class="text-2xl font-bold text-white">Oříznout obrázek</h3>
                <button @click="closeCropperModal" class="p-2 text-gray-400 hover:text-white hover:bg-white/5 rounded-full transition-all">
                  <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
              </div>

              <div class="cropper-wrapper">
                <Cropper
                  ref="cropperRef"
                  :src="imageToCrop"
                  :stencil-props="{ aspectRatio: cropperAspectRatio }"
                  image-restriction="stencil"
                  class="cropper"
                />
              </div>

              <div class="flex justify-end gap-4 pt-6 border-t border-gray-800 mt-4">
                <button type="button" @click="closeCropperModal" class="px-6 py-3 text-gray-400 hover:text-white font-bold uppercase tracking-widest rounded-xl transition-all text-xs">
                  Zrušit
                </button>
                <button type="button" @click="cropImage" class="px-8 py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold uppercase tracking-widest rounded-xl shadow-lg shadow-blue-600/20 transition-all text-xs">
                  Oříznout a uložit
                  </button>
              </div>
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
import { Cropper } from 'vue-advanced-cropper';
import 'vue-advanced-cropper/dist/style.css';

const authStore = useAuthStore();
const { updateProfile, getWatchlist, getCollections, changePassword, getReviews } = useApi();
const toast = useToast();

const isLoadingProfile = ref(true);
const isEditModalOpen = ref(false);
const isSaving = ref(false);
const showPasswordSection = ref(false);
const isChangingPassword = ref(false);

// Cropper State
const isCropperModalOpen = ref(false);
const imageToCrop = ref(null);
const cropperCallback = ref(null);
const cropperAspectRatio = ref(null);
const cropperRef = ref(null); // Ref to the cropper component

const editForm = reactive({
  username: '',
  // bio: '', // REMOVED
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
  // editForm.bio = authStore.user.bio; // REMOVED
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

// New functions for cropper
const openCropper = (image, callback, aspectRatio) => {
  imageToCrop.value = image;
  cropperCallback.value = callback;
  cropperAspectRatio.value = aspectRatio;
  isCropperModalOpen.value = true;
};

const closeCropperModal = () => {
  isCropperModalOpen.value = false;
  imageToCrop.value = null;
  cropperCallback.value = null;
  cropperAspectRatio.value = null;
};

const cropImage = () => {
  if (cropperRef.value && cropperCallback.value) {
    const { canvas } = cropperRef.value.getResult();
    if (canvas) {
      canvas.toBlob((blob) => {
        cropperCallback.value(blob);
        closeCropperModal();
      }, 'image/png');
    }
  }
};

const handleCroppedProfilePicture = (blob) => {
  profilePictureFile.value = blob;
  previewImageUrl.value = URL.createObjectURL(blob);
};

const handleCroppedCoverPicture = (blob) => {
  coverPictureFile.value = blob;
  coverPreviewUrl.value = URL.createObjectURL(blob);
};

// Modified handleFileChange and handleCoverChange
const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      openCropper(e.target.result, handleCroppedProfilePicture, 1); // 1:1 aspect ratio for profile picture
    };
    reader.readAsDataURL(file);
    event.target.value = ''; // Clear the input so the same file can be selected again
  }
};

const handleCoverChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      openCropper(e.target.result, handleCroppedCoverPicture, 1920 / 500); // aspect ratio for cover picture
    };
    reader.readAsDataURL(file);
    event.target.value = ''; // Clear the input so the same file can be selected again
  }
};

const saveProfile = async () => {
  isSaving.value = true;
  const formData = new FormData();
  formData.append('username', editForm.username);
  // formData.append('bio', editForm.bio); // REMOVED
  if (profilePictureFile.value) {
    formData.append('profile_picture', profilePictureFile.value, 'profile.png');
  }
  if (coverPictureFile.value) {
    formData.append('cover_picture', coverPictureFile.value, 'cover.png');
  }

  try {
    await updateProfile(formData);
    await authStore.fetchProfile();
    toast.success('Profil uložen!');
    closeEditModal();
  }
   catch (err) {
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

const levelTitle = computed(() => {
  if (userLevel.value < 5) return 'Začátečník';
  if (userLevel.value < 10) return 'Filmový Fanoušek';
  if (userLevel.value < 20) return 'Kritik';
  return 'Filmový Mistr';
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

/* Styles for the Cropper to ensure it's visible and functional */
.cropper-wrapper {
  max-width: 100%;
  max-height: 50vh; /* Adjust as needed */
  margin: 0 auto;
  background-color: #333; /* Dark background for cropper */
}

.cropper {
  height: 300px; /* Or a flexible height */
  width: 100%;
}
</style>