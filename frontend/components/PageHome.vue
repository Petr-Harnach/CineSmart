<template>
  <div>
    <!-- Main Trailer Banner -->
    <div class="mb-12">
      <div v-if="loadingMainTrailer" class="text-center text-gray-500 py-24">
        <p>Loading epic trailers...</p>
      </div>
      <div v-else-if="currentTrailerMovie && currentTrailerMovie.trailer_url"
           class="relative max-w-6xl mx-auto overflow-hidden rounded-2xl shadow-2xl group">
        <div class="relative" style="padding-top: 56.25%;">
            <div ref="youtubePlayerContainer" class="absolute top-0 left-0 w-full h-full"></div>
        </div>
        <!-- Carousel Navigation -->
        <template v-if="mainTrailerMovies.length > 1">
          <button @click="prevTrailer" class="absolute left-0 top-1/2 -translate-y-1/2 z-10 p-4 bg-black bg-opacity-50 rounded-r-lg text-white opacity-0 group-hover:opacity-100 transition-opacity">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
          </button>
          <button @click="nextTrailer" class="absolute right-0 top-1/2 -translate-y-1/2 z-10 p-4 bg-black bg-opacity-50 rounded-l-lg text-white opacity-0 group-hover:opacity-100 transition-opacity">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
          </button>
        </template>
        <!-- Overlays -->
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
              <img v-if="currentTrailerMovie.poster" :src="currentTrailerMovie.poster" :alt="currentTrailerMovie.title" class="hidden md:block w-32 lg:w-40 rounded-lg shadow-lg object-cover cursor-pointer" @click="showMovieDetail(currentTrailerMovie.id)">
              <button 
                @click.stop="toggleWatchlist"
                class="absolute top-0 right-0 transform -translate-y-1/2 translate-x-1/2 bg-gray-800 bg-opacity-75 rounded-full p-2 text-white hover:bg-opacity-100 hover:scale-110 transition-transform"
                :aria-label="isCurrentTrailerInWatchlist ? 'Remove from watchlist' : 'Add to watchlist'"
              >
                <!-- Plus Icon -->
                <svg v-if="!isCurrentTrailerInWatchlist" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                </svg>
                <!-- Check Icon -->
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </button>
            </div>
            <div class="pointer-events-auto">
              <h2 class="text-4xl md:text-5xl font-black tracking-tight">{{ currentTrailerMovie.title }}</h2>
              <p v-if="currentTrailerMovie.release_date" class="text-lg font-medium mt-2 opacity-80">
                  Released: {{ new Date(currentTrailerMovie.release_date).getFullYear() }}
              </p>
              <button @click="showMovieDetail(currentTrailerMovie.id)" class="mt-4 inline-flex items-center px-6 py-3 bg-white/10 border border-white/20 backdrop-blur-md rounded-lg text-lg font-semibold transition hover:bg-white/20">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                  View Details
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-center bg-gray-100 dark:bg-gray-800 rounded-lg py-24 max-w-6xl mx-auto">
        <h3 class="text-xl font-semibold text-gray-700 dark:text-gray-300">No Featured Trailer Available</h3>
        <p class="text-gray-500 dark:text-gray-400 mt-2">Check back later for more epic content.</p>
      </div>
    </div>

    <!-- Top Rated Movies Section -->
    <div class="mb-12 reveal">
      <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-4">Top Rated Movies</h2>
      <div v-if="loadingTopRated" class="text-center text-gray-500">
        <p>Loading top rated movies...</p>
      </div>
      <Carousel v-else>
        <div 
          v-for="movie in topRatedMovies" 
          :key="movie.id" 
          class="flex-shrink-0 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer"
          @click="showMovieDetail(movie.id)"
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

    <!-- From your Watchlist Section -->
    <div class="mb-12 reveal">
      <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-4">From Your Watchlist</h2>
      <div v-if="loadingWatchlist" class="text-center text-gray-500">
        <p>Loading watchlist...</p>
      </div>
      <div v-else-if="!authStore.isLoggedIn" class="text-center p-8 bg-gray-100 dark:bg-gray-800 rounded-lg">
        <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">Your Watchlist is a click away</h3>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Log in to keep track of movies you want to watch.</p>
        <div class="mt-6">
          <button @click="navigateToLogin" type="button" class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            Log in
          </button>
        </div>
      </div>
      <div v-else-if="userWatchlist.length === 0" class="text-center text-gray-600 dark:text-gray-400">
        <p>Your watchlist is empty. Add some movies!</p>
      </div>
      <Carousel v-else>
        <div 
          v-for="item in userWatchlist" 
          :key="item.id" 
          class="flex-shrink-0 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer"
          @click="showMovieDetail(item.movie.id)"
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

    <!-- Popular Actors Section -->
    <div class="mb-12 reveal">
      <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-4">Popular Actors</h2>
      <div v-if="loadingPopularActors" class="text-center text-gray-500">
        <p>Loading popular actors...</p>
      </div>
      <div v-else-if="popularActors.length === 0" class="text-center text-gray-600 dark:text-gray-400">
        <p>No popular actors found.</p>
      </div>
      <Carousel v-else>
        <div 
          v-for="actor in popularActors" 
          :key="actor.id" 
          class="flex-shrink-0 w-48 flex flex-col items-center cursor-pointer transform hover:-translate-y-1 transition-transform duration-300"
          @click="showActorDetail(actor.id)"
        >
          <!-- Placeholder for actor image/avatar -->
          <img v-if="actor.photo" :src="actor.photo" :alt="actor.name" class="h-40 w-40 rounded-full object-cover shadow-lg mb-3">
          <div v-else class="bg-gray-300 dark:bg-gray-700 h-40 w-40 rounded-full flex items-center justify-center shadow-lg mb-3 text-gray-500">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-20 w-20" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
          </div>
          <h3 class="text-md font-bold text-gray-900 dark:text-gray-100 text-center truncate w-full">{{ actor.name }}</h3>
        </div>
      </Carousel>
    </div>

    <!-- In Theaters Section -->
    <div class="mb-12 reveal">
      <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-4">In Theaters Now</h2>
      <div v-if="loadingInTheaters" class="text-center text-gray-500">
        <p>Loading what's in theaters...</p>
      </div>
      <div v-else-if="inTheatersMovies.length === 0" class="text-center text-gray-600 dark:text-gray-400">
        <p>No movies in theaters found.</p>
      </div>
      <Carousel v-else>
        <div 
          v-for="movie in inTheatersMovies" 
          :key="movie.id" 
          class="flex-shrink-0 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer"
          @click="showMovieDetail(movie.id)"
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

    <!-- Coming Soon Section -->
    <div class="mb-12 reveal">
      <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-4">Coming Soon</h2>
      <div v-if="loadingComingSoon" class="text-center text-gray-500">
        <p>Loading coming soon movies...</p>
      </div>
      <div v-else-if="!comingSoonMovies || comingSoonMovies.length === 0" class="text-center text-gray-600 dark:text-gray-400">
        <p>No upcoming movies found.</p>
      </div>
      <Carousel v-else>
        <div 
          v-for="movie in comingSoonMovies" 
          :key="movie.id" 
          class="flex-shrink-0 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer"
          @click="showMovieDetail(movie.id)"
        >
          <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" class="h-64 w-full object-cover">
          <div v-else class="bg-gray-300 dark:bg-gray-700 h-64 w-full"></div>
          <div class="p-4">
            <h3 class="text-md font-semibold text-gray-900 dark:text-gray-100 truncate">{{ movie.title }}</h3>
            <p v-if="movie.release_date" class="text-sm text-gray-500 mt-1">Releases: {{ new Date(movie.release_date).toLocaleDateString() }}</p>
          </div>
        </div>
      </Carousel>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, watch, computed, nextTick } from 'vue';
