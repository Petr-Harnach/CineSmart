<template>
  <div class="max-w-4xl mx-auto mt-10">
    <button @click="$emit('navigate', 'home')" class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600 mb-4">&larr; Back to Movies</button>
    
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
          <div class="flex items-center mb-4">
            <p class="text-gray-600 dark:text-gray-300 text-lg mr-4">{{ movie.release_date.substring(0, 4) }} | {{ movie.duration_minutes }} min</p>
            <AvgRating :rating="movie.avg_rating" />
          </div>
          
          <button 
            @click="toggleWatchlist" 
            :disabled="isProcessingWatchlist && authStore.isLoggedIn"
            class="mb-4 w-full p-2 rounded font-semibold"
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
          
          <p class="text-gray-700 dark:text-gray-200 mb-4">{{ movie.description }}</p>
          
          <div class="mb-4 dark:text-gray-100">
            <span class="font-semibold">Director:</span> 
            <a v-if="movie.director" @click.prevent="$emit('show-director-detail', movie.director.id)" href="#" class="ml-2 hover:underline cursor-pointer">
              {{ movie.director.name }}
            </a>
            <span v-else class="ml-2">N/A</span>
          </div>
          
          <div class="mb-4 dark:text-gray-100">
            <span class="font-semibold">Genres:</span> 
            <span v-if="movie.genres && movie.genres.length" class="ml-2">
              {{ movie.genres.map(g => g.name).join(', ') }}
            </span>
            <span v-else class="ml-2">N/A</span>
          </div>

          <div v-if="movie.screenwriter" class="mb-4 dark:text-gray-100">
            <span class="font-semibold">Screenwriter:</span> 
            <span class="ml-2">{{ movie.screenwriter }}</span>
          </div>

          <div v-if="movie.actors && movie.actors.length" class="mb-4 dark:text-gray-100">
            <span class="font-semibold">Actors:</span> 
            <span class="ml-2">
              <template v-for="(actor, index) in movie.actors" :key="actor.id">
                <a @click.prevent="$emit('show-actor-detail', actor.id)" href="#" class="hover:underline cursor-pointer">
                  {{ actor.name }}
                </a>
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
              <!-- Edit Form for User's Review -->
              <form @submit.prevent="handleSaveEdit(userReview.id)">
                <div class="mb-2">
                  <label for="edit-rating" class="block text-gray-700 dark:text-gray-300 text-sm">Rating (1-5 Stars)</label>
                  <input type="number" v-model="editedReviewRating" id="edit-rating" min="1" max="5" class="w-full p-1 border rounded bg-gray-100 dark:bg-gray-600 dark:text-gray-200 dark:border-gray-500" required />
                </div>
                <div class="mb-2">
                  <label for="edit-comment" class="block text-gray-700 dark:text-gray-300 text-sm">Comment</label>
                  <textarea v-model="editedReviewComment" id="edit-comment" rows="2" class="w-full p-1 border rounded bg-gray-100 dark:bg-gray-600 dark:text-gray-200 dark:border-gray-500"></textarea>
                </div>
                <div class="flex justify-end space-x-2">
                  <button type="button" @click="handleCancelEdit" class="px-3 py-1 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 dark:bg-gray-500 dark:text-gray-100 dark:hover:bg-gray-400">Cancel</button>
                  <button type="submit" class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700">Save Changes</button>
                </div>
              </form>
            </template>
            <template v-else>
              <!-- Display User's Review -->
              <div class="flex justify-between items-center mb-2">
                <p class="font-semibold dark:text-gray-100">{{ userReview.user.username }}</p>
                <p class="text-yellow-500">{{ '⭐'.repeat(userReview.rating) }}</p>
              </div>
              <p class="text-gray-700 dark:text-gray-300">{{ userReview.comment }}</p>
              <p class="text-gray-500 dark:text-gray-400 text-sm mt-2">{{ new Date(userReview.created_at).toLocaleDateString() }}</p>
              <div class="mt-2 flex space-x-2 justify-end">
                <button @click="handleEditReview(userReview)" class="px-3 py-1 text-sm bg-gray-200 text-gray-800 rounded hover:bg-gray-300 dark:bg-gray-600 dark:text-gray-100 dark:hover:bg-gray-500">Edit</button>
                <button @click="handleDeleteReview(userReview.id)" class="px-3 py-1 text-sm bg-red-200 text-red-800 rounded hover:bg-red-300 dark:bg-red-800 dark:text-red-200 dark:hover:bg-red-700">Delete</button>
              </div>
            </template>
          </div>
        </div>

        <!-- Other Reviews section -->
        <h2 class="text-2xl font-bold mb-4 dark:text-gray-100">Reviews</h2>
        <div v-if="otherReviews.length" class="space-y-4">
          <div v-for="review in otherReviews" :key="review.id" class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg shadow-sm">
            <div class="flex justify-between items-center mb-2">
              <p class="font-semibold dark:text-gray-100">
                <a 
                  v-if="authStore.isLoggedIn && review.user.id !== authStore.user?.id"
                  href="#" 
                  @click.prevent="$emit('show-user-profile', review.user.id)" 
                  class="hover:underline"
                >
                  {{ review.user.username }}
                </a>
                <span v-else>{{ review.user.username }}</span>
              </p>
              <p class="text-yellow-500">{{ '⭐'.repeat(review.rating) }}</p>
            </div>
            <p class="text-gray-700 dark:text-gray-300">{{ review.comment }}</p>
            <p class="text-gray-500 dark:text-gray-400 text-sm mt-2">{{ new Date(review.created_at).toLocaleDateString() }}</p>
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
              <label for="rating" class="block text-gray-700 dark:text-gray-300">Rating (1-5 Stars)</label>
              <input type="number" v-model="newReview.rating" id="rating" min="1" max="5" class="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600" required />
            </div>
            <div class="mb-4">
              <label for="comment" class="block text-gray-700 dark:text-gray-300">Comment</label>
              <textarea v-model="newReview.comment" id="comment" rows="4" class="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600"></textarea>
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
            @click="$emit('show-detail', relatedMovie.id)"
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
  </div>
