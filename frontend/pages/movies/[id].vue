<template>
  <div class="max-w-4xl mx-auto mt-10">
    <NuxtLink to="/" class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600 mb-4 inline-block">&larr; Back to Movies</NuxtLink>
    
    <div v-if="loading" class="text-center text-gray-500">Loading movie details...</div>
    
    <div v-else-if="error" class="text-center text-red-500">Failed to load movie: {{ error.message }}</div>

    <div v-else-if="movie" class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
      <div class="md:flex">
        <div class="md:flex-shrink-0">
          <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" class="h-96 w-full object-cover md:w-64">
          <div v-else class="bg-gray-300 dark:bg-gray-700 h-96 w-full md:w-64 flex items-center justify-center text-gray-500">No Poster</div>
        </div>
        <div class="p-8 w-full">
          <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">{{ movie.title }}</h1>
          <div class="flex items-center mb-4 text-gray-600 dark:text-gray-300 text-lg">
            <span v-if="movie.release_date" class="mr-2">{{ movie.release_date.substring(0, 4) }}</span>
            <span v-else class="mr-2">TBA</span>
            <span v-if="movie.duration_minutes">| {{ movie.duration_minutes }} min</span>
            <AvgRating :rating="movie.avg_rating" class="ml-4" />
          </div>
          
          <div class="flex gap-2 mb-4">
            <button 
              @click="toggleWatchlist" 
              :disabled="isProcessingWatchlist && authStore.isLoggedIn"
              class="flex-1 p-2 rounded font-semibold transition"
              :class="[
                authStore.isLoggedIn 
                  ? (watchlistItem 
                      ? 'bg-gray-200 text-gray-800 hover:bg-gray-300 dark:bg-gray-600 dark:text-gray-100 dark:hover:bg-gray-500' 
                      : 'bg-gray-800 text-white hover:bg-gray-700 dark:bg-gray-700 dark:hover:bg-gray-600')
                  : 'bg-gray-400 text-white cursor-pointer hover:bg-gray-500 dark:bg-gray-500 dark:hover:bg-gray-400'
              ]"
            >
              {{ isProcessingWatchlist ? '...' : (authStore.isLoggedIn ? (watchlistItem ? '✓ On Watchlist' : '+ Add to Watchlist') : 'Log in to add to Watchlist') }}
            </button>

            <!-- Collection Dropdown -->
            <div v-if="authStore.isLoggedIn" class="relative">
              <button 
                @click="showCollectionDropdown = !showCollectionDropdown"
                class="p-2 px-4 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-100 rounded font-semibold hover:bg-gray-200 dark:hover:bg-gray-600 transition h-full flex items-center gap-2"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                </svg>
                Collection
              </button>
              
              <div v-if="showCollectionDropdown" 
                   class="absolute right-0 top-full mt-2 w-56 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md shadow-xl z-30 overflow-hidden">
                <div v-if="userCollections.length === 0" class="p-4 text-sm text-gray-500 italic">
                  You have no collections. Create one first!
                </div>
                <div v-else>
                  <p class="px-4 py-2 text-xs font-bold text-gray-400 uppercase tracking-wider border-b border-gray-100 dark:border-gray-700">Add to:</p>
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
          
          <div v-if="movie.description" class="mb-4">
            <p class="text-gray-700 dark:text-gray-200 inline">
              {{ truncatedDescription }}
            </p>
            <button 
              v-if="movie.description.length > 250" 
              @click="isDescriptionExpanded = !isDescriptionExpanded" 
              class="text-blue-600 dark:text-blue-400 hover:underline ml-1 text-sm font-semibold"
            >
              {{ isDescriptionExpanded ? 'Show less' : 'Read more' }}
            </button>
          </div>
          <p v-else class="text-gray-500 italic mb-4">No description available.</p>
          
          <div class="mb-4 dark:text-gray-100">
            <span class="font-semibold">Directors:</span> 
            <span v-if="movie.directors && movie.directors.length" class="ml-2">
              <template v-for="(director, index) in movie.directors" :key="director.id">
                <NuxtLink :to="`/directors/${director.id}`" class="hover:underline cursor-pointer">
                  {{ director.name }}
                </NuxtLink>
                <span v-if="index < movie.directors.length - 1">, </span>
              </template>
            </span>
            <span v-else class="ml-2">N/A</span>
          </div>
          
          <div class="mb-4 dark:text-gray-100">
            <span class="font-semibold">Genres:</span> 
            <span v-if="movie.genres && movie.genres.length" class="ml-2">
              {{ movie.genres.map(g => g.name).join(', ') }}
            </span>
            <span v-else class="ml-2">N/A</span>
          </div>

          <div v-if="movie.screenwriters && movie.screenwriters.length" class="mb-4 dark:text-gray-100">
            <span class="font-semibold">Screenwriters:</span> 
            <span class="ml-2">
              <span v-for="(writer, index) in movie.screenwriters" :key="writer.id">
                {{ writer.name }}<span v-if="index < movie.screenwriters.length - 1">, </span>
              </span>
            </span>
          </div>

          <div v-if="movie.actors && movie.actors.length" class="mb-4 dark:text-gray-100">
            <span class="font-semibold">Actors:</span> 
            <span class="ml-2">
              <template v-for="(actor, index) in movie.actors" :key="actor.id">
                <NuxtLink :to="`/actors/${actor.id}`" class="hover:underline cursor-pointer">
                  {{ actor.name }}
                </NuxtLink>
                <span v-if="index < movie.actors.length - 1">, </span>
              </template>
            </span>
          </div>
        </div>
      </div>
      <div class="p-8 border-t border-gray-200 dark:border-gray-700">
        <!-- Your Review Section -->
        <div v-if="userReview" class="mb-8">
          <h3 class="text-xl font-bold mb-4 dark:text-gray-100">Your Review</h3>
          <div class="bg-blue-50 dark:bg-gray-700/50 p-4 rounded-lg shadow-sm border border-blue-200 dark:border-gray-600">
            <template v-if="editingReviewId === userReview.id">
              <form @submit.prevent="handleSaveEdit(userReview.id)">
                <div class="mb-2">
                  <label class="block text-gray-700 dark:text-gray-300 text-sm mb-1">Rating</label>
                  <RatingInput v-model="editedReviewRating" />
                </div>
                <div class="mb-2">
                  <label for="edit-comment" class="block text-gray-700 dark:text-gray-300 text-sm">Comment</label>
                  <textarea 
                    v-model="editedReviewComment" 
                    id="edit-comment" 
                    rows="2" 
                    maxlength="1000"
                    class="w-full p-1 border rounded bg-gray-100 dark:bg-gray-600 dark:text-gray-200 dark:border-gray-500"
                  ></textarea>
                  <div class="text-right text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {{ editedReviewComment.length }} / 1000
                  </div>
                </div>
                <div class="flex justify-end space-x-2">
                  <button type="button" @click="handleCancelEdit" class="px-3 py-1 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 dark:bg-gray-500 dark:text-gray-100 dark:hover:bg-gray-400">Cancel</button>
                  <button type="submit" class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700">Save Changes</button>
                </div>
              </form>
            </template>
            <template v-else>
              <div class="flex justify-between items-start mb-2">
                <p class="font-semibold dark:text-gray-100">{{ userReview.user.username }}</p>
                <p class="text-yellow-500 text-lg">{{ '⭐'.repeat(userReview.rating) }}</p>
              </div>
              <p class="text-gray-700 dark:text-gray-300 mb-3">{{ userReview.comment }}</p>
              <div class="flex justify-between items-center">
                <p class="text-gray-500 dark:text-gray-400 text-sm">{{ new Date(userReview.created_at).toLocaleDateString() }}</p>
                <div class="flex items-center gap-4">
                  <button @click="handleToggleLike(userReview)" class="flex items-center gap-1 text-gray-500 hover:text-blue-500 dark:text-gray-400 dark:hover:text-blue-400">
                    <svg v-if="userReview.user_has_liked" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 fill-blue-500 text-blue-500" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                    </svg>
                    <span>{{ userReview.likes_count }}</span>
                  </button>
                  <button @click="handleEditReview(userReview)" class="px-3 py-1 text-sm bg-gray-200 text-gray-800 rounded hover:bg-gray-300 dark:bg-gray-600 dark:text-gray-100 dark:hover:bg-gray-500">Edit</button>
                  <button @click="handleDeleteReview(userReview.id)" class="px-3 py-1 text-sm bg-red-200 text-red-800 rounded hover:bg-red-300 dark:bg-red-800 dark:text-red-200 dark:hover:bg-red-700">Delete</button>
                </div>
              </div>
            </template>
          </div>
        </div>

        <!-- Other Reviews section -->
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-2xl font-bold dark:text-gray-100">Reviews</h2>
          <div v-if="reviews.length > 0">
            <label for="sort-reviews" class="text-sm mr-2 dark:text-gray-300">Sort by:</label>
            <select id="sort-reviews" v-model="reviewSortOrder" class="p-1 border rounded-md text-sm bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200">
              <option value="-created_at">Newest</option>
              <option value="created_at">Oldest</option>
              <option value="-likes_count">Most Liked</option>
            </select>
          </div>
        </div>
        <div v-if="otherReviews.length > 0" class="space-y-4">
          <div v-for="review in otherReviews" :key="review.id" class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg shadow-sm">
            <div class="flex justify-between items-start mb-2">
              <p class="font-semibold dark:text-gray-100">
                <NuxtLink v-if="authStore.isLoggedIn && review.user.id !== authStore.user?.id" :to="`/user/${review.user.id}`" class="hover:underline">
                  {{ review.user.username }}
                </NuxtLink>
                <span v-else>{{ review.user.username }}</span>
              </p>
              <p class="text-yellow-500 text-lg">{{ '⭐'.repeat(review.rating) }}</p>
            </div>
            <p class="text-gray-700 dark:text-gray-300 mb-3">{{ review.comment }}</p>
            <div class="flex justify-between items-center">
              <p class="text-gray-500 dark:text-gray-400 text-sm">{{ new Date(review.created_at).toLocaleDateString() }}</p>
              <button @click="handleToggleLike(review)" class="flex items-center gap-1 text-gray-500 hover:text-blue-500 dark:text-gray-400 dark:hover:text-blue-400 disabled:opacity-50" :disabled="!authStore.isLoggedIn">
                <svg v-if="review.user_has_liked" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 fill-blue-500 text-blue-500" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
                <span>{{ review.likes_count }}</span>
              </button>
            </div>
          </div>
        </div>
        <p v-else-if="!userReview" class="text-gray-500 dark:text-gray-400">No reviews yet.</p>
        <p v-else class="text-gray-500 dark:text-gray-400">No other reviews yet.</p>

        <!-- New Review Form -->
        <div v-if="authStore.isLoggedIn && !userReview" class="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
          <h3 class="text-xl font-bold mb-4 dark:text-gray-100">Add Your Review</h3>
          <form @submit.prevent="submitReview" class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
            <div v-if="submitError" class="bg-red-100 text-red-700 p-3 mb-4 rounded">{{ submitError }}</div>
            <div class="mb-4">
              <label class="block text-gray-700 dark:text-gray-300 mb-1">Rating</label>
              <RatingInput v-model="newReview.rating" />
            </div>
            <div class="mb-4">
              <label for="comment" class="block text-gray-700 dark:text-gray-300">Comment</label>
              <textarea 
                v-model="newReview.comment" 
                id="comment" 
                rows="4" 
                maxlength="1000"
                class="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600"
              ></textarea>
              <div class="text-right text-xs text-gray-500 dark:text-gray-400 mt-1">
                {{ newReview.comment.length }} / 1000
              </div>
            </div>
            <button type="submit" :disabled="submittingReview" class="w-full bg-blue-500 text-white p-2 rounded disabled:bg-blue-300">
              {{ submittingReview ? 'Submitting...' : 'Submit Review' }}
            </button>
          </form>
        </div>
        <p v-else-if="!authStore.isLoggedIn" class="mt-8 text-gray-600 dark:text-gray-400">Please <a @click.prevent="$emit('navigate', 'login')" class="text-blue-500 hover:underline cursor-pointer">log in</a> to add a review.</p>
      </div>

      <!-- Related Movies Section -->
      <div v-if="relatedMovies.length > 0" class="p-8 border-t border-gray-200 dark:border-gray-700">
        <h2 class="text-2xl font-bold mt-8 mb-4 dark:text-gray-100">You might also like</h2>
        <Carousel>
          <div 
            v-for="relatedMovie in relatedMovies" 
            :key="relatedMovie.id" 
            class="flex-shrink-0 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer"
            @click="goToMovie(relatedMovie.id)"
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
    <div v-else class="text-center text-gray-500">Movie not found.</div>

    <!-- Confirm Modal -->
    <ConfirmModal 
      :is-open="isConfirmModalOpen"
      :title="'Delete Review'"
      :message="'Are you sure you want to delete your review? This action cannot be undone.'"
      @confirm="confirmDeleteReview"
      @close="isConfirmModalOpen = false"
    />
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

