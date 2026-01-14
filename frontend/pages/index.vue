<template>
  <div class="space-y-16 pb-12">
    <!-- Hlavní banner s trailery -->
    <div class="mb-12">
      <div v-if="loadingMainTrailer" class="text-center text-gray-500 py-24">
        <p class="animate-pulse">Načítám skvělé trailery...</p>
      </div>
      <div v-else-if="currentTrailerMovie && currentTrailerMovie.trailer_url"
           class="relative max-w-6xl mx-auto overflow-hidden rounded-3xl shadow-2xl group">
        <div class="relative" style="padding-top: 56.25%;">
            <div ref="youtubePlayerContainer" class="absolute top-0 left-0 w-full h-full"></div>
        </div>
        <!-- Navigace karuselu -->
        <template v-if="mainTrailerMovies.length > 1">
          <button @click="prevTrailer" class="absolute left-0 top-1/2 -translate-y-1/2 z-10 p-4 bg-black/40 backdrop-blur-md rounded-r-2xl text-white opacity-0 group-hover:opacity-100 transition-all hover:bg-black/60">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" /></svg>
          </button>
          <button @click="nextTrailer" class="absolute right-0 top-1/2 -translate-y-1/2 z-10 p-4 bg-black/40 backdrop-blur-md rounded-l-2xl text-white opacity-0 group-hover:opacity-100 transition-all hover:bg-black/60">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" /></svg>
          </button>
        </template>
        <!-- Překryvy -->
        <div 
          class="absolute bottom-0 left-0 right-0 h-1/3 bg-gradient-to-t from-black via-black/60 to-transparent pointer-events-none transition-opacity duration-700"
          :class="{'opacity-0': isVideoPlaying}"
        ></div>
        <div 
          class="absolute bottom-0 left-0 right-0 p-8 md:p-12 text-white pointer-events-none transition-opacity duration-700"
          :class="{'opacity-0': isVideoPlaying}"
        >
          <div class="flex flex-col md:flex-row items-end gap-8">
            <div class="relative flex-shrink-0 pointer-events-auto hidden md:block">
              <img v-if="currentTrailerMovie.poster" :src="currentTrailerMovie.poster" :alt="currentTrailerMovie.title" class="w-40 lg:w-48 rounded-2xl shadow-2xl object-cover cursor-pointer hover:scale-105 transition-transform" @click="goToDetail(currentTrailerMovie)">
              <button 
                @click.stop="toggleWatchlist"
                class="absolute -top-3 -right-3 bg-blue-600 shadow-xl rounded-full p-3 text-white hover:bg-blue-500 hover:scale-110 transition-all"
                :title="isCurrentTrailerInWatchlist ? 'Odebrat ze seznamu' : 'Přidat do seznamu'"
              >
                <svg v-if="!isCurrentTrailerInWatchlist" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </button>
            </div>
            <div class="pointer-events-auto flex-grow">
              <div class="flex items-center gap-3 mb-2">
                <span v-if="currentTrailerMovie.type === 'series'" class="px-2 py-0.5 bg-blue-600 text-[10px] font-black uppercase rounded tracking-wider">Seriál</span>
                <span v-else class="px-2 py-0.5 bg-gray-600 text-[10px] font-black uppercase rounded tracking-wider">Film</span>
                <AvgRating :rating="currentTrailerMovie.avg_rating" />
              </div>
              <h2 class="text-4xl md:text-6xl font-black tracking-tighter leading-none">{{ currentTrailerMovie.title }}</h2>
              <p v-if="currentTrailerMovie.release_date" class="text-lg font-medium mt-3 opacity-70">
                  Vydáno: {{ new Date(currentTrailerMovie.release_date).getFullYear() }}
              </p>
              <button @click="goToDetail(currentTrailerMovie)" class="mt-6 inline-flex items-center px-8 py-4 bg-white text-black rounded-xl text-lg font-bold transition hover:bg-blue-50 hover:scale-105 active:scale-95 shadow-lg">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                  Zobrazit detaily
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-center bg-gray-100 dark:bg-gray-800 rounded-3xl py-24 max-w-6xl mx-auto border-2 border-dashed border-gray-200 dark:border-gray-700">
        <h3 class="text-2xl font-bold text-gray-700 dark:text-gray-300">Žádný trailer není k dispozici</h3>
        <p class="text-gray-500 dark:text-gray-400 mt-2">Zkuste to prosím později.</p>
      </div>
    </div>

    <!-- Sekce Nejlépe hodnocené -->
    <section class="reveal">
      <h2 class="text-3xl md:text-4xl font-black text-gray-900 dark:text-white mb-8 tracking-tight px-1">Nejlépe hodnocené</h2>
      <div v-if="loadingTopRated" class="flex justify-center py-12">
        <div class="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
      <Carousel v-else>
        <div 
          v-for="movie in topRatedMovies" 
          :key="movie.id" 
          class="flex-shrink-0 w-48 bg-white dark:bg-gray-800 rounded-2xl shadow-lg overflow-hidden transform hover:-translate-y-2 transition-all duration-300 cursor-pointer group"
          @click="goToDetail(movie)"
        >
          <div class="relative aspect-[2/3] overflow-hidden">
            <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500">
            <div v-else class="w-full h-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-gray-400">
               <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
            </div>
            <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
               <AvgRating :rating="movie.avg_rating" size="sm" class="shadow-2xl" />
            </div>
          </div>
          <div class="p-4">
            <h3 class="text-sm font-bold text-gray-900 dark:text-gray-100 line-clamp-2 h-10 leading-tight mb-1">{{ movie.title }}</h3>
            <div class="flex justify-between items-center">
              <span class="text-[10px] font-bold text-gray-500 dark:text-gray-400 uppercase tracking-widest">{{ movie.type === 'series' ? 'Seriál' : 'Film' }}</span>
              <span class="text-xs font-medium text-gray-400">{{ movie.release_date ? movie.release_date.substring(0, 4) : 'TBA' }}</span>
            </div>
          </div>
        </div>
      </Carousel>
    </section>

    <!-- Sekce Z vašeho seznamu -->
    <section class="reveal">
      <h2 class="text-3xl md:text-4xl font-black text-gray-900 dark:text-white mb-8 tracking-tight px-1">Z vašeho seznamu</h2>
      <div v-if="loadingWatchlist" class="flex justify-center py-12">
        <div class="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
      
      <!-- EMPTY STATE / LOGIN CTA -->
      <div v-else-if="!authStore.isLoggedIn" class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-blue-600 to-indigo-900 p-12 text-white shadow-2xl">
        <div class="relative z-10 flex flex-col items-center text-center max-w-2xl mx-auto">
          <div class="mb-6 p-4 bg-white/10 backdrop-blur-xl rounded-2xl shadow-inner">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
          </div>
          <h3 class="text-3xl md:text-4xl font-black mb-4 tracking-tight">Váš osobní seznam filmů</h3>
          <p class="text-lg text-blue-100 mb-8 font-medium leading-relaxed">
            Mějte přehled o všem, co chcete vidět. Přidejte si filmy a seriály do svého seznamu a my vám pohlídáme každou novinku.
          </p>
          <button @click="openAuthModal('login')" type="button" class="px-10 py-4 bg-white text-blue-700 font-black rounded-2xl shadow-xl hover:bg-blue-50 hover:scale-105 active:scale-95 transition-all text-lg">
            Přihlásit se k odběru
          </button>
        </div>
        <!-- Decorative blobs -->
        <div class="absolute -top-24 -left-24 w-64 h-64 bg-white/5 rounded-full blur-3xl"></div>
        <div class="absolute -bottom-24 -right-24 w-64 h-64 bg-indigo-400/20 rounded-full blur-3xl"></div>
      </div>

      <div v-else-if="userWatchlist.length === 0" class="text-center py-20 bg-gray-50 dark:bg-gray-800/50 rounded-3xl border-2 border-dashed border-gray-200 dark:border-gray-700">
        <div class="mb-4 inline-block p-4 bg-gray-100 dark:bg-gray-700 rounded-full">
           <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        </div>
        <p class="text-xl font-bold text-gray-600 dark:text-gray-300">Váš seznam je zatím prázdný.</p>
        <p class="text-gray-500 dark:text-gray-400 mt-1">Procházejte filmy a přidejte si své první kousky!</p>
      </div>

      <Carousel v-else>
        <div 
          v-for="item in userWatchlist" 
          :key="item.id" 
          class="flex-shrink-0 w-48 bg-white dark:bg-gray-800 rounded-2xl shadow-lg overflow-hidden transform hover:-translate-y-2 transition-all duration-300 cursor-pointer group"
          @click="goToDetail(item.movie)"
        >
          <div class="relative aspect-[2/3] overflow-hidden">
            <img v-if="item.movie.poster" :src="item.movie.poster" :alt="item.movie.title" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500">
            <div v-else class="w-full h-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-gray-400">Není plakát</div>
          </div>
          <div class="p-4">
            <h3 class="text-sm font-bold text-gray-900 dark:text-gray-100 line-clamp-2 h-10 leading-tight mb-1">{{ item.movie.title }}</h3>
            <AvgRating :rating="item.movie.avg_rating" size="sm" />
          </div>
        </div>
      </Carousel>
    </section>

    <!-- Sekce Populární herci -->
    <section class="reveal">
      <h2 class="text-3xl md:text-4xl font-black text-gray-900 dark:text-white mb-8 tracking-tight px-1">Populární herci</h2>
      <div v-if="loadingPopularActors" class="flex justify-center py-12">
        <div class="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
      <div v-else-if="popularActors.length === 0" class="text-center text-gray-600 dark:text-gray-400">
        <p>Žádní populární herci nenalezeni.</p>
      </div>
      <Carousel v-else>
        <div 
          v-for="actor in popularActors" 
          :key="actor.id" 
          class="flex-shrink-0 w-48 flex flex-col items-center cursor-pointer group"
          @click="goToActor(actor.id)"
        >
          <div class="relative mb-4">
            <img v-if="actor.photo" :src="actor.photo" :alt="actor.name" class="h-40 w-40 rounded-full object-cover shadow-2xl ring-4 ring-transparent group-hover:ring-blue-500 transition-all duration-300 group-hover:scale-105">
            <div v-else class="bg-gray-300 dark:bg-gray-700 h-40 w-40 rounded-full flex items-center justify-center shadow-lg text-gray-500 ring-4 ring-transparent group-hover:ring-blue-500 transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-20 w-20" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
            </div>
          </div>
          <h3 class="text-md font-extrabold text-gray-900 dark:text-gray-100 text-center truncate w-full group-hover:text-blue-500 transition-colors">{{ actor.name }}</h3>
        </div>
      </Carousel>
    </section>

    <!-- Sekce Právě v kinech -->
    <section class="reveal">
      <h2 class="text-3xl md:text-4xl font-black text-gray-900 dark:text-white mb-8 tracking-tight px-1">Právě v kinech</h2>
      <div v-if="loadingInTheaters" class="flex justify-center py-12">
        <div class="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
      <div v-else-if="inTheatersMovies.length === 0" class="text-center text-gray-600 dark:text-gray-400">
        <p>Žádné filmy v kinech nenalezeny.</p>
      </div>
      <Carousel v-else>
        <div 
          v-for="movie in inTheatersMovies" 
          :key="movie.id" 
          class="flex-shrink-0 w-48 bg-white dark:bg-gray-800 rounded-2xl shadow-lg overflow-hidden transform hover:-translate-y-2 transition-all duration-300 cursor-pointer group"
          @click="goToDetail(movie)"
        >
          <div class="relative aspect-[2/3] overflow-hidden">
            <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500">
            <div v-else class="w-full h-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-gray-400">Není plakát</div>
          </div>
          <div class="p-4">
            <h3 class="text-sm font-bold text-gray-900 dark:text-gray-100 line-clamp-2 h-10 leading-tight mb-1">{{ movie.title }}</h3>
            <AvgRating :rating="movie.avg_rating" />
          </div>
        </div>
      </Carousel>
    </section>

    <!-- Sekce Brzy v kinech -->
    <section class="reveal">
      <h2 class="text-3xl md:text-4xl font-black text-gray-900 dark:text-white mb-8 tracking-tight px-1">Brzy v kinech</h2>
      <div v-if="loadingComingSoon" class="flex justify-center py-12">
        <div class="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
      <div v-else-if="comingSoonMovies.length === 0" class="text-center text-gray-600 dark:text-gray-400">
        <p>Žádné nadcházející filmy nenalezeny.</p>
      </div>
      <Carousel v-else>
        <div 
          v-for="movie in comingSoonMovies" 
          :key="movie.id" 
          class="flex-shrink-0 w-48 bg-white dark:bg-gray-800 rounded-2xl shadow-lg overflow-hidden transform hover:-translate-y-2 transition-all duration-300 cursor-pointer group"
          @click="goToDetail(movie)"
        >
          <div class="relative aspect-[2/3] overflow-hidden">
            <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500 opacity-80 group-hover:opacity-100">
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-60"></div>
            <div class="absolute bottom-2 left-2 right-2 bg-blue-600/90 backdrop-blur-sm text-white text-[10px] font-black px-2 py-1.5 rounded-lg text-center shadow-lg">
              {{ new Date(movie.release_date).toLocaleDateString('cs-CZ', { day: 'numeric', month: 'short' }) }}
            </div>
          </div>
          <div class="p-4">
            <h3 class="text-sm font-bold text-gray-900 dark:text-gray-100 line-clamp-2 h-10 leading-tight mb-1">{{ movie.title }}</h3>
            <p class="text-[10px] font-black text-blue-600 dark:text-blue-400 uppercase tracking-widest">Očekávané</p>
          </div>
        </div>
      </Carousel>
    </section>
  </div>
