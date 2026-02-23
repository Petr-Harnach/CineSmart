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
            @click.stop="toggleWatchlist"
            class="absolute top-3 right-3 bg-gray-900/70 text-white p-2.5 rounded-full hover:bg-gray-900 transition-all shadow-lg border border-white/20"
            :class="{
              'hover:scale-110': !(!isMovieReleased && watchlistItem?.watched),
              'opacity-50 cursor-not-allowed': (!isMovieReleased && watchlistItem?.watched)
            }"
            :title="getWatchlistButtonTitle"
            :disabled="!authStore.isLoggedIn && !isMovieReleased && watchlistItem?.watched"
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
          <div class="flex justify-between items-start">
            <h1 class="text-4xl font-bold text-gray-900 dark:text-gray-100 mb-2">{{ movie.title }}</h1>
            
            <!-- Tlačítko Kolekce -->
            <div v-if="authStore.isLoggedIn" class="relative">
              <button 
                @click="showCollectionDropdown = !showCollectionDropdown"
                class="flex items-center gap-2 p-2 px-3 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 transition text-sm font-semibold"
                title="Přidat do kolekce"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
                <span>Kolekce</span>
              </button>
              
              <div v-if="showCollectionDropdown" 
                   class="absolute right-0 top-full mt-2 w-56 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md shadow-xl z-30 overflow-hidden">
                <div v-if="userCollections.length === 0" class="p-4 text-sm text-gray-500 italic">
                  Nemáte žádné kolekce.
                </div>
                <div v-else>
                  <p class="px-4 py-2 text-xs font-bold text-gray-400 uppercase tracking-wider border-b border-gray-100 dark:border-gray-700">Přidat do:</p>
                  <button 
                    v-for="col in userCollections" 
                    :key="col.id"
                    @click="handleAddToCollection(col.id)"
                    class="w-full text-left px-4 py-3 text-sm hover:bg-blue-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 border-b border-gray-50 dark:border-gray-700 last:border-0"
                  >
                    {{ col.name }}
                  </button>
                </div>
              </div>
            </div>
          </div>

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
          <p v-else class="text-gray-500 italic mb-6">Popis není k dispozici.</p>
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
      
      <!-- Sekce Recenze -->
      <div class="mt-12">
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
          <h2 class="text-2xl font-bold mb-4 text-gray-900 dark:text-gray-100">Recenze</h2>
          
          <template v-if="!isMovieReleased">
            <div class="bg-gray-100 dark:bg-gray-700/50 p-6 rounded-lg text-center border border-gray-200 dark:border-gray-700">
              <p class="text-lg font-semibold text-gray-700 dark:text-gray-300">
                Film ještě nevyšel.
              </p>
              <p class="text-gray-500 dark:text-gray-400 mt-2">
                Recenze a hodnocení budou dostupné po datu vydání: 
                <span class="font-medium">{{ movie.release_date ? new Date(movie.release_date).toLocaleDateString() : 'Neznámo' }}</span>
              </p>
            </div>
          </template>
          <template v-else>
            <!-- Vaše recenze (pokud existuje) -->
            <div v-if="userReview" class="mb-8">
              <h3 class="text-lg font-bold mb-2 dark:text-gray-200">Vaše recenze</h3>
              <div class="bg-blue-50 dark:bg-gray-700/50 p-4 rounded-lg shadow-sm border border-blue-200 dark:border-gray-600">
                <template v-if="editingReviewId === userReview.id">
                  <form @submit.prevent="handleSaveEdit(userReview.id)">
                    <div class="mb-2">
                      <label class="block text-gray-700 dark:text-gray-300 text-sm mb-1">Hodnocení</label>
                      <RatingInput v-model="editedReviewRating" />
                    </div>
                    <div class="mb-2">
                      <label for="edit-comment" class="block text-gray-700 dark:text-gray-300 text-sm">Komentář</label>
                      <textarea v-model="editedReviewComment" id="edit-comment" rows="2" maxlength="1000" class="w-full p-1 border rounded bg-gray-100 dark:bg-gray-600 dark:text-gray-200 dark:border-gray-500"></textarea>
                  </div>
                  <div class="flex justify-end space-x-2">
                    <button type="button" @click="handleCancelEdit" class="px-3 py-1 bg-gray-300 rounded text-sm">Zrušit</button>
                    <button type="submit" class="px-3 py-1 bg-blue-600 text-white rounded text-sm">Uložit</button>
                  </div>
                </form>
              </template>
              <template v-else>
                <div class="flex justify-between items-start mb-2">
                  <p class="font-semibold dark:text-gray-100">{{ userReview.user.username }}</p>
                  <p class="text-yellow-500">{{ '⭐'.repeat(userReview.rating) }}</p>
                </div>
                <p class="text-gray-700 dark:text-gray-300 text-sm">{{ userReview.comment }}</p>
                <div class="flex justify-end gap-2 mt-3">
                  <button @click="handleEditReview(userReview)" class="text-xs text-blue-600 hover:underline">Upravit</button>
                  <button @click="handleDeleteReview(userReview.id)" class="text-xs text-red-600 hover:underline">Smazat</button>
                </div>
              </template>
            </div>
          </div>

          <!-- Ostatní recenze -->
          <div v-if="otherReviews.length > 0" class="space-y-4">
            <div v-for="review in otherReviews" :key="review.id" class="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg border border-gray-100 dark:border-gray-700">
              <div class="flex justify-between items-start mb-2">
                <p class="font-semibold dark:text-gray-100">{{ review.user.username }}</p>
                <p class="text-yellow-500">{{ '⭐'.repeat(review.rating) }}</p>
              </div>
              <p class="text-gray-700 dark:text-gray-300 text-sm">{{ review.comment }}</p>
            </div>
          </div>
          <p v-else-if="!userReview" class="text-gray-500 italic text-center py-4">Zatím žádné recenze.</p>

          <!-- Formulář pro přidání recenze -->
          <div v-if="authStore.isLoggedIn && !userReview" class="mt-8">
            <h3 class="font-bold mb-4 dark:text-gray-100">Přidat recenzi</h3>
            <form @submit.prevent="submitReview" class="space-y-4">
              <RatingInput v-model="newReview.rating" />
              <textarea v-model="newReview.comment" placeholder="Napište svůj názor..." class="w-full p-3 border rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white" rows="3"></textarea>
              <button type="submit" :disabled="submittingReview" class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-blue-400">Odeslat</button>
            </form>
          </div>
        </template>
        </div>
      </div>

      <!-- Sekce Obsazení -->
      <div v-if="movie.actors && movie.actors.length" class="mt-12">
        <h2 class="text-2xl font-bold mb-4 text-gray-900 dark:text-gray-100">Obsazení</h2>
        <Carousel>
          <NuxtLink v-for="actor in movie.actors" :key="actor.id" :to="`/actors/${actor.id}`" class="flex-shrink-0 w-32 text-center group">
            <div class="aspect-[2/3] w-full bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform group-hover:-translate-y-1 transition-transform">
              <img v-if="actor.photo" :src="actor.photo" :alt="actor.name" class="w-full h-full object-cover">
              <div v-else class="w-full h-full flex items-center justify-center bg-gray-300 dark:bg-gray-700 text-gray-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
              </div>
            </div>
            <p class="mt-2 text-sm font-semibold text-gray-800 dark:text-gray-200 truncate group-hover:underline">{{ actor.name }}</p>
          </NuxtLink>
        </Carousel>
      </div>

      <!-- Mohlo by se vám líbit -->
      <div v-if="relatedMovies.length > 0" class="mt-12">
        <h2 class="text-2xl font-bold mb-4 text-gray-900 dark:text-gray-100">Mohlo by se vám líbit</h2>
        <Carousel>
          <div 
            v-for="relatedMovie in relatedMovies" 
            :key="relatedMovie.id" 
            class="flex-shrink-0 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer"
            @click="goToDetail(relatedMovie)"
          >
            <img v-if="relatedMovie.poster" :src="relatedMovie.poster" :alt="relatedMovie.title" class="h-64 w-full object-cover">
            <div v-else class="bg-gray-300 dark:bg-gray-700 h-64 w-full"></div>
            <div class="p-4">
              <h3 class="text-md font-semibold text-gray-900 dark:text-gray-100 truncate">{{ relatedMovie.title }}</h3>
              <p v-if="relatedMovie.release_date" class="text-sm text-gray-500">{{ new Date(relatedMovie.release_date).getFullYear() }}</p>
            </div>
          </div>
        </Carousel>
      </div>

    </div>
    
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
import { ref, onMounted, watch, reactive, computed, inject } from 'vue';
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
const openAuthModal = inject('openAuthModal'); // Pro otevření přihlašovacího modalu