const goToMovie = (id) => {
  router.push(`/movies/${id}`);
};

// ... (fetch functions same as before) ...

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
    // toast.success('Added to collection!'); // Removed per user request
  } catch (err) {
    console.error('Failed to add to collection:', err);
    toast.error('Movie is already in this collection.');
  }
};

const handleToggleLike = async (review) => {
  if (!authStore.isLoggedIn) {
    // openAuthModal('login'); // TODO: Handle modal globally
    return;
  }
  try {
    if (review.user_has_liked) {
      review.likes_count--;
      review.user_has_liked = false;
    } else {
      review.likes_count++;
      review.user_has_liked = true;
    }
    await toggleLikeReview(review.id);
  } catch (err) {
    console.error('Failed to toggle like:', err);
    if (review.user_has_liked) {
      review.likes_count--;
      review.user_has_liked = false;
    } else {
      review.likes_count++;
      review.user_has_liked = true;
    }
  }
};

watch(reviewSortOrder, fetchReviews);

const toggleWatchlist = async () => {
  if (!authStore.isLoggedIn) {
    // openAuthModal('login'); // TODO
    return;
  }
  isProcessingWatchlist.value = true;
  try {
    if (watchlistItem.value) {
      await removeFromWatchlist(watchlistItem.value.id);
      // toast.success('Removed from watchlist'); // Removed
    } else {
      await addToWatchlist(movieId.value);
      // toast.success('Added to watchlist'); // Removed
    }
    await fetchWatchlist();
  } catch (err) {
    console.error("Failed to toggle watchlist:", err);
    toast.error('Failed to update watchlist');
  } finally {
    isProcessingWatchlist.value = false;
  }
};