</template>


<script setup>
import { ref, onMounted, watch, computed, nextTick, inject } from 'vue';
import { useApi } from '../composables/useApi';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';
import AvgRating from '../components/AvgRating.vue';
import Carousel from '../components/Carousel.vue';

const router = useRouter();
const authStore = useAuthStore();
const { getMovies, getWatchlist, getActors, addToWatchlist, removeFromWatchlist } = useApi();

const openAuthModal = inject('openAuthModal');

const topRatedMovies = ref([]);
const userWatchlist = ref([]);
const popularActors = ref([]);
const inTheatersMovies = ref([]);
const comingSoonMovies = ref([]); 
const mainTrailerMovies = ref([]);
const currentTrailerIndex = ref(0);
const loadingTopRated = ref(true);
const loadingWatchlist = ref(true);
const loadingPopularActors = ref(true);
const loadingInTheaters = ref(true);
const loadingComingSoon = ref(true);
const loadingMainTrailer = ref(true);
const error = ref(null);

const player = ref(null);
const isVideoPlaying = ref(false);

const goToDetail = (item) => {
  if (item.type === 'series') {
    router.push(`/series/${item.id}`);
  } else {
    router.push(`/movies/${item.id}`);
  }
};

const goToActor = (id) => {
  router.push(`/actors/${id}`);
};