import { useApi } from '../composables/useApi';
import { useAuthStore } from '../stores/auth';
import AvgRating from './AvgRating.vue';
import Carousel from './Carousel.vue';

const props = defineProps({
  filters: Object,
});

const emit = defineEmits(['show-detail', 'navigate', 'show-actor-detail']);
const authStore = useAuthStore();
const { getMovies, getWatchlist, getActors, addToWatchlist, removeFromWatchlist } = useApi();

const topRatedMovies = ref([]);
const userWatchlist = ref([]);
const popularActors = ref([]);
const inTheatersMovies = ref([]);
const mainTrailerMovies = ref([]); // New array for carousel
const currentTrailerIndex = ref(0); // Index for the carousel
const loadingTopRated = ref(true);
const loadingWatchlist = ref(true);
const loadingPopularActors = ref(true);
const loadingInTheaters = ref(true);
const loadingMainTrailer = ref(true); // New loading state for main trailer
const error = ref(null);

const player = ref(null); // To hold the YouTube player instance
const isVideoPlaying = ref(false); // To track player state

// Helper to extract video ID from YouTube URL
const parseVideoId = (url) => {
  if (!url) return null;
  const videoIdMatch = url.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|v\/|shorts\/))([^&\n?#]+)/);
  return videoIdMatch ? videoIdMatch[1] : null;
};

// This function will be called by the YouTube player API
const onPlayerStateChange = (event) => {
  if (event.data === 1) { // 1 is YT.PlayerState.PLAYING
    isVideoPlaying.value = true;
  } else if (event.data === 2 || event.data === 0) { // 2 is PAUSED, 0 is ENDED
    isVideoPlaying.value = false;
  }
};

// Computed property to get the movie to display based on the carousel index.
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
    emit('navigate', 'login');
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
    await fetchUserWatchlist(); // Refresh the watchlist state
  } catch (error) {
    console.error("Failed to update watchlist:", error);
    // Optionally, show a toast or error message to the user
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
    console.error('Error fetching top rated movies:', err);
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
    userWatchlist.value = response.data?.results || [];
  } catch (err) {
    console.error('Error fetching user watchlist:', err);
  } finally {
    loadingWatchlist.value = false;
  }
};