const movieId = computed(() => Number(route.params.id));

const {
  getMovieById, addReview, updateReview, deleteReview, 
  getWatchlist, addToWatchlist, removeFromWatchlist, updateWatchlist, // Přidáno updateWatchlist
  getMovies, getReviews, toggleLikeReview,
  getCollections, addMovieToCollection
} = useApi();

const movie = ref(null);
const reviews = ref([]);
const userCollections = ref([]); // State pro kolekce
const showCollectionDropdown = ref(false); // State pro dropdown kolekcí
const relatedMovies = ref([]);
const loading = ref(true);
const error = ref(null);

const newReview = reactive({ rating: 5, comment: '' });
const submittingReview = ref(false);

const editingReviewId = ref(null);
const editedReviewRating = ref(1);
const editedReviewComment = ref('');

const watchlist = ref([]);
const isProcessingWatchlist = ref(false);

const isConfirmModalOpen = ref(false);
const pendingDeleteReviewId = ref(null);

const today = new Date();
today.setHours(0, 0, 0, 0); // Reset time for comparison

const isMovieReleased = computed(() => {
  if (!movie.value || !movie.value.release_date) return false;
  const releaseDate = new Date(movie.value.release_date);
  releaseDate.setHours(0, 0, 0, 0); // Reset time for comparison
  return releaseDate <= today;
});