const parseVideoId = (url) => {
  if (!url) return null;
  const videoIdMatch = url.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|v\/|shorts\/))([^&\n?#]+)/);
  return videoIdMatch ? videoIdMatch[1] : null;
};

const onPlayerStateChange = (event) => {
  if (event.data === 1) { // 1 is YT.PlayerState.PLAYING
    isVideoPlaying.value = true;
  } else if (event.data === 2 || event.data === 0) { // 2 is PAUSED, 0 is ENDED
    isVideoPlaying.value = false;
  }
};

const currentTrailerMovie = computed(() => {
  if (mainTrailerMovies.value.length === 0) return null;
  return mainTrailerMovies.value[currentTrailerIndex.value];
});

const isCurrentTrailerInWatchlist = computed(() => {
  if (!currentTrailerMovie.value || !userWatchlist.value) return null;
  return userWatchlist.value.find(item => item.movie.id === currentTrailerMovie.value.id);
});

const toggleWatchlist = async () => {
  if (!authStore.isLoggedIn) {
    openAuthModal('login'); 
    return;
  }
  if (!currentTrailerMovie.value) return;

  const watchlistItem = isCurrentTrailerInWatchlist.value;
  try {
    if (watchlistItem) {
      await removeFromWatchlist(watchlistItem.id);
    } else {
      await addToWatchlist(currentTrailerMovie.value.id);
    }
    await fetchUserWatchlist(); 
  } catch (error) {
    console.error("Nepodařilo se aktualizovat seznam:", error);
  }
};

const nextTrailer = () => {
  if (mainTrailerMovies.value.length > 1) {
    currentTrailerIndex.value = (currentTrailerIndex.value + 1) % mainTrailerMovies.value.length;
  }
};

const prevTrailer = () => {
  if (mainTrailerMovies.value.length > 1) {
    currentTrailerIndex.value = (currentTrailerIndex.value - 1 + mainTrailerMovies.value.length) % mainTrailerMovies.value.length;
  }
};

const youtubePlayerContainer = ref(null);
const isApiReady = ref(false);

const initPlayer = (videoId) => {
  if (player.value) {
    player.value.destroy();
  }
  player.value = new window.YT.Player(youtubePlayerContainer.value, {
    height: '100%',
    width: '100%',
    videoId: videoId,
    playerVars: { 
      'controls': 1, 
      'modestbranding': 1,
      'rel': 0,
    },
    events: {
      'onStateChange': onPlayerStateChange
    }
  });
};

const loadYouTubeAPI = () => {
  if (window.YT && window.YT.Player) {
    isApiReady.value = true;
    return;
  }
  
  const tag = document.createElement('script');
  tag.src = "https://www.youtube.com/iframe_api";
  const firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

  window.onYouTubeIframeAPIReady = () => {
    isApiReady.value = true;
  };
};

watch([currentTrailerMovie, isApiReady], ([movie, apiReady]) => {
  if (movie && apiReady) {
    nextTick(() => {
      const videoId = parseVideoId(movie.trailer_url);
      if (!videoId) return;

      if (player.value && typeof player.value.cueVideoById === 'function') {
        player.value.cueVideoById(videoId);
      } else {
        if (youtubePlayerContainer.value) {
            initPlayer(videoId);
        }
      }
    });
  }
}, { deep: true });


const fetchTopRatedMovies = async () => {
  loadingTopRated.value = true;
  try {
    const response = await getMovies({ ordering: '-avg_rating', limit: 5 });
    topRatedMovies.value = response.data?.results || [];
  } catch (err) {
    console.error('Chyba při načítání nejlépe hodnocených filmů:', err);
  } finally {
    loadingTopRated.value = false;
  }
};

const fetchUserWatchlist = async () => {
  loadingWatchlist.value = true;
  if (!authStore.isLoggedIn) {
    loadingWatchlist.value = false;
    return;
  }
  try {
    const response = await getWatchlist();
    const allItems = response.data?.results || [];
    userWatchlist.value = allItems.filter(item => !item.watched);
  } catch (err) {
    console.error('Chyba při načítání seznamu uživatele:', err);
  } finally {
    loadingWatchlist.value = false;
  }
};

const fetchPopularActors = async () => {
  loadingPopularActors.value = true;
  try {
    const response = await getActors({ limit: 10 }); 
    popularActors.value = response.data?.results || [];
  } catch (err) {
    console.error('Chyba při načítání herců:', err);
  } finally {
    loadingPopularActors.value = false;
  }
};

const fetchInTheatersMovies = async () => {
  loadingInTheaters.value = true;
  try {
    const today = new Date();
    const oneMonthAgo = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
    
    const formattedToday = today.toISOString().split('T')[0];
    const formattedOneMonthAgo = oneMonthAgo.toISOString().split('T')[0];

    const response = await getMovies({ 
      ordering: '-release_date', 
      limit: 5,
      release_date__gte: formattedOneMonthAgo,
      release_date__lte: formattedToday
    });
    inTheatersMovies.value = response.data?.results || [];
  } catch (err) {
    console.error('Chyba při načítání filmů v kinech:', err);
  } finally {
    loadingInTheaters.value = false;
  }
};

const fetchComingSoonMovies = async () => {
  loadingComingSoon.value = true;
  try {
    const today = new Date();
    const formattedToday = today.toISOString().split('T')[0];

    const response = await getMovies({ 
      ordering: 'release_date',
      limit: 10,
      release_date__gt: formattedToday 
    });
    comingSoonMovies.value = response.data?.results || [];
  } catch (err) {
    console.error('Chyba při načítání nadcházejících filmů:', err);
  } finally {
    loadingComingSoon.value = false;
  }
};

const fetchMainTrailerMovie = async () => {
  loadingMainTrailer.value = true;
  try {
    const today = new Date();
    const oneMonthAgo = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
    
    const formattedToday = today.toISOString().split('T')[0];
    const formattedOneMonthAgo = oneMonthAgo.toISOString().split('T')[0];

    let response = await getMovies({ 
      ordering: '-release_date', 
      limit: 20,
      release_date__gte: formattedOneMonthAgo,
      release_date__lte: formattedToday
    });
    
    let results = response.data?.results || [];
    let moviesWithTrailers = results.filter(movie => movie.trailer_url).slice(0, 6);

    if (moviesWithTrailers.length === 0) {
      response = await getMovies({ 
        ordering: '-release_date', 
        limit: 20, 
        release_date__lte: formattedToday 
      });
      results = response.data?.results || [];
      moviesWithTrailers = results.filter(movie => movie.trailer_url).slice(0, 6);
    }

    mainTrailerMovies.value = moviesWithTrailers;
  } catch (err) {
    console.error('Chyba při načítání trailerů:', err);
  } finally {
    loadingMainTrailer.value = false;
  }
};

onMounted(() => {
  loadYouTubeAPI();
  fetchTopRatedMovies();
  fetchUserWatchlist();
  fetchPopularActors();
  fetchInTheatersMovies();
  fetchComingSoonMovies();
  fetchMainTrailerMovie();

  const observerOptions = {
    threshold: 0.25,
    rootMargin: '0px 0px -100px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  nextTick(() => {
    const revealedElements = document.querySelectorAll('.reveal');
    revealedElements.forEach(el => observer.observe(el));
  });
});
</script>

<style scoped>
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s ease-out;
}

.reveal.active {
  opacity: 1;
  transform: translateY(0);
}
</style>