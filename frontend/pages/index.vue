<template>
  <div>
    <!-- Hlavní banner s trailery -->
    <div class="mb-12">
      <div v-if="loadingMainTrailer" class="text-center text-gray-500 py-24">
        <p>Načítám skvělé trailery...</p>
      </div>
      <div v-else-if="currentTrailerMovie && currentTrailerMovie.trailer_url"
           class="relative max-w-6xl mx-auto overflow-hidden rounded-2xl shadow-2xl group">
        <div class="relative" style="padding-top: 56.25%;">
            <div ref="youtubePlayerContainer" class="absolute top-0 left-0 w-full h-full"></div>
        </div>
        <!-- Navigace karuselu -->
        <template v-if="mainTrailerMovies.length > 1">
          <button @click="prevTrailer" class="absolute left-0 top-1/2 -translate-y-1/2 z-10 p-4 bg-black bg-opacity-50 rounded-r-lg text-white opacity-0 group-hover:opacity-100 transition-opacity">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
          </button>
          <button @click="nextTrailer" class="absolute right-0 top-1/2 -translate-y-1/2 z-10 p-4 bg-black bg-opacity-50 rounded-l-lg text-white opacity-0 group-hover:opacity-100 transition-opacity">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
          </button>
        </template>
        <!-- Překryvy -->
        <div 
          class="absolute bottom-0 left-0 right-0 h-1/4 bg-gradient-to-t from-black to-transparent pointer-events-none transition-opacity duration-500"
          :class="{'opacity-0': isVideoPlaying}"
        ></div>
        <div 
          class="absolute bottom-0 left-0 right-0 p-8 md:p-12 text-white pointer-events-none transition-opacity duration-500"
          :class="{'opacity-0': isVideoPlaying}"
        >
          <div class="flex flex-col md:flex-row items-center gap-6">
            <div class="relative flex-shrink-0 self-end pointer-events-auto">
              <!-- KLIKATELNÝ PLAKÁT -> goToDetail -->
              <img v-if="currentTrailerMovie.poster" :src="currentTrailerMovie.poster" :alt="currentTrailerMovie.title" class="hidden md:block w-32 lg:w-40 rounded-lg shadow-lg object-cover cursor-pointer" @click="goToDetail(currentTrailerMovie)">
              <button 
                @click.stop="toggleWatchlist"
                class="absolute top-0 right-0 transform -translate-y-1/2 translate-x-1/2 bg-gray-800 bg-opacity-75 rounded-full p-2 text-white hover:bg-opacity-100 hover:scale-110 transition-transform"
                :aria-label="isCurrentTrailerInWatchlist ? 'Odebrat ze seznamu' : 'Přidat do seznamu'"
              >
                <svg v-if="!isCurrentTrailerInWatchlist" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </button>
            </div>
            <div class="pointer-events-auto">
              <h2 class="text-4xl md:text-5xl font-black tracking-tight">{{ currentTrailerMovie.title }}</h2>
              <p v-if="currentTrailerMovie.release_date" class="text-lg font-medium mt-2 opacity-80">
                  Vydáno: {{ new Date(currentTrailerMovie.release_date).getFullYear() }}
              </p>
              <!-- TLAČÍTKO DETAIL -> goToDetail -->
              <button @click="goToDetail(currentTrailerMovie)" class="mt-4 inline-flex items-center px-6 py-3 bg-white/10 border border-white/20 backdrop-blur-md rounded-lg text-lg font-semibold transition hover:bg-white/20">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                  Zobrazit detaily
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-center bg-gray-100 dark:bg-gray-800 rounded-lg py-24 max-w-6xl mx-auto">
        <h3 class="text-xl font-semibold text-gray-700 dark:text-gray-300">Žádný trailer není k dispozici</h3>
        <p class="text-gray-500 dark:text-gray-400 mt-2">Zkuste to prosím později.</p>
      </div>
    </div>

    <!-- Sekce Nejlépe hodnocené -->
    <div class="mb-12 reveal">
      <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-4">Nejlépe hodnocené</h2>
      <div v-if="loadingTopRated" class="text-center text-gray-500">
        <p>Načítám filmy...</p>
      </div>
      <Carousel v-else>
        <div 
          v-for="movie in topRatedMovies" 
          :key="movie.id" 
          class="flex-shrink-0 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer"
          @click="goToDetail(movie)"
        >
          <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" class="h-64 w-full object-cover">
          <div v-else class="bg-gray-300 dark:bg-gray-700 h-64 w-full"></div>
          <div class="p-4">
            <h3 class="text-md font-semibold text-gray-900 dark:text-gray-100 truncate">{{ movie.title }}</h3>
            <AvgRating :rating="movie.avg_rating" />
          </div>
        </div>
      </Carousel>
    </div>

    <!-- Sekce Z vašeho seznamu -->
    <div class="mb-12 reveal">
      <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-4">Z vašeho seznamu</h2>
      <div v-if="loadingWatchlist" class="text-center text-gray-500">
        <p>Načítám seznam...</p>
      </div>
      <div v-else-if="!authStore.isLoggedIn" class="text-center p-8 bg-gray-100 dark:bg-gray-800 rounded-lg">
        <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">Váš seznam je na dosah kliknutí</h3>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Přihlaste se, abyste si mohli ukládat filmy, které chcete vidět.</p>
        <div class="mt-6">
          <button @click="openAuthModal('login')" type="button" class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            Přihlásit se
          </button>
        </div>
      </div>
      <div v-else-if="userWatchlist.length === 0" class="text-center text-gray-600 dark:text-gray-400">
        <p>Váš seznam je prázdný. Přidejte nějaké filmy!</p>
      </div>
      <Carousel v-else>
        <div 
          v-for="item in userWatchlist" 
          :key="item.id" 
          class="flex-shrink-0 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer"
          @click="goToDetail(item.movie)"
        >
          <img v-if="item.movie.poster" :src="item.movie.poster" :alt="item.movie.title" class="h-64 w-full object-cover">
          <div v-else class="bg-gray-300 dark:bg-gray-700 h-64 w-full"></div>
          <div class="p-4">
            <h3 class="text-md font-semibold text-gray-900 dark:text-gray-100 truncate">{{ item.movie.title }}</h3>
            <AvgRating :rating="item.movie.avg_rating" />
          </div>
        </div>
      </Carousel>
    </div>

    <!-- Sekce Populární herci -->
    <div class="mb-12 reveal">
      <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-4">Populární herci</h2>
      <div v-if="loadingPopularActors" class="text-center text-gray-500">
        <p>Načítám herce...</p>
      </div>
      <div v-else-if="popularActors.length === 0" class="text-center text-gray-600 dark:text-gray-400">
        <p>Žádní populární herci nenalezeni.</p>
      </div>
      <Carousel v-else>
        <div 
          v-for="actor in popularActors" 
          :key="actor.id" 
          class="flex-shrink-0 w-48 flex flex-col items-center cursor-pointer transform hover:-translate-y-1 transition-transform duration-300"
          @click="goToActor(actor.id)"
        >
          <img v-if="actor.photo" :src="actor.photo" :alt="actor.name" class="h-40 w-40 rounded-full object-cover shadow-lg mb-3">
          <div v-else class="bg-gray-300 dark:bg-gray-700 h-40 w-40 rounded-full flex items-center justify-center shadow-lg mb-3 text-gray-500">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-20 w-20" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
          </div>
          <h3 class="text-md font-bold text-gray-900 dark:text-gray-100 text-center truncate w-full">{{ actor.name }}</h3>
        </div>
      </Carousel>
    </div>

    <!-- Sekce Právě v kinech -->
    <div class="mb-12 reveal">
      <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-4">Právě v kinech</h2>
      <div v-if="loadingInTheaters" class="text-center text-gray-500">
        <p>Načítám filmy v kinech...</p>
      </div>
      <div v-else-if="inTheatersMovies.length === 0" class="text-center text-gray-600 dark:text-gray-400">
        <p>Žádné filmy v kinech nenalezeny.</p>
      </div>
      <Carousel v-else>
        <div 
          v-for="movie in inTheatersMovies" 
          :key="movie.id" 
          class="flex-shrink-0 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer"
          @click="goToDetail(movie)"
        >
          <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" class="h-64 w-full object-cover">
          <div v-else class="bg-gray-300 dark:bg-gray-700 h-64 w-full"></div>
          <div class="p-4">
            <h3 class="text-md font-semibold text-gray-900 dark:text-gray-100 truncate">{{ movie.title }}</h3>
            <AvgRating :rating="movie.avg_rating" />
          </div>
        </div>
      </Carousel>
    </div>

    <!-- Sekce Brzy v kinech -->
    <div class="mb-12 reveal">
      <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-4">Brzy v kinech</h2>
      <div v-if="loadingComingSoon" class="text-center text-gray-500">
        <p>Načítám nadcházející filmy...</p>
      </div>
      <div v-else-if="comingSoonMovies.length === 0" class="text-center text-gray-600 dark:text-gray-400">
        <p>Žádné nadcházející filmy nenalezeny.</p>
      </div>
      <Carousel v-else>
        <div 
          v-for="movie in comingSoonMovies" 
          :key="movie.id" 
          class="flex-shrink-0 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer opacity-90 hover:opacity-100"
          @click="goToDetail(movie)"
        >
          <div class="relative">
            <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" class="h-64 w-full object-cover">
            <div v-else class="bg-gray-300 dark:bg-gray-700 h-64 w-full"></div>
            <div class="absolute top-2 right-2 bg-blue-600 text-white text-xs font-bold px-2 py-1 rounded">
              {{ new Date(movie.release_date).toLocaleDateString() }}
            </div>
          </div>
          <div class="p-4">
            <h3 class="text-md font-semibold text-gray-900 dark:text-gray-100 truncate">{{ movie.title }}</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">Brzy v kinech</p>
          </div>
        </div>
      </Carousel>
    </div>
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