const submitReview = async () => {
  submittingReview.value = true;
  submitError.value = null;
  try {
    await addReview({
      movie_id: movieId.value,
      rating: newReview.rating,
      comment: newReview.comment,
    });
    newReview.rating = 5;
    newReview.comment = '';
    await fetchReviews();
    // toast.success('Review submitted!'); // Removed
  } catch (err) {
    console.error('Error submitting review:', err);
    if (err.response && err.response.data) {
        const data = err.response.data;
        if (data.detail) {
            submitError.value = data.detail;
        } else {
            submitError.value = 'An unknown error occurred.';
        }
    } else {
        submitError.value = 'Failed to submit review. Please check your connection.';
    }
    toast.error('Failed to submit review');
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
  editedReviewRating.value = 1;
  editedReviewComment.value = '';
};

const handleSaveEdit = async (reviewId) => {
  try {
    await updateReview(reviewId, {
      rating: editedReviewRating.value,
      comment: editedReviewComment.value,
    });
    await fetchReviews();
    handleCancelEdit();
    // toast.success('Review updated!'); // Removed
  } catch (err) {
    console.error('Error saving review:', err);
    toast.error('Failed to update review');
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
    // toast.success('Review deleted.'); // Removed
  } catch (err) {
    console.error('Error deleting review:', err);
    toast.error('Failed to delete review');
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
  if (newId) {
    fetchMovie(Number(newId));
  }
});
</script>