const watchlistItem = computed(() => watchlist.value.find(item => item.movie.id === movieId.value));

const getWatchlistButtonTitle = computed(() => {
  if (watchlistItem.value) {
    if (watchlistItem.value.watched) {
      return 'Odebrat ze shlédnutých';
    } else {
      return 'Odebrat ze seznamu';
    }
  } else {
    if (!isMovieReleased.value) {
      return 'Film ještě nevyšel'; // Can't mark as watched
    }
    return 'Přidat do seznamu';
  }
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

const goToDetail = (item) => {
  if (item.type === 'series') {
    router.push(`/series/${item.id}`);
  } else {
    router.push(`/movies/${item.id}`);
  }
};

const fetchUserCollections = async () => {
  if (!authStore.isLoggedIn) {
      userCollections.value = [];
      return;
  }
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
    const response = await getReviews({ movie: movieId.value });
    reviews.value = response.data.results;
  } catch (err) {
    console.error('Error fetching reviews:', err);
  }
};

const fetchWatchlist = async () => {
  if (!authStore.isLoggedIn) {
      watchlist.value = [];
      return;
  }
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

    // Načítání dat závislých na uživateli
    if (authStore.isLoggedIn) {
        await fetchWatchlist();
        await fetchUserCollections(); // Načtení kolekcí
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
  if (!authStore.isLoggedIn) { // Znovu kontrola pro jistotu
    openAuthModal('login');
    return;
  }
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
  if (!authStore.isLoggedIn) {
    openAuthModal('login');
    return;
  }
  
  // Pokud je film nevydaný a už je označen jako shlédnutý, nedovolíme to změnit
  if (!isMovieReleased.value && watchlistItem.value?.watched) {
    toast.error('Nelze změnit status shlédnutí u filmu, který ještě nevyšel.');
    return;
  }

  isProcessingWatchlist.value = true;
  try {
    if (watchlistItem.value) {
      // Pokud je již v seznamu, odebereme nebo změníme status watched (jen pokud film vyšel)
      if (watchlistItem.value.watched && !isMovieReleased.value) { // Edge case: already watched and then changed to not released
        // Nemělo by nastat, backend by to nepustil.
      } else if (!watchlistItem.value.watched && !isMovieReleased.value) {
        // přidání k vidění (ale ne shlédnutí) nevydaného filmu
        await updateWatchlist(watchlistItem.value.id, { watched: false });
      } else if (watchlistItem.value.watched && isMovieReleased.value) {
        // odebrání shlédnutí u vydaného filmu
        await removeFromWatchlist(watchlistItem.value.id); // Odebereme celý item, aby se vynuloval
      } else if (!watchlistItem.value.watched && isMovieReleased.value) {
        // označit jako shlédnuté u vydaného filmu
        await updateWatchlist(watchlistItem.value.id, { watched: true });
      } else {
        // Fallback: odebereme ze seznamu
        await removeFromWatchlist(watchlistItem.value.id);
      }
    } else {
      // Přidání do seznamu. Pokud film nevyšel, watched=false. Jinak watched=true
      await addToWatchlist(movieId.value, isMovieReleased.value); // Pass watched status to backend
    }
    await fetchWatchlist();
  } catch (err) {
    console.error("Failed to toggle watchlist:", err);
    toast.error(err.response?.data?.detail || 'Nepodařilo se aktualizovat seznam.');
  } finally {
    isProcessingWatchlist.value = false;
  }
};

const submitReview = async () => {
  if (!authStore.isLoggedIn) {
    openAuthModal('login');
    return;
  }
  submittingReview.value = true;
  try {
    await addReview({
      movie_id: movieId.value,
      rating: newReview.rating,
      comment: newReview.comment,
    });
    newReview.rating = 5;
    newReview.comment = '';
    await fetchReviews();
    toast.success('Recenze odeslána.');
  } catch (err) {
    console.error('Error submitting review:', err);
    toast.error(err.response?.data?.detail || 'Nepodařilo se odeslat recenzi.');
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
    toast.error(err.response?.data?.detail || 'Nepodařilo se aktualizovat recenzi.');
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
    toast.error(err.response?.data?.detail || 'Nepodařilo se smazat recenzi.');
  } finally {
    isConfirmModalOpen.value = false;
    pendingDeleteReviewId.value = null;
  }
};

onMounted(() => {
  if (movieId.value) {
    fetchMovie(movieId.value);
  }
});

watch(() => route.params.id, (newId) => {
  if (newId && Number(newId) !== movieId.value) {
    fetchMovie(Number(newId));
  }
});

// Sledování přihlášení a načtení dat
watch(() => authStore.isLoggedIn, (isLoggedIn) => {
  if (isLoggedIn) {
    fetchWatchlist();
    fetchUserCollections(); // Načtení kolekcí
  } else {
    watchlist.value = [];
    userCollections.value = [];
  }
});
</script>