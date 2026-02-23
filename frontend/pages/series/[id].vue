<template>
  <div class="max-w-6xl mx-auto mt-10 p-4">
    <NuxtLink to="/" class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600 mb-4 inline-block">&larr; Zpět</NuxtLink>
    
    <div v-if="loading" class="text-center text-gray-500 py-12">Načítám detaily seriálu...</div>
    <div v-else-if="error" class="text-center text-red-500 py-12">Nepodařilo se načíst seriál: {{ error.message }}</div>

    <div v-else-if="series" class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
      <!-- Hlavička seriálu -->
      <div class="md:flex">
        <!-- PLAKÁT S TLAČÍTKEM -->
        <div class="md:flex-shrink-0 relative group">
          <img v-if="series.poster" :src="series.poster" :alt="series.title" class="h-96 w-full object-cover md:w-80">
          <div v-else class="bg-gray-300 dark:bg-gray-700 h-96 w-full md:w-80 flex items-center justify-center text-gray-500">Žádný plakát</div>
          
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
        
        <div class="p-8 w-full">
          <div class="flex justify-between items-start mb-2">
            <h1 class="text-4xl font-bold text-gray-900 dark:text-gray-100">{{ series.title }}</h1>
            
            <!-- Tlačítko Kolekce (Ikonka knížky) -->
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

          <div class="flex flex-wrap items-center mb-6 text-gray-600 dark:text-gray-300 text-lg gap-4">
            <span v-if="series.release_date">
              {{ series.release_date.substring(0, 4) }}
              <span v-if="series.end_date"> – {{ series.end_date.substring(0, 4) }}</span>
              <span v-else> – Současnost</span>
            </span>
            <span v-else>TBA</span>
            
            <span v-if="series.seasons && series.seasons.length" class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded dark:bg-blue-900 dark:text-blue-200">
              {{ series.seasons.length }} {{ series.seasons.length === 1 ? 'Série' : (series.seasons.length < 5 ? 'Série' : 'Sérií') }}
            </span>

            <AvgRating :rating="series.avg_rating" />
          </div>
          
          <div v-if="series.description" class="mb-6">
            <h3 class="font-bold text-gray-900 dark:text-gray-100 mb-1">Popis</h3>
            <p class="text-gray-700 dark:text-gray-200 leading-relaxed">{{ series.description }}</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm border-t border-gray-100 dark:border-gray-700 pt-4">
            <div v-if="series.directors && series.directors.length">
              <span class="font-bold text-gray-900 dark:text-gray-100">Tvůrci/Režie:</span>
              <span class="text-gray-600 dark:text-gray-300 ml-2">
                <template v-for="(d, i) in series.directors" :key="d.id">
                  <NuxtLink :to="`/directors/${d.id}`" class="hover:underline">{{ d.name }}</NuxtLink><span v-if="i < series.directors.length - 1">, </span>
                </template>
              </span>
            </div>
            <div v-if="series.genres && series.genres.length">
              <span class="font-bold text-gray-900 dark:text-gray-100">Žánry:</span>
              <span class="text-gray-600 dark:text-gray-300 ml-2">{{ series.genres.map(g => g.name).join(', ') }}</span>
            </div>
          </div>
        </div>
      </div>

      <hr class="border-gray-200 dark:border-gray-700">

      <div class="p-8 bg-gray-50 dark:bg-gray-900/50">
        <h2 class="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-100">Epizody</h2>
        
        <div v-if="series.seasons && series.seasons.length > 0">
          <div class="flex overflow-x-auto space-x-2 mb-6 pb-2 border-b border-gray-200 dark:border-gray-700">
            <button 
              v-for="(season, index) in series.seasons" 
              :key="season.id"
              @click="selectedSeasonIndex = index"
              class="px-4 py-2 whitespace-nowrap rounded-t-lg font-medium transition-colors"
              :class="selectedSeasonIndex === index 
                ? 'bg-white dark:bg-gray-800 text-blue-600 dark:text-blue-400 border-b-2 border-blue-600' 
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'"
            >
              {{ season.season_number }}. Série
            </button>
          </div>

          <div v-if="currentSeason" class="space-y-4">
            <div class="mb-4">
              <h3 class="text-xl font-bold text-gray-800 dark:text-gray-100">
                {{ currentSeason.title || `${currentSeason.season_number}. Série` }}
              </h3>
              <p v-if="currentSeason.release_date" class="text-sm text-gray-500">
                Premiéra: {{ new Date(currentSeason.release_date).getFullYear() }}
              </p>
              <p v-if="currentSeason.overview" class="text-gray-600 dark:text-gray-300 mt-2">
                {{ currentSeason.overview }}
              </p>
            </div>

            <div v-if="currentSeason.episodes && currentSeason.episodes.length > 0" class="space-y-4">
              <div 
                v-for="episode in currentSeason.episodes" 
                :key="episode.id" 
                class="flex flex-col sm:flex-row bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden hover:shadow-md transition-shadow"
              >
                <div class="sm:w-48 flex-shrink-0 relative">
                  <img 
                    v-if="getEpisodeImage(episode)" 
                    :src="getEpisodeImage(episode)" 
                    :alt="episode.title" 
                    class="w-full h-32 object-cover"
                  >
                  <div v-else class="w-full h-32 bg-gray-300 dark:bg-gray-700 flex items-center justify-center text-gray-500 text-xs">
                    Bez náhledu
                  </div>
                  <div class="absolute bottom-1 right-1 bg-black bg-opacity-75 text-white text-xs px-1 rounded">
                    {{ episode.episode_number }}
                  </div>
                </div>
                
                <div class="p-4 flex-grow">
                  <div class="flex justify-between items-start">
                    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100">
                      {{ episode.episode_number }}. {{ episode.title }}
                    </h4>
                    <span v-if="episode.runtime" class="text-xs font-mono bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-gray-600 dark:text-gray-300">
                      {{ episode.runtime }} min
                    </span>
                  </div>
                  <p class="text-xs text-gray-500 mb-2">
                    {{ episode.air_date ? new Date(episode.air_date).toLocaleDateString('cs-CZ') : 'Datum neznámé' }}
                  </p>
                  <p class="text-sm text-gray-600 dark:text-gray-300 line-clamp-2">
                    {{ episode.overview || 'Popis epizody není k dispozici.' }}
                  </p>
                  
                  <div v-if="episode.directors?.length || episode.guest_stars?.length" class="mt-3 text-xs text-gray-500 dark:text-gray-400">
                    <span v-if="episode.directors?.length">
                      <strong>Režie:</strong> {{ episode.directors.map(d => d.name).join(', ') }}
                    </span>
                    <span v-if="episode.guest_stars?.length" class="ml-3">
                      <strong>Hosté:</strong> {{ episode.guest_stars.map(a => a.name).join(', ') }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-500 italic">
              Tato série zatím nemá žádné epizody.
            </div>
          </div>
        </div>
      </div>

      <hr class="border-gray-200 dark:border-gray-700">

      <!-- Recenze -->
      <div class="p-8">
        <div v-if="userReview" class="mb-8">
          <h3 class="text-xl font-bold mb-4 dark:text-gray-100">Vaše recenze</h3>
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

        <h2 class="text-2xl font-bold mb-4 dark:text-gray-100">Recenze</h2>
        <div v-if="otherReviews.length > 0" class="space-y-4">
          <div v-for="review in otherReviews" :key="review.id" class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-100 dark:border-gray-700">
            <div class="flex justify-between items-start mb-2">
              <p class="font-semibold dark:text-gray-100">{{ review.user.username }}</p>
              <p class="text-yellow-500">{{ '⭐'.repeat(review.rating) }}</p>
            </div>
            <p class="text-gray-700 dark:text-gray-300 text-sm">{{ review.comment }}</p>
          </div>
        </div>
        <p v-else-if="!userReview" class="text-gray-500 italic text-center py-4">Zatím žádné recenze.</p>

        <div v-if="authStore.isLoggedIn && !userReview" class="mt-8">
          <h3 class="font-bold mb-4 dark:text-gray-100">Přidat recenzi</h3>
          <form @submit.prevent="submitReview" class="space-y-4">
            <RatingInput v-model="newReview.rating" />
            <textarea v-model="newReview.comment" placeholder="Napište svůj názor na seriál..." class="w-full p-3 border rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white" rows="3"></textarea>
            <button type="submit" :disabled="submittingReview" class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-blue-400">Odeslat</button>
          </form>
        </div>
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