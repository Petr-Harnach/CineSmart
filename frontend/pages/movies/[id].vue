<template>
  <div class="max-w-6xl mx-auto mt-10 p-4">
    <div v-if="loading" class="text-center text-gray-500 py-12">Načítám detaily filmu...</div>
    <div v-else-if="error" class="text-center text-red-500 py-12">Nepodařilo se načíst film: {{ error.message }}</div>

    <div v-else-if="movie">
      <!-- Horní sekce - plakát a základní info -->
      <div class="flex flex-col md:flex-row gap-8">
        <!-- Plakát -->
        <div class="flex-shrink-0 w-64 mx-auto md:mx-0 relative group">
          <div class="aspect-[2/3] rounded-lg overflow-hidden shadow-lg">
            <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" class="w-full h-full object-cover">
            <div v-else class="bg-gray-300 dark:bg-gray-700 w-full h-full flex items-center justify-center text-gray-500">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
            </div>
          </div>
          <!-- Tlačítko Watchlist (Overlay) -->
          <button 
            v-if="authStore.isLoggedIn"
            @click.stop="toggleWatchlist"
            class="absolute top-3 right-3 bg-gray-900/70 text-white p-2.5 rounded-full hover:bg-gray-900 hover:scale-110 transition-all shadow-lg border border-white/20"
            :title="watchlistItem ? 'Odebrat ze seznamu' : 'Přidat do seznamu'"
          >
            <svg v-if="!watchlistItem" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </button>
        </div>

        <!-- Informace o filmu -->
        <div class="flex-grow text-center md:text-left">
          <h1 class="text-4xl font-bold text-gray-900 dark:text-gray-100 mb-2">{{ movie.title }}</h1>
          <p class="text-lg text-gray-500 mb-4">{{ movie.release_date ? movie.release_date.substring(0, 4) : '' }}</p>
          
          <!-- Žánry -->
          <div class="flex flex-wrap gap-2 justify-center md:justify-start mb-6">
            <span v-for="genre in movie.genres" :key="genre.id" class="px-3 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded-full dark:bg-blue-900/30 dark:text-blue-300">
              {{ genre.name }}
            </span>
          </div>

          <p v-if="movie.description" class="text-gray-700 dark:text-gray-300 leading-relaxed mb-6">
            {{ movie.description }}
          </p>
        </div>
      </div>

      <!-- Karty s podrobnostmi a produkcí -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mt-12">
        <!-- Karta Podrobnosti -->
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
          <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-gray-100">Podrobnosti</h2>
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p class="font-semibold text-gray-500 dark:text-gray-400">Hodnocení</p>
              <AvgRating :rating="movie.avg_rating" />
            </div>
            <div>
              <p class="font-semibold text-gray-500 dark:text-gray-400">Délka</p>
              <p class="text-gray-900 dark:text-white">{{ movie.duration_minutes ? `${movie.duration_minutes} min` : 'N/A' }}</p>
            </div>
            <div>
              <p class="font-semibold text-gray-500 dark:text-gray-400">Vydáno</p>
              <p class="text-gray-900 dark:text-white">{{ movie.release_date ? new Date(movie.release_date).toLocaleDateString() : 'N/A' }}</p>
            </div>
            <div>
              <p class="font-semibold text-gray-500 dark:text-gray-400">Země</p>
              <p class="text-gray-900 dark:text-white">{{ movie.country || 'N/A' }}</p>
            </div>
          </div>
        </div>

        <!-- Karta Produkce -->
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
          <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-gray-100">Produkce</h2>
          <div class="space-y-3 text-sm">
            <div v-if="movie.directors && movie.directors.length">
              <p class="font-semibold text-gray-500 dark:text-gray-400">Režie</p>
              <p class="text-gray-900 dark:text-white">
                <template v-for="(director, index) in movie.directors" :key="director.id">
                  <NuxtLink :to="`/directors/${director.id}`" class="hover:underline">{{ director.name }}</NuxtLink><span v-if="index < movie.directors.length - 1">, </span>
                </template>
              </p>
            </div>
            <div v-if="movie.screenwriters && movie.screenwriters.length">
              <p class="font-semibold text-gray-500 dark:text-gray-400">Scénář</p>
              <p class="text-gray-900 dark:text-white">
                <span v-for="(writer, index) in movie.screenwriters" :key="writer.id">
                  {{ writer.name }}<span v-if="index < movie.screenwriters.length - 1">, </span>
                </span>
              </p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Sekce Obsazení -->
      <div class="mt-12">
        <h2 class="text-2xl font-bold mb-4 text-gray-900 dark:text-gray-100">Obsazení</h2>
        <div class="flex overflow-x-auto gap-4 pb-4 -mx-4 px-4">
          <NuxtLink v-for="actor in movie.actors" :key="actor.id" :to="`/actors/${actor.id}`" class="flex-shrink-0 w-32 text-center group">
            <div class="aspect-[2/3] w-full bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform group-hover:-translate-y-1 transition-transform">
              <img v-if="actor.photo" :src="actor.photo" :alt="actor.name" class="w-full h-full object-cover">
              <div v-else class="w-full h-full flex items-center justify-center bg-gray-300 dark:bg-gray-700 text-gray-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
              </div>
            </div>
            <p class="mt-2 text-sm font-semibold text-gray-800 dark:text-gray-200 truncate group-hover:underline">{{ actor.name }}</p>
          </NuxtLink>
        </div>
      </div>
      
      <!-- ... zbytek kódu pro recenze a doporučení ... -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, reactive, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useApi } from '../../composables/useApi';
