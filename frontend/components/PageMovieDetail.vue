<template>
  <div class="max-w-4xl mx-auto mt-10">
    <button @click="$emit('navigate', 'home')" class="text-blue-500 hover:underline mb-4">&larr; Back to Movies</button>
    
    <div v-if="loading" class="text-center text-gray-500">Loading movie details...</div>
    
    <div v-else-if="error" class="text-center text-red-500">Failed to load movie: {{ error.message }}</div>

    <div v-else-if="movie" class="bg-white rounded-lg shadow-md overflow-hidden md:flex">
      <div class="md:flex-shrink-0">
        <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" class="h-96 w-full object-cover md:w-64">
        <div v-else class="bg-gray-300 h-96 w-full md:w-64 flex items-center justify-center text-gray-500">No Poster</div>
      </div>
      <div class="p-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ movie.title }}</h1>
        <p class="text-gray-600 text-lg mb-4">{{ movie.release_date }} | {{ movie.duration_minutes }} min</p>
        
        <p class="text-gray-700 mb-4">{{ movie.description }}</p>
        
        <div class="mb-4">
          <span class="font-semibold">Director:</span> 
          <span v-if="movie.director">{{ movie.director.name }}</span>
          <span v-else>N/A</span>
        </div>
        
        <div class="mb-4">
          <span class="font-semibold">Genres:</span> 
          <span v-if="movie.genres && movie.genres.length">
            {{ movie.genres.map(g => g.name).join(', ') }}
          </span>
          <span v-else>N/A</span>
        </div>

        <!-- Reviews section will go here -->
        <h2 class="text-2xl font-bold mt-8 mb-4">Reviews</h2>
        <p class="text-gray-500">No reviews yet.</p>
      </div>
    </div>
    <div v-else class="text-center text-gray-500">Movie not found.</div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useApi } from '../composables/useApi';

const props = defineProps({
  movieId: Number,
});

const emit = defineEmits(['navigate']);

const { getMovieById } = useApi();
const movie = ref(null);
const loading = ref(true);
const error = ref(null);

const fetchMovie = async (id) => {
  loading.value = true;
  error.value = null;
  try {
    const response = await getMovieById(id);
    movie.value = response.data;
  } catch (err) {
    error.value = err;
    console.error('Error fetching movie:', err);
  } finally {
    loading.value = false;
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
