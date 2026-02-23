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
          <div class="flex flex-col md:flex-row justify-between items-start gap-4 mb-2">
            <h1 class="text-4xl font-bold text-gray-900 dark:text-gray-100">{{ movie.title }}</h1>
            
            <!-- Tlačítko Kolekce -->
            <div v-if="authStore.isLoggedIn" class="relative self-center md:self-start">
              <button 
                @click="showCollectionDropdown = !showCollectionDropdown"
                class="flex items-center gap-2 p-2 px-3 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 transition text-sm font-semibold border border-gray-200 dark:border-gray-600"
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

          <p class="text-lg text-gray-500 mb-4">{{ movie.release_date ? movie.release_date.substring(0, 4) : 'TBA' }}</p>
          
          <!-- Žánry -->
          <div class="flex flex-wrap gap-2 justify-center md:justify-start mb-6">
            <span v-for="genre in movie.genres" :key="genre.id" class="px-3 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded-full dark:bg-blue-900/30 dark:text-blue-300">
              {{ genre.name }}
            </span>
          </div>

          <!-- Popis s logikou Číst více -->
          <div v-if="movie.description" class="mb-6">
            <p class="text-gray-700 dark:text-gray-300 leading-relaxed">
              {{ truncatedDescription }}
            </p>
            <button 
              v-if="movie.description.length > 250" 
              @click="isDescriptionExpanded = !isDescriptionExpanded" 
              class="text-blue-600 dark:text-blue-400 hover:underline mt-1 text-sm font-semibold"
            >
              {{ isDescriptionExpanded ? 'Zobrazit méně' : 'Číst více' }}
            </button>
          </div>
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
      
      <!-- RECENZE SEKCE (Sjednoceno se seriály) -->
      <div class="mt-12">
        <div class="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
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
              <div class="flex items-center gap-4 mb-3">
                <span class="text-2xl font-black text-gray-900 dark:text-white">{{ userReview.rating }} <span class="text-yellow-500 text-xl">★</span></span>
                <div class="h-4 w-px bg-gray-300 dark:bg-gray-700"></div>
                <span class="text-sm font-bold text-gray-500 uppercase">{{ new Date(userReview.created_at).toLocaleDateString() }}</span>
              </div>
              <p class="text-gray-700 dark:text-gray-300 leading-relaxed text-sm">{{ userReview.comment }}</p>
            </div>
          </div>

          <!-- Ostatní recenze -->
          <div v-if="otherReviews.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div v-for="review in otherReviews" :key="review.id" class="bg-gray-50 dark:bg-gray-800/50 p-6 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm transition-transform hover:shadow-md">
              <div class="flex justify-between items-start mb-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-black text-sm uppercase">
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
              <p class="text-gray-600 dark:text-gray-400 text-sm leading-relaxed italic">{{ review.comment }}</p>
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
                <textarea v-model="newReview.comment" placeholder="Jak se vám tento film líbil? Co říkáte na obsazení nebo atmosféru?" class="w-full p-4 border rounded-2xl dark:bg-gray-900 dark:border-gray-700 dark:text-white focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all" rows="4"></textarea>
              </div>
              <button type="submit" :disabled="submittingReview" class="w-full md:w-auto px-10 py-4 bg-blue-600 hover:bg-blue-500 text-white rounded-2xl text-sm font-black uppercase tracking-widest transition-all transform hover:scale-105 shadow-xl shadow-blue-600/20 disabled:opacity-50">
                Odeslat recenzi
              </button>
            </form>
          </div>
        </div>
      </div>

      <!-- Sekce Obsazení -->
      <div v-if="movie.actors && movie.actors.length" class="mt-12">
        <h2 class="text-2xl font-bold mb-4 text-gray-900 dark:text-gray-100">Obsazení</h2>
        <Carousel>
          <NuxtLink v-for="actor in movie.actors" :key="actor.id" :to="`/actors/${actor.id}`" class="flex-shrink-0 w-32 text-center group">
            <div class="aspect-[2/3] w-full bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform group-hover:-translate-y-1 transition-transform border border-gray-200 dark:border-gray-700">
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
            class="flex-shrink-0 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer border border-gray-200 dark:border-gray-700"
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
const openAuthModal = inject('openAuthModal');

const movieId = computed(() => Number(route.params.id));

const {
  getMovieById, addReview, updateReview, deleteReview, 
  getWatchlist, addToWatchlist, removeFromWatchlist, 
  getMovies, getReviews, getCollections, addMovieToCollection
} = useApi();

const movie = ref(null);
const reviews = ref([]);
const userCollections = ref([]);
const showCollectionDropdown = ref(false);
const relatedMovies = ref([]);
const loading = ref(true);
const error = ref(null);

const isDescriptionExpanded = ref(false);

const newReview = reactive({ rating: 5, comment: '' });
const submittingReview = ref(false);

const editingReviewId = ref(null);
const editedReviewRating = ref(1);
const editedReviewComment = ref('');

const watchlist = ref([]);
const isProcessingWatchlist = ref(false);

const isConfirmModalOpen = ref(false);
const pendingDeleteReviewId = ref(null);

const watchlistItem = computed(() => watchlist.value.find(item => item.movie.id === movieId.value));

const truncatedDescription = computed(() => {
  if (!movie.value || !movie.value.description) return '';
  if (isDescriptionExpanded.value || movie.value.description.length <= 250) {
    return movie.value.description;
  }
  return movie.value.description.substring(0, 250) + '...';
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
  if (!authStore.isLoggedIn) return;
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
  if (!authStore.isLoggedIn) {
    openAuthModal('login');
    return;
  }
  
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

const submitReview = async () => {
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

// Sledování přihlášení a načtení watchlistu
watch(() => authStore.isLoggedIn, (isLoggedIn) => {
  if (isLoggedIn) {
    fetchWatchlist();
    fetchUserCollections();
  } else {
    watchlist.value = [];
    userCollections.value = [];
  }
});
</script>