import { useAuthStore } from '../../stores/auth';
import { useToast } from '../../composables/useToast';
import AvgRating from '../../components/AvgRating.vue';
import Carousel from '../../components/Carousel.vue';
import RatingInput from '../../components/RatingInput.vue';
import ConfirmModal from '../../components/ConfirmModal.vue';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const toast = useToast();

const movieId = computed(() => Number(route.params.id));

const {
  getMovieById, addReview, updateReview, deleteReview, 
  getWatchlist, addToWatchlist, removeFromWatchlist, 
  getMovies, getReviews, toggleLikeReview,
  getCollections, addMovieToCollection
} = useApi();

const movie = ref(null);
const reviews = ref([]);
const userCollections = ref([]);
const showCollectionDropdown = ref(false);
const reviewSortOrder = ref('-created_at');
const relatedMovies = ref([]);
const loading = ref(true);
const error = ref(null);

const isDescriptionExpanded = ref(false);

const newReview = reactive({ rating: 5, comment: '' });
const submittingReview = ref(false);
const submitError = ref(null);

const editingReviewId = ref(null);
const editedReviewRating = ref(1);
const editedReviewComment = ref('');

const watchlist = ref([]);
const isProcessingWatchlist = ref(false);

// Confirm Modal State
const isConfirmModalOpen = ref(false);
const pendingDeleteReviewId = ref(null);

const watchlistItem = computed(() => watchlist.value.find(item => item.movie.id === movieId.value));

const userReview = computed(() => {
  if (!authStore.user || !reviews.value) return null;
  return reviews.value.find(review => review.user.id === authStore.user.id);
});

const otherReviews = computed(() => {
  if (!reviews.value) return [];
  if (!userReview.value) return reviews.value;
  return reviews.value.filter(review => review.id !== userReview.value.id);
});

const goToDetail = (item) => {
  if (item.type === 'series') {
    router.push(`/series/${item.id}`);
  } else {
    router.push(`/movies/${item.id}`);
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

const fetchRelatedMovies = async (currentMovie) => {
  if (!currentMovie || !currentMovie.genres || currentMovie.genres.length === 0) {
    relatedMovies.value = [];
    return;
  }
  try {
    const genreId = currentMovie.genres[0].id;
    const response = await getMovies({ genres: genreId, limit: 10 });
    relatedMovies.value = response.data.results.filter(m => m.id !== currentMovie.id);
  } catch (err) {
    console.error('Error fetching related movies:', err);
    relatedMovies.value = [];
  }
};

const fetchReviews = async () => {
  try {
    const response = await getReviews({ movie: movieId.value, ordering: reviewSortOrder.value });
    reviews.value = response.data.results;
  } catch (err) {
    console.error('Error fetching reviews:', err);
  }
};

const fetchWatchlist = async () => {
  try {
    const response = await getWatchlist();
    watchlist.value = response.data.results;
  } catch (err) {
    console.error("Failed to fetch watchlist:", err);
  }
};

const fetchMovie = async (id) => {
  loading.value = true;
  error.value = null;
  relatedMovies.value = [];
  try {
    const response = await getMovieById(id);
    movie.value = response.data;
    
    if (movie.value.type === 'series') {
        router.replace(`/series/${id}`);
        return;
    }

    if (authStore.isLoggedIn) {
      await fetchWatchlist();
      await fetchUserCollections();
    }
    await fetchRelatedMovies(movie.value);
    await fetchReviews();
  } catch (err) {
    error.value = err;
    console.error('Error fetching movie:', err);
  } finally {
    loading.value = false;
  }
};

const handleAddToCollection = async (collectionId) => {
  try {
    await addMovieToCollection(collectionId, movieId.value);
    showCollectionDropdown.value = false;
    toast.success('Přidáno do kolekce.');
  } catch (err) {
    console.error('Failed to add to collection:', err);
    toast.error('Film už v této kolekci je.');
  }
};

const toggleWatchlist = async () => {
  if (!authStore.isLoggedIn) return;
  isProcessingWatchlist.value = true;
  try {
    if (watchlistItem.value) {
      await removeFromWatchlist(watchlistItem.value.id);
    } else {
      await addToWatchlist(movieId.value);
    }
    await fetchWatchlist();
  } catch (err) {
    console.error("Failed to toggle watchlist:", err);
    toast.error('Nepodařilo se aktualizovat seznam.');
  } finally {
    isProcessingWatchlist.value = false;
  }
};

onMounted(() => {
  if (movieId.value) {
    fetchMovie(movieId.value);
  }
});

watch(() => route.params.id, (newId) => {
  if (newId) {
    fetchMovie(Number(newId));
  }
});
</script>