</template>

<script setup>
import { ref, onMounted, watch, reactive, computed } from 'vue';
import { useApi } from '../composables/useApi';
import { useAuthStore } from '../stores/auth';
import AvgRating from './AvgRating.vue';
import Carousel from './Carousel.vue';

const props = defineProps({
  movieId: Number,
});

const emit = defineEmits(['navigate', 'show-actor-detail', 'show-director-detail', 'show-detail', 'show-user-profile']);
const authStore = useAuthStore();

const { getMovieById, addReview, updateReview, deleteReview, getWatchlist, addToWatchlist, removeFromWatchlist, getMovies } = useApi();
const movie = ref(null);
const relatedMovies = ref([]);
const loading = ref(true);
const error = ref(null);

const newReview = reactive({
  rating: 5,
  comment: '',
});
const submittingReview = ref(false);
const submitError = ref(null);

const editingReviewId = ref(null);
const editedReviewRating = ref(1);
const editedReviewComment = ref('');


const watchlist = ref([]);
const isProcessingWatchlist = ref(false);
const watchlistItem = computed(() => {
  return watchlist.value.find(item => item.movie.id === props.movieId);
});

const userReview = computed(() => {
  if (!authStore.user || !movie.value || !movie.value.reviews) return null;
  return movie.value.reviews.find(review => review.user.id === authStore.user.id);
});

const otherReviews = computed(() => {
  if (!movie.value || !movie.value.reviews) return [];
  if (!userReview.value) return movie.value.reviews;
  return movie.value.reviews.filter(review => review.id !== userReview.value.id);
});

const fetchMovie = async (id) => {
  loading.value = true;
  error.value = null;
  relatedMovies.value = [];
  try {
    const response = await getMovieById(id);
    movie.value = response.data;
    if (authStore.isLoggedIn) {
      await fetchWatchlist();
    }
    await fetchRelatedMovies(movie.value);
  } catch (err) {
    error.value = err;
    console.error('Error fetching movie:', err);
  } finally {
    loading.value = false;
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

const fetchWatchlist = async () => {
  try {
    const response = await getWatchlist();
    watchlist.value = response.data.results;
  } catch (err) {
    console.error("Failed to fetch watchlist:", err);
  }
};

const toggleWatchlist = async () => {
  if (!authStore.isLoggedIn) {
    emit('navigate', 'login');
    return;
  }
  isProcessingWatchlist.value = true;
  try {
    if (watchlistItem.value) {
      // It's on the list, remove it
      await removeFromWatchlist(watchlistItem.value.id);
    } else {
      // It's not on the list, add it
      await addToWatchlist(props.movieId);
    }
    // Refresh watchlist to update state
    await fetchWatchlist();
  } catch (err) {
    console.error("Failed to toggle watchlist:", err);
  } finally {
    isProcessingWatchlist.value = false;
  }
};

const submitReview = async () => {
  submittingReview.value = true;
  submitError.value = null;
  try {
    await addReview({
      movie_id: props.movieId,
      rating: newReview.rating,
      comment: newReview.comment,
    });
    // Clear form and refetch movie to show new review
    newReview.rating = 5;
    newReview.comment = '';
    await fetchMovie(props.movieId);
  } catch (err) {
    console.error('Error submitting review:', err);
    if (err.response && err.response.data) {
        const data = err.response.data;
        if (Array.isArray(data) && data.length > 0) {
            submitError.value = data[0];
        } else if (data.detail) {
            submitError.value = data.detail;
        } else if (data.non_field_errors) {
            submitError.value = data.non_field_errors[0];
        } else if (data.rating) {
            submitError.value = `Rating: ${data.rating[0]}`;
        } else if (data.comment) {
            submitError.value = `Comment: ${data.comment[0]}`;
        } else {
            submitError.value = 'An unknown error occurred.';
        }
    } else {
        submitError.value = 'Failed to submit review. Please check your connection.';
    }
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
    await fetchMovie(props.movieId); // Refresh movie details to show updated review
    handleCancelEdit(); // Exit edit mode
  } catch (err) {
    console.error('Error saving review:', err);
    // You might want to display an error message to the user here
  }
};

const handleDeleteReview = async (reviewId) => {
  if (confirm('Are you sure you want to delete this review?')) {
    try {
      await deleteReview(reviewId);
      await fetchMovie(props.movieId); // Refresh movie details to update review list
    } catch (err) {
      console.error('Error deleting review:', err);
      // Display error to user
    }
  }
};


onMounted(() => {
  if (props.movieId) {
    fetchMovie(props.movieId);
  }
});

watch(() => props.movieId, (newId) => {
  if (newId) {
    fetchMovie(newId);
  }
});
</script>