<template>
  <div class="max-w-6xl mx-auto mt-10 p-4">
    <NuxtLink to="/" class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600 mb-4 inline-block">&larr; Zpět</NuxtLink>
    
    <div v-if="loading" class="text-center text-gray-500 py-12">Načítám detaily seriálu...</div>
    <div v-else-if="error" class="text-center text-red-500 py-12">Nepodařilo se načíst seriál: {{ error.message }}</div>

    <div v-else-if="series" class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
      <!-- Hlavička seriálu -->
      <div class="md:flex border-b border-gray-200 dark:border-gray-700">
        <!-- PLAKÁT S TLAČÍTKEM -->
        <div class="md:flex-shrink-0 relative group">
          <img v-if="series.poster" :src="series.poster" :alt="series.title" class="h-96 w-full object-cover md:w-80">
          <div v-else class="bg-gray-300 dark:bg-gray-700 h-96 w-full md:w-80 flex items-center justify-center text-gray-500">Žádný plakát</div>
          
          <button 
            @click.stop="toggleWatchlist"
            class="absolute top-3 right-3 bg-gray-900/70 text-white p-2.5 rounded-full hover:bg-gray-900 hover:scale-110 transition-all shadow-lg border border-white/20"
            :title="watchlistItem ? 'Odebrat ze seznamu' : 'Přidat do seznamu'"
          >
            <svg v-if="!watchlistItem" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" /></svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" /></svg>
          </button>
        </div>
        
        <div class="p-8 w-full">
          <div class="flex justify-between items-start mb-2">
            <h1 class="text-4xl font-bold text-gray-900 dark:text-gray-100">{{ series.title }}</h1>
            
            <div v-if="authStore.isLoggedIn" class="relative">
              <button @click="showCollectionDropdown = !showCollectionDropdown" class="flex items-center gap-2 p-2 px-3 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 transition text-sm font-semibold">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg>
                <span>Kolekce</span>
              </button>
              <div v-if="showCollectionDropdown" class="absolute right-0 top-full mt-2 w-56 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md shadow-xl z-30 overflow-hidden">
                <div v-if="userCollections.length === 0" class="p-4 text-sm text-gray-500 italic">Nemáte žádné kolekce.</div>
                <div v-else>
                  <p class="px-4 py-2 text-xs font-bold text-gray-400 uppercase tracking-wider border-b border-gray-100 dark:border-gray-700">Přidat do:</p>
                  <button v-for="col in userCollections" :key="col.id" @click="handleAddToCollection(col.id)" class="w-full text-left px-4 py-3 text-sm hover:bg-blue-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 border-b border-gray-50 dark:border-gray-700 last:border-0">{{ col.name }}</button>
                </div>
              </div>
            </div>
          </div>

          <div class="flex flex-wrap items-center mb-6 text-gray-600 dark:text-gray-300 text-lg gap-4">
            <span v-if="series.release_date">
              {{ series.release_date.substring(0, 4) }}
              <span v-if="series.end_date"> – {{ series.end_date.substring(0, 4) }}</span>
              <span v-else> – Současnost</span>
            </span>
            <span v-else>TBA</span>
            <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded dark:bg-blue-900 dark:text-blue-200">
              {{ series.seasons?.length || 0 }} {{ series.seasons?.length === 1 ? 'Série' : (series.seasons?.length < 5 ? 'Série' : 'Sérií') }}
            </span>
            <AvgRating :rating="series.avg_rating" />
          </div>
          
          <div v-if="series.description" class="mb-6">
            <h3 class="font-bold text-gray-900 dark:text-gray-100 mb-1 uppercase text-xs tracking-widest">Popis seriálu</h3>
            <p class="text-gray-700 dark:text-gray-300 leading-relaxed text-sm">{{ series.description }}</p>
          </div>

          <div class="grid grid-cols-1 gap-4 text-sm border-t border-gray-100 dark:border-gray-700 pt-4">
            <div v-if="series.directors?.length">
              <span class="font-bold text-gray-900 dark:text-gray-100">Hlavní tvůrci:</span>
              <span class="text-gray-600 dark:text-gray-400 ml-2">
                <template v-for="(d, i) in series.directors" :key="d.id">
                  <NuxtLink :to="`/directors/${d.id}`" class="hover:text-blue-500 transition-colors">{{ d.name }}</NuxtLink><span v-if="i < series.directors.length - 1">, </span>
                </template>
              </span>
            </div>
            <div v-if="series.genres?.length">
              <span class="font-bold text-gray-900 dark:text-gray-100">Žánry:</span>
              <span class="text-gray-600 dark:text-gray-400 ml-2">{{ series.genres.map(g => g.name).join(', ') }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- SEKCE EPIZODY -->
      <div class="p-8 bg-gray-50 dark:bg-gray-900/30">
        <h2 class="text-2xl font-black mb-6 text-gray-800 dark:text-gray-100 flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
          Série a Epizody
        </h2>
        
        <div v-if="series.seasons && series.seasons.length > 0">
          <!-- Taby sérií -->
          <div class="flex overflow-x-auto space-x-2 mb-8 pb-2 border-b border-gray-200 dark:border-gray-700 scrollbar-hide">
            <button 
              v-for="(season, index) in series.seasons" 
              :key="season.id"
              @click="selectedSeasonIndex = index"
              class="px-6 py-3 whitespace-nowrap rounded-t-xl font-bold transition-all"
              :class="selectedSeasonIndex === index 
                ? 'bg-white dark:bg-gray-800 text-blue-600 dark:text-blue-400 border-t border-l border-r border-gray-200 dark:border-gray-700 shadow-sm' 
                : 'text-gray-500 dark:text-gray-500 hover:text-gray-800 dark:hover:text-gray-300'"
            >
              {{ season.season_number }}. Série
            </button>
          </div>

          <!-- Detail vybrané série -->
          <div v-if="currentSeason" class="animate-in fade-in duration-500">
            <div class="flex flex-col md:flex-row gap-6 mb-10 bg-blue-50/50 dark:bg-blue-900/10 p-6 rounded-2xl border border-blue-100 dark:border-blue-900/30">
              <div class="w-32 flex-shrink-0">
                <img v-if="currentSeason.poster" :src="currentSeason.poster" class="w-full h-auto rounded-lg shadow-lg">
                <div v-else class="w-full aspect-[2/3] bg-gray-200 dark:bg-gray-700 rounded-lg flex items-center justify-center text-gray-400 text-xs">Bez plakátu</div>
              </div>
              <div class="flex-grow">
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                  {{ currentSeason.title || `${currentSeason.season_number}. Série` }}
                </h3>
                <p v-if="currentSeason.release_date" class="text-xs font-bold text-blue-600 dark:text-blue-400 uppercase tracking-widest mb-3">
                  Premiéra: {{ new Date(currentSeason.release_date).toLocaleDateString('cs-CZ') }}
                </p>
                <p v-if="currentSeason.overview" class="text-gray-600 dark:text-gray-400 text-sm leading-relaxed mb-4">
                  {{ currentSeason.overview }}
                </p>
                
                <!-- Štáb série -->
                <div class="flex flex-wrap gap-6 text-xs border-t border-gray-200 dark:border-gray-700 pt-4 mt-2">
                  <div v-if="currentSeason.directors?.length">
                    <p class="font-bold text-gray-500 uppercase mb-1">Režie série</p>
                    <p class="text-gray-900 dark:text-gray-200">{{ currentSeason.directors.map(d => d.name).join(', ') }}</p>
                  </div>
                  <div v-if="currentSeason.screenwriters?.length">
                    <p class="font-bold text-gray-500 uppercase mb-1">Scénář série</p>
                    <p class="text-gray-900 dark:text-gray-200">{{ currentSeason.screenwriters.map(s => s.name).join(', ') }}</p>
                  </div>
                  <div v-if="currentSeason.actors?.length">
                    <p class="font-bold text-gray-500 uppercase mb-1">Hlavní obsazení</p>
                    <p class="text-gray-900 dark:text-gray-200">{{ currentSeason.actors.map(a => a.name).join(', ') }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Seznam epizod -->
            <div v-if="currentSeason.episodes?.length > 0" class="grid grid-cols-1 gap-4">
              <div 
                v-for="episode in currentSeason.episodes" 
                :key="episode.id" 
                @click="openEpisodeModal(episode)"
                class="flex flex-col sm:flex-row bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden hover:border-blue-500 dark:hover:border-blue-500 hover:shadow-lg transition-all cursor-pointer group"
              >
                <div class="sm:w-56 flex-shrink-0 relative overflow-hidden">
                  <img v-if="getEpisodeImage(episode)" :src="getEpisodeImage(episode)" class="w-full h-36 object-cover group-hover:scale-105 transition-transform duration-500">
                  <div v-else class="w-full h-36 bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-gray-400 text-xs tracking-widest uppercase">Bez náhledu</div>
                  <div class="absolute inset-0 bg-black/20 group-hover:bg-transparent transition-colors"></div>
                  <div class="absolute bottom-2 left-2 bg-black/80 text-white text-[10px] font-black px-2 py-1 rounded-md uppercase tracking-tighter">
                    E{{ episode.episode_number }}
                  </div>
                </div>
                
                <div class="p-5 flex-grow min-w-0">
                  <div class="flex justify-between items-start mb-1">
                    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 truncate group-hover:text-blue-500 transition-colors">
                      {{ episode.episode_number }}. {{ episode.title }}
                    </h4>
                    <span v-if="episode.runtime" class="text-[10px] font-bold bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-gray-500 dark:text-gray-400">
                      {{ episode.runtime }} MIN
                    </span>
                  </div>
                  <p class="text-[11px] text-gray-400 font-bold mb-2">
                    {{ episode.air_date ? new Date(episode.air_date).toLocaleDateString('cs-CZ') : 'DATUM NEZNÁMÉ' }}
                  </p>
                  <p class="text-sm text-gray-600 dark:text-gray-400 line-clamp-2 italic">
                    {{ episode.overview || 'Popis epizody bude brzy doplněn.' }}
                  </p>
                  
                  <!-- Rychlý přehled štábu u epizody -->
                  <div class="mt-4 flex gap-4 text-[10px] text-gray-400 uppercase tracking-widest font-bold">
                    <span v-if="episode.directors?.length">
                      <span class="text-blue-500">Režie:</span> {{ episode.directors[0].name }}
                    </span>
                    <span v-if="episode.screenwriters?.length">
                      <span class="text-blue-500">Scénář:</span> {{ episode.screenwriters[0].name }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-12 bg-white dark:bg-gray-800 rounded-2xl border border-dashed border-gray-300 dark:border-gray-700 text-gray-500 italic">
              Tato série zatím nemá žádné epizody.
            </div>
          </div>
        </div>
      </div>

      <!-- RECENZE SEKCE -->
      <div class="p-8 border-t border-gray-200 dark:border-gray-700">
        <h2 class="text-2xl font-black mb-8 dark:text-gray-100 flex items-center gap-2 uppercase tracking-tight">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg>
          Recenze a Hodnocení
        </h2>

        <!-- Moje recenze -->
        <div v-if="userReview" class="mb-10 bg-blue-50 dark:bg-blue-900/20 p-6 rounded-2xl border border-blue-100 dark:border-blue-900/30">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-sm font-black text-blue-600 dark:text-blue-400 uppercase tracking-widest">Moje hodnocení</h3>
            <div class="flex gap-2">
              <button @click="handleEditReview(userReview)" class="text-[10px] font-bold text-gray-500 hover:text-blue-500 uppercase transition-colors">Upravit</button>
              <button @click="handleDeleteReview(userReview.id)" class="text-[10px] font-bold text-gray-500 hover:text-red-500 uppercase transition-colors">Smazat</button>
            </div>
          </div>
          
          <div v-if="editingReviewId === userReview.id">
            <form @submit.prevent="handleSaveEdit(userReview.id)" class="space-y-4">
              <RatingInput v-model="editedReviewRating" />
              <textarea v-model="editedReviewComment" rows="3" class="w-full p-3 border rounded-xl bg-white dark:bg-gray-800 dark:text-gray-200 dark:border-gray-700 focus:ring-2 focus:ring-blue-500 focus:outline-none"></textarea>
              <div class="flex justify-end gap-2">
                <button type="button" @click="handleCancelEdit" class="px-4 py-2 text-sm font-bold text-gray-500 uppercase">Zrušit</button>
                <button type="submit" class="px-6 py-2 bg-blue-600 text-white rounded-xl text-sm font-bold shadow-lg shadow-blue-600/20">Uložit změny</button>
              </div>
            </form>
          </div>
          <div v-else>
            <div class="flex items-center gap-4 mb-4">
              <img v-if="userReview.user.profile_picture" :src="userReview.user.profile_picture" class="w-10 h-10 rounded-full object-cover border-2 border-white dark:border-gray-700">
              <div v-else class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-black text-sm uppercase">
                {{ userReview.user.username.charAt(0) }}
              </div>
              <div class="flex items-center gap-4">
                <span class="text-2xl font-black text-gray-900 dark:text-white">{{ userReview.rating }} <span class="text-yellow-500 text-xl">★</span></span>
                <div class="h-4 w-px bg-gray-300 dark:bg-gray-700"></div>
                <span class="text-sm font-bold text-gray-500 uppercase">{{ new Date(userReview.created_at).toLocaleDateString() }}</span>
              </div>
            </div>
            <p class="text-gray-700 dark:text-gray-300 leading-relaxed">{{ userReview.comment }}</p>
          </div>
        </div>

        <!-- Ostatní recenze -->
        <div v-if="otherReviews.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div v-for="review in otherReviews" :key="review.id" class="bg-gray-50 dark:bg-gray-800/50 p-6 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm transition-transform hover:shadow-md">
            <div class="flex justify-between items-start mb-4">
              <div class="flex items-center gap-3">
                <img v-if="review.user.profile_picture" :src="review.user.profile_picture" class="w-10 h-10 rounded-full object-cover border border-gray-200 dark:border-gray-700">
                <div v-else class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-black text-sm uppercase">
                  {{ review.user.username.charAt(0) }}
                </div>
                <div class="min-w-0">
                  <p class="font-bold text-gray-900 dark:text-white truncate">{{ review.user.username }}</p>
                  <p class="text-[10px] text-gray-400 font-bold uppercase">{{ new Date(review.created_at).toLocaleDateString() }}</p>
                </div>
              </div>
              <div class="bg-yellow-500/10 text-yellow-600 dark:text-yellow-500 px-2 py-1 rounded-lg text-xs font-black">
                {{ review.rating }} ★
              </div>
            </div>
            <p class="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">{{ review.comment }}</p>
          </div>
        </div>
        <div v-else-if="!userReview" class="text-center py-12 bg-gray-50 dark:bg-gray-800/30 rounded-3xl border-2 border-dashed border-gray-200 dark:border-gray-700">
          <p class="text-gray-500 font-bold uppercase tracking-widest text-xs">Buďte první, kdo napíše recenzi!</p>
        </div>

        <!-- Formulář pro novou recenzi -->
        <div v-if="authStore.isLoggedIn && !userReview" class="mt-12 bg-white dark:bg-gray-800 p-8 rounded-3xl shadow-xl border border-gray-100 dark:border-gray-700">
          <h3 class="text-xl font-black mb-6 dark:text-gray-100 uppercase tracking-tight">Napsat vlastní názor</h3>
          <form @submit.prevent="submitReview" class="space-y-6">
            <div>
              <label class="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-3">Vaše hodnocení</label>
              <RatingInput v-model="newReview.rating" />
            </div>
            <div>
              <label class="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-3">Text recenze</label>
              <textarea v-model="newReview.comment" placeholder="Jak se vám tento seriál líbil? Co říkáte na obsazení nebo atmosféru?" class="w-full p-4 border rounded-2xl dark:bg-gray-900 dark:border-gray-700 dark:text-white focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all" rows="4"></textarea>
            </div>
            <button type="submit" :disabled="submittingReview" class="w-full md:w-auto px-10 py-4 bg-blue-600 hover:bg-blue-500 text-white rounded-2xl text-sm font-black uppercase tracking-widest transition-all transform hover:scale-105 shadow-xl shadow-blue-600/20 disabled:opacity-50">
              Odeslat recenzi
            </button>
          </form>
        </div>
      </div>
    </div>

    <!-- EPISODE DETAIL MODAL -->
    <transition enter-active-class="duration-300 ease-out" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100" leave-active-class="duration-200 ease-in" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
      <div v-if="selectedEpisode" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <div class="flex items-center justify-center min-h-screen px-4 py-12 text-center sm:block sm:p-0">
          <div class="fixed inset-0 bg-gray-900/90 backdrop-blur-sm transition-opacity" @click="closeEpisodeModal"></div>

          <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

          <div class="inline-block align-bottom bg-white dark:bg-gray-900 rounded-3xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full border border-gray-200 dark:border-gray-800">
            <div class="relative h-64 sm:h-96">
              <img v-if="getEpisodeImage(selectedEpisode)" :src="getEpisodeImage(selectedEpisode)" class="w-full h-full object-cover">
              <div v-else class="w-full h-full bg-gray-800 flex items-center justify-center text-gray-600">Bez náhledu</div>
              <div class="absolute inset-0 bg-gradient-to-t from-gray-900 via-transparent to-transparent"></div>
              <button @click="closeEpisodeModal" class="absolute top-4 right-4 bg-black/50 hover:bg-black/80 text-white p-2 rounded-full transition-colors">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
              <div class="absolute bottom-6 left-8 right-8">
                <p class="text-blue-400 font-black uppercase tracking-widest text-xs mb-2">{{ currentSeason?.season_number }}. Série &bull; Epizoda {{ selectedEpisode.episode_number }}</p>
                <h3 class="text-3xl sm:text-4xl font-black text-white leading-tight">{{ selectedEpisode.title }}</h3>
              </div>
            </div>

            <div class="p-8 sm:p-10">
              <div class="flex flex-wrap items-center gap-6 mb-8 pb-6 border-b border-gray-100 dark:border-gray-800">
                <div class="flex items-center gap-2">
                  <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                  <span class="text-sm font-bold text-gray-600 dark:text-gray-400">{{ selectedEpisode.air_date ? new Date(selectedEpisode.air_date).toLocaleDateString('cs-CZ') : 'Datum neznámé' }}</span>
                </div>
                <div v-if="selectedEpisode.runtime" class="flex items-center gap-2">
                  <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  <span class="text-sm font-bold text-gray-600 dark:text-gray-400">{{ selectedEpisode.runtime }} minut</span>
                </div>
              </div>

              <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
                <div class="lg:col-span-2">
                  <h4 class="text-xs font-black text-gray-400 uppercase tracking-widest mb-4">Děj epizody</h4>
                  <p class="text-gray-700 dark:text-gray-300 leading-relaxed">{{ selectedEpisode.overview || 'K této epizodě zatím nebyl přidán podrobný popis.' }}</p>
                </div>
                
                <div class="space-y-8">
                  <div v-if="selectedEpisode.directors?.length">
                    <h4 class="text-xs font-black text-gray-400 uppercase tracking-widest mb-3">Režie</h4>
                    <div class="space-y-2">
                      <NuxtLink v-for="d in selectedEpisode.directors" :key="d.id" :to="`/directors/${d.id}`" class="block text-sm font-bold text-blue-600 dark:text-blue-400 hover:underline">{{ d.name }}</NuxtLink>
                    </div>
                  </div>
                  <div v-if="selectedEpisode.screenwriters?.length">
                    <h4 class="text-xs font-black text-gray-400 uppercase tracking-widest mb-3">Scénář</h4>
                    <div class="space-y-2">
                      <p v-for="s in selectedEpisode.screenwriters" :key="s.id" class="text-sm font-bold text-gray-800 dark:text-gray-200">{{ s.name }}</p>
                    </div>
                  </div>
                  <div v-if="selectedEpisode.guest_stars?.length">
                    <h4 class="text-xs font-black text-gray-400 uppercase tracking-widest mb-3">Hostující hvězdy</h4>
                    <div class="space-y-2">
                      <NuxtLink v-for="a in selectedEpisode.guest_stars" :key="a.id" :to="`/actors/${a.id}`" class="block text-sm font-bold text-blue-600 dark:text-blue-400 hover:underline">{{ a.name }}</NuxtLink>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Confirm Modal -->
    <ConfirmModal 
      :is-open="isConfirmModalOpen"
      :title="'Smazat recenzi'"
      :message="'Opravdu chcete smazat svou recenzi?'"
      @confirm="confirmDeleteReview" 
      @close="isConfirmModalOpen = false" 
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, reactive, inject } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useApi } from '../../composables/useApi';
import { useAuthStore } from '../../stores/auth';
import { useToast } from '../../composables/useToast';
import AvgRating from '../../components/AvgRating.vue';
import RatingInput from '../../components/RatingInput.vue';
import ConfirmModal from '../../components/ConfirmModal.vue';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const toast = useToast();
const openAuthModal = inject('openAuthModal');

const { 
  getMovieById, getWatchlist, addToWatchlist, removeFromWatchlist, 
  getCollections, addMovieToCollection, getReviews, addReview, updateReview, deleteReview 
} = useApi();

const seriesId = computed(() => Number(route.params.id));
const series = ref(null);
const loading = ref(true);
const error = ref(null);
const selectedSeasonIndex = ref(0);
const userCollections = ref([]);
const showCollectionDropdown = ref(false);

const reviews = ref([]);
const newReview = reactive({ rating: 5, comment: '' });
const submittingReview = ref(false);
const editingReviewId = ref(null);
const editedReviewRating = ref(1);
const editedReviewComment = ref('');

const isConfirmModalOpen = ref(false);
const pendingDeleteReviewId = ref(null);

const watchlist = ref([]);
const isProcessingWatchlist = ref(false);

// Episode Modal State
const selectedEpisode = ref(null);

const currentSeason = computed(() => {
  if (!series.value || !series.value.seasons || series.value.seasons.length === 0) return null;
  return series.value.seasons[selectedSeasonIndex.value];
});

const watchlistItem = computed(() => {
  if (!watchlist.value) return null;
  return watchlist.value.find(item => item.movie.id === seriesId.value);
});

const userReview = computed(() => {
  if (!authStore.user || !reviews.value) return null;
  return reviews.value.find(review => review.user.id === authStore.user.id);
});

const otherReviews = computed(() => {
  if (!reviews.value) return [];
  if (!userReview.value) return reviews.value;
  return reviews.value.filter(review => review.id !== userReview.value.id);
});

const fetchReviews = async () => {
  try {
    const response = await getReviews({ movie: seriesId.value });
    reviews.value = response.data.results;
  } catch (err) {
    console.error('Error fetching reviews:', err);
  }
};

const fetchSeries = async () => {
  loading.value = true;
  try {
    const response = await getMovieById(seriesId.value);
    series.value = response.data;
    if (series.value.type !== 'series') {
        router.replace(`/movies/${seriesId.value}`);
    }
    
    if (authStore.isLoggedIn) {
      await fetchWatchlistData();
      await fetchUserCollections();
    }
    await fetchReviews();
  } catch (err) {
    console.error(err);
    error.value = err;
  } finally {
    loading.value = false;
  }
};

const fetchWatchlistData = async () => {
  try {
    const response = await getWatchlist();
    watchlist.value = response.data.results;
  } catch (err) {
    console.error(err);
  }
};

const fetchUserCollections = async () => {
  try {
    const response = await getCollections();
    userCollections.value = response.data.results.filter(c => c.user.id === authStore.user?.id);
  } catch (err) {
    console.error('Failed to fetch collections:', err);
  }
};

const handleAddToCollection = async (collectionId) => {
  try {
    await addMovieToCollection(collectionId, seriesId.value);
    showCollectionDropdown.value = false;
    toast.success('Přidáno do kolekce.');
  } catch (err) {
    console.error('Failed to add to collection:', err);
    toast.error('Seriál už v této kolekci je.');
  }
};

const toggleWatchlist = async () => {
  if (!authStore.isLoggedIn) {
    openAuthModal('login');
    return;
  }
  isProcessingWatchlist.value = true;
  try {
    if (watchlistItem.value) {
      await removeFromWatchlist(watchlistItem.value.id);
    } else {
      await addToWatchlist(seriesId.value);
    }
    await fetchWatchlistData();
  } catch (err) {
    toast.error("Chyba při aktualizaci seznamu.");
  } finally {
    isProcessingWatchlist.value = false;
  }
};

const submitReview = async () => {
  submittingReview.value = true;
  try {
    await addReview({
      movie_id: seriesId.value,
      rating: newReview.rating,
      comment: newReview.comment,
    });
    newReview.rating = 5;
    newReview.comment = '';
    await fetchReviews();
    toast.success('Recenze odeslána.');
  } catch (err) {
    console.error('Error submitting review:', err);
    toast.error('Nepodařilo se odeslat recenzi.');
  } finally {
    submittingReview.value = false;
  }
};

const handleEditReview = (review) => {
  editingReviewId.value = review.id;
  editedReviewRating.value = review.rating;
  editedReviewComment.value = review.comment;
};

const handleCancelEdit = () => {
  editingReviewId.value = null;
};

const handleSaveEdit = async (reviewId) => {
  try {
    await updateReview(reviewId, {
      rating: editedReviewRating.value,
      comment: editedReviewComment.value,
    });
    await fetchReviews();
    handleCancelEdit();
    toast.success('Recenze aktualizována.');
  } catch (err) {
    console.error('Error saving review:', err);
    toast.error('Nepodařilo se aktualizovat recenzi.');
  }
};

const handleDeleteReview = (reviewId) => {
  pendingDeleteReviewId.value = reviewId;
  isConfirmModalOpen.value = true;
};

const confirmDeleteReview = async () => {
  if (!pendingDeleteReviewId.value) return;
  try {
    await deleteReview(pendingDeleteReviewId.value);
    await fetchReviews();
    toast.success('Recenze smazána.');
  } catch (err) {
    console.error('Error deleting review:', err);
    toast.error('Nepodařilo se smazat recenzi.');
  } finally {
    isConfirmModalOpen.value = false;
    pendingDeleteReviewId.value = null;
  }
};

const getEpisodeImage = (episode) => {
  if (episode.still_path) return episode.still_path;
  if (currentSeason.value && currentSeason.value.poster) return currentSeason.value.poster;
  if (series.value && series.value.poster) return series.value.poster;
  return null;
};

const openEpisodeModal = (episode) => {
  selectedEpisode.value = episode;
};

const closeEpisodeModal = () => {
  selectedEpisode.value = null;
};

onMounted(fetchSeries);

watch(() => route.params.id, (newId) => {
  if (newId && Number(newId) !== seriesId.value) {
    fetchSeries();
  }
});

watch(() => authStore.isLoggedIn, (isLoggedIn) => {
  if (isLoggedIn) {
    fetchWatchlistData();
    fetchUserCollections();
  } else {
    watchlist.value = [];
    userCollections.value = [];
  }
});
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>