const navigateToLogin = () => {
  emit('navigate', 'login');
};

const fetchPopularActors = async () => {
  loadingPopularActors.value = true;
  try {
    const response = await getActors({ limit: 10 }); // Limit to 10 popular actors
    popularActors.value = response.data?.results || [];
  } catch (err) {
    console.error('Error fetching popular actors:', err);
  } finally {
    loadingPopularActors.value = false;
  }
};

const fetchInTheatersMovies = async () => {
  loadingInTheaters.value = true;
  try {
    const today = new Date();
    const oneMonthAgo = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
    const formattedDate = oneMonthAgo.toISOString().split('T')[0];

    const response = await getMovies({ 
      ordering: '-release_date', 
      limit: 5,
      release_date__gte: formattedDate 
    });
    inTheatersMovies.value = response.data?.results || [];
  } catch (err) {
    console.error('Error fetching "In Theaters" movies:', err);
  } finally {
    loadingInTheaters.value = false;
  }
};

const fetchMainTrailerMovie = async () => {
  loadingMainTrailer.value = true;
  try {
    const today = new Date();
    const oneMonthAgo = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
    const formattedDate = oneMonthAgo.toISOString().split('T')[0];

    // Nejdříve zkusíme novinky s trailerem za poslední měsíc
    let response = await getMovies({ 
      ordering: '-release_date', 
      limit: 20,
      release_date__gte: formattedDate 
    });
    
    let results = response.data?.results || [];
    let moviesWithTrailers = results.filter(movie => movie.trailer_url).slice(0, 6);

    // Pokud nemáme žádné novinky s trailerem, vezmeme prostě nejnovější filmy s trailerem bez omezení datem (fallback)
    if (moviesWithTrailers.length === 0) {
      response = await getMovies({ ordering: '-release_date', limit: 20 });
      results = response.data?.results || [];
      moviesWithTrailers = results.filter(movie => movie.trailer_url).slice(0, 6);
    }

    mainTrailerMovies.value = moviesWithTrailers;
  } catch (err) {
    console.error('Error fetching main trailer movies:', err);
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
  fetchMainTrailerMovie();

  // Logika pro animace při skrolování
  const observerOptions = {
    threshold: 0.25, // Spustí se, až když je vidět 25% sekce
    rootMargin: '0px 0px -100px 0px' // Posune spouštěcí linii o 100px nahoru od spodku
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        observer.unobserve(entry.target); // Animovat jen jednou
      }
    });
  }, observerOptions);

  nextTick(() => {
    const revealedElements = document.querySelectorAll('.reveal');
    revealedElements.forEach(el => observer.observe(el));
  });
});

const showMovieDetail = (movieId) => {
  emit('show-detail', movieId);
};

const showActorDetail = (actorId) => {
  emit('show-actor-detail', actorId);
};
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