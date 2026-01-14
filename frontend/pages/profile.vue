<template>
  <!-- Main Background: Dark gradient for high-end feel -->
  <div class="bg-gray-100 dark:bg-gradient-to-br dark:from-gray-900 dark:via-gray-950 dark:to-black min-h-screen pb-12 transition-colors duration-500">
    <!-- Loading State -->
    <div v-if="isLoadingProfile" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>

    <div v-else-if="authStore.user">
      <!-- HERO SECTION (STEAM STYLE) -->
      <div class="relative w-full h-64 md:h-[450px] bg-gray-950 overflow-hidden group">
        <!-- Cover Image with Smooth Fade -->
        <div class="absolute inset-0">
          <img 
            v-if="authStore.user.cover_picture" 
            :src="authStore.user.cover_picture" 
            class="w-full h-full object-cover transition-transform duration-[2000ms] group-hover:scale-110"
            alt="Cover"
          >
          <!-- The "Steam Fade" Gradient: Fades to background color at the bottom -->
          <div class="absolute inset-0 bg-gradient-to-t from-[#141419] via-transparent to-transparent opacity-100"></div>
          <div class="absolute inset-0 bg-gradient-to-b from-black/20 via-transparent to-transparent"></div>
        </div>

        <button 
          @click="openEditModal"
          class="absolute top-6 right-6 bg-black/40 hover:bg-blue-600/60 backdrop-blur-xl text-white px-6 py-2.5 rounded-full text-sm font-bold transition-all flex items-center gap-2 border border-white/10 shadow-2xl z-30 group/btn"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 group-hover/btn:rotate-90 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
          Upravit profil
        </button>
      </div>

      <!-- PROFILE INFO BAR -->
      <div class="container mx-auto px-4 relative -mt-28 md:-mt-36 mb-12 flex flex-col md:flex-row items-center md:items-end gap-8 z-20">
        <!-- Avatar with Black Frame -->
        <div class="relative flex-shrink-0 group">
          <div class="w-40 h-40 md:w-56 md:h-56 rounded-full p-1.5 bg-black shadow-[0_0_50px_rgba(0,0,0,0.5)] transform -rotate-3 group-hover:rotate-0 transition-transform duration-500">
            <div class="w-full h-full rounded-full overflow-hidden bg-[#141419] border-4 border-[#141419]">
              <img 
                v-if="authStore.user.profile_picture" 
                :src="authStore.user.profile_picture" 
                class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                alt="Avatar"
              >
              <div v-else class="w-full h-full flex items-center justify-center text-white text-6xl font-black bg-slate-800">
                {{ authStore.user.username.charAt(0).toUpperCase() }}
              </div>
            </div>
          </div>
          <!-- Level Badge -->
          <div class="absolute -bottom-2 -right-2 md:bottom-0 md:right-0 z-30 bg-gradient-to-br from-yellow-400 to-orange-600 text-gray-900 font-black w-12 h-12 md:w-16 md:h-16 rounded-full flex items-center justify-center border-4 border-[#141419] shadow-2xl text-lg md:text-2xl transform rotate-12 group-hover:rotate-0 transition-all">
            {{ userLevel }}
          </div>
        </div>

        <!-- Name, Bio & Stats -->
        <div class="flex-grow text-center md:text-left pb-4">
          <h1 class="text-4xl md:text-7xl font-black text-white drop-shadow-[0_5px_15px_rgba(0,0,0,0.5)] tracking-tighter mb-3">
            {{ authStore.user.username }}
          </h1>
          <p class="text-gray-300 text-sm md:text-xl max-w-2xl mx-auto md:mx-0 font-medium leading-relaxed mb-6 drop-shadow-md">
            {{ authStore.user.bio || 'Tento uživatel zatím nemá žádný příběh...' }}
          </p>
          
          <!-- Modern Stats Chips -->
          <div class="flex flex-wrap justify-center md:justify-start gap-4">
            <div class="bg-white/5 backdrop-blur-2xl border border-white/10 px-5 py-2.5 rounded-2xl flex items-center gap-4 shadow-2xl">
              <div class="p-2 bg-blue-500/20 rounded-xl">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" /></svg>
              </div>
              <div class="flex flex-col">
                <span class="text-white font-black text-xl leading-none">{{ stats.totalCount }}</span>
                <span class="text-[10px] text-gray-400 uppercase font-black tracking-tighter mt-1">Filmotéka</span>
              </div>
            </div>
            <div class="bg-white/5 backdrop-blur-2xl border border-white/10 px-5 py-2.5 rounded-2xl flex items-center gap-4 shadow-2xl">
              <div class="p-2 bg-emerald-500/20 rounded-xl">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 2m6-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              </div>
              <div class="flex flex-col">
                <span class="text-white font-black text-xl leading-none">{{ stats.formattedTime }}</span>
                <span class="text-[10px] text-gray-400 uppercase font-black tracking-tighter mt-1">U obrazovky</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- MAIN CONTENT LAYOUT -->
      <div class="container mx-auto px-4 grid grid-cols-1 lg:grid-cols-4 gap-8">
        
        <!-- LEFT COLUMN (Showcases) -->
        <div class="lg:col-span-3 space-y-10">
          
          <!-- SHOWCASE: TOP OBLÍBENÉ (Glassmorphism) -->
          <div class="bg-white/[0.03] backdrop-blur-2xl rounded-3xl shadow-2xl border border-white/10 overflow-hidden transition-all duration-500">
            <div class="px-8 py-5 border-b border-white/5 flex justify-between items-center bg-white/[0.02]">
              <h2 class="text-xl font-black text-white flex items-center gap-3 tracking-tight uppercase italic">
                <span class="w-2 h-8 bg-blue-600 rounded-full"></span>
                Top Výstavka
              </h2>
            </div>
            <div class="p-8">
              <div v-if="topFavorites.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-6">
                <NuxtLink 
                  v-for="item in topFavorites" 
                  :key="item.id" 
                  :to="`/movies/${item.movie.id}`"
                  class="group relative aspect-[2/3] rounded-2xl overflow-hidden shadow-2xl transition-all duration-500 hover:scale-110 hover:ring-4 hover:ring-blue-500/50 z-0 hover:z-10"
                >
                  <img :src="item.movie.poster" class="w-full h-full object-cover">
                  <div class="absolute inset-0 bg-gradient-to-t from-black via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-all duration-300 flex flex-col justify-end p-4">
                    <span class="text-white text-sm font-black leading-tight drop-shadow-md">{{ item.movie.title }}</span>
                  </div>
                </NuxtLink>
              </div>
              <div v-else class="flex flex-col items-center justify-center py-16 text-gray-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mb-4 opacity-10" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <p class="text-lg font-bold opacity-30">Zatím žádné oblíbené kousky</p>
              </div>
            </div>
          </div>

          <!-- SHOWCASE: KOLEKCE (Glassmorphism) -->
          <div class="bg-white/[0.03] backdrop-blur-2xl rounded-3xl shadow-2xl border border-white/10 overflow-hidden">
            <div class="px-8 py-5 border-b border-white/5 flex justify-between items-center bg-white/[0.02]">
              <h2 class="text-xl font-black text-white flex items-center gap-3 tracking-tight uppercase italic">
                <span class="w-2 h-8 bg-purple-600 rounded-full"></span>
                Moje Kolekce
              </h2>
              <NuxtLink to="/collections" class="text-[10px] font-black text-blue-400 hover:text-white uppercase tracking-[0.2em] transition-all">Zobrazit vše &rarr;</NuxtLink>
            </div>
            <div class="p-8">
              <div v-if="collections.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div 
                  v-for="collection in collections.slice(0, 4)" 
                  :key="collection.id" 
                  class="flex items-center gap-5 p-5 rounded-2xl bg-white/[0.03] hover:bg-white/[0.08] transition-all cursor-pointer border border-white/5 hover:border-white/20 group"
                  @click="navigateTo(`/collections/${collection.id}`)"
                >
                  <div class="w-16 h-16 bg-gradient-to-br from-indigo-600 to-blue-700 rounded-2xl flex-shrink-0 flex items-center justify-center text-white shadow-2xl group-hover:scale-110 transition-transform duration-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                  </div>
                  <div class="overflow-hidden">
                    <h4 class="font-black text-white text-lg truncate group-hover:text-blue-400 transition-colors">{{ collection.name }}</h4>
                    <p class="text-xs text-gray-400 font-bold uppercase tracking-wider">{{ collection.items.length }} položek</p>
                  </div>
                </div>
              </div>
              <div v-else class="flex flex-col items-center justify-center py-10 opacity-30">
                <p class="text-sm font-black uppercase tracking-widest text-white">Žádné kolekce</p>
              </div>
            </div>
          </div>

        </div>

        <!-- RIGHT COLUMN (Sidebar) -->
        <div class="lg:col-span-1 space-y-8">
          
          <!-- Odznaky -->
          <div class="bg-white/[0.03] backdrop-blur-2xl rounded-3xl shadow-2xl border border-white/10 p-8">
            <h3 class="text-[10px] font-black text-gray-500 uppercase tracking-[0.3em] mb-6">Úspěchy</h3>
            <div class="flex flex-col gap-4">
              <div class="bg-yellow-500/10 p-4 rounded-2xl border border-yellow-500/20 flex items-center gap-4 transition-transform hover:scale-105">
                <span class="text-2xl">👑</span>
                <div>
                  <p class="text-white font-black text-sm">Úroveň {{ userLevel }}</p>
                  <p class="text-[10px] text-yellow-500 uppercase font-black">Filmový Mistr</p>
                </div>
              </div>
              <div v-if="stats.totalCount >= 50" class="bg-purple-500/10 p-4 rounded-2xl border border-purple-500/20 flex items-center gap-4">
                <span class="text-2xl">🎬</span>
                <div>
                  <p class="text-white font-black text-sm">Cinephile</p>
                  <p class="text-[10px] text-purple-500 uppercase font-black">50+ zhlédnutí</p>
                </div>
              </div>
              <div v-else class="bg-gray-500/10 p-4 rounded-2xl border border-gray-500/20 flex items-center gap-4 opacity-70">
                <span class="text-xl">🐣</span>
                <div>
                  <p class="text-white font-black text-sm">Začátečník</p>
                  <p class="text-[10px] text-gray-400 uppercase font-black">Méně než 50 filmů</p>
                </div>
              </div>
              <div v-if="stats.favoriteGenre !== 'N/A'" class="bg-blue-500/10 p-4 rounded-2xl border border-blue-500/20 flex items-center gap-4">
                <span class="text-2xl">💙</span>
                <div>
                  <p class="text-white font-black text-sm">{{ stats.favoriteGenre }}</p>
                  <p class="text-[10px] text-blue-500 uppercase font-black">Nejoblíbenější žánr</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Links -->
          <div class="bg-white/[0.03] backdrop-blur-2xl rounded-3xl shadow-2xl border border-white/10 overflow-hidden p-2">
            <NuxtLink to="/watchlist" class="flex items-center justify-between px-6 py-4 rounded-2xl hover:bg-white/10 text-gray-300 hover:text-white transition-all group">
              <div class="flex items-center gap-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 group-hover:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" /></svg>
                <span class="font-black text-sm uppercase tracking-wider">Můj seznam</span>
              </div>
              <span class="text-xs font-black bg-white/10 px-3 py-1 rounded-full">{{ watchlistItems.length }}</span>
            </NuxtLink>
            
            <NuxtLink to="/collections" class="flex items-center justify-between px-6 py-4 rounded-2xl hover:bg-white/10 text-gray-300 hover:text-white transition-all group">
              <div class="flex items-center gap-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 group-hover:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                <span class="font-black text-sm uppercase tracking-wider">Kolekce</span>
              </div>
              <span class="text-xs font-black bg-white/10 px-3 py-1 rounded-full">{{ collections.length }}</span>
            </NuxtLink>
            
            <div class="flex items-center justify-between px-6 py-4 rounded-2xl opacity-40 grayscale group">
              <div class="flex items-center gap-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg>
                <span class="font-black text-sm uppercase tracking-wider">Recenze</span>
              </div>
              <span class="text-xs font-black bg-white/10 px-3 py-1 rounded-full">{{ reviewCount }}</span>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- EDIT PROFILE MODAL (With Fixed Previews) -->
    <transition enter-active-class="duration-300 ease-out" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100" leave-active-class="duration-200 ease-in" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
      <div v-if="isEditModalOpen" class="fixed inset-0 z-[100] overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <div class="flex items-center justify-center min-h-screen px-4 text-center">
          <div class="fixed inset-0 bg-black/90 backdrop-blur-md transition-opacity" @click="closeEditModal"></div>

          <div class="inline-block align-bottom bg-[#1a1a21] rounded-[2rem] text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full border border-white/10">
            <div class="px-8 py-8">
              <div class="flex justify-between items-center mb-8">
                <h3 class="text-2xl font-black text-white italic uppercase tracking-tighter">Nastavení Profilu</h3>
                <button @click="closeEditModal" class="p-2 text-gray-400 hover:text-white hover:bg-white/5 rounded-full transition-all">
                  <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
              </div>

              <form @submit.prevent="saveProfile" class="space-y-6">
                
                <!-- COVER IMAGE SETTINGS -->
                <div>
                  <label class="block text-xs font-black text-gray-500 uppercase tracking-widest mb-2">Pozadí profilu (Cover)</label>
                  <p class="text-[10px] text-gray-500 mb-2">Doporučená velikost: 1920x500 px. Max 2MB.</p>
                  
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

                <!-- AVATAR SETTINGS -->
                <div>
                  <label class="block text-xs font-black text-gray-500 uppercase tracking-widest mb-2">Avatar</label>
                  <p class="text-[10px] text-gray-500 mb-2">Doporučená velikost: 500x500 px (Čtverec). Max 2MB.</p>
                  
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
                      <label class="block text-xs font-black text-gray-500 uppercase tracking-widest mb-2">Uživatelské jméno</label>
                      <input type="text" v-model="editForm.username" class="w-full p-3 bg-white/5 border border-white/10 rounded-xl text-white font-bold focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all">
                    </div>
                  </div>
                </div>

                <!-- INFO FIELDS -->
                <div class="grid grid-cols-1 gap-4">
                  <div>
                    <label class="block text-xs font-black text-gray-500 uppercase tracking-widest mb-2">Příběh (Bio)</label>
                    <textarea v-model="editForm.bio" rows="3" class="w-full p-4 bg-white/5 border border-white/10 rounded-2xl text-white font-medium focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all placeholder-gray-600" placeholder="Napište něco o sobě..."></textarea>
                  </div>
                </div>

                <!-- Password Toggle -->
                <div class="border-t border-gray-800 pt-4">
                  <button type="button" @click="showPasswordSection = !showPasswordSection" class="text-xs font-black uppercase tracking-widest text-gray-500 hover:text-blue-400 transition-colors">
                    {{ showPasswordSection ? 'Skrýt změnu hesla' : 'Změnit heslo' }}
                  </button>
                  
                  <div v-if="showPasswordSection" class="mt-4 p-6 bg-black/20 rounded-2xl border border-white/5 space-y-4">
                    <input type="password" v-model="passwordForm.old_password" placeholder="Současné heslo" class="w-full p-3 bg-white/5 border border-white/10 rounded-xl text-white text-sm focus:ring-2 focus:ring-red-500/50 focus:outline-none transition-all">
                    <div class="grid grid-cols-2 gap-4">
                      <input type="password" v-model="passwordForm.new_password" placeholder="Nové heslo" class="w-full p-3 bg-white/5 border border-white/10 rounded-xl text-white text-sm focus:ring-2 focus:ring-red-500/50 focus:outline-none transition-all">
                      <input type="password" v-model="passwordForm.confirm_password" placeholder="Potvrdit nové" class="w-full p-3 bg-white/5 border border-white/10 rounded-xl text-white text-sm focus:ring-2 focus:ring-red-500/50 focus:outline-none transition-all">
                    </div>
                    <button type="button" @click="handleChangePassword" :disabled="isChangingPassword" class="w-full py-3 bg-red-600/10 hover:bg-red-600 text-red-500 hover:text-white font-black uppercase tracking-widest rounded-xl transition-all border border-red-600/20 text-xs">
                      Aktualizovat heslo
                    </button>
                  </div>
                </div>

                <div class="flex justify-end pt-6 border-t border-gray-800 mt-4">
                  <button type="submit" :disabled="isSaving" class="px-10 py-4 bg-blue-600 hover:bg-blue-500 text-white font-black uppercase tracking-widest rounded-2xl shadow-2xl shadow-blue-600/20 transition-all transform hover:scale-105 active:scale-95 disabled:opacity-50">
                    {{ isSaving ? 'Ukládám...' : 'Uložit Profil' }}
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