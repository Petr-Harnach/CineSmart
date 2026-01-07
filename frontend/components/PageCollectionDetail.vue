<template>
  <div v-if="loading" class="text-center text-gray-500 py-12">Loading collection...</div>
  <div v-else-if="error" class="text-center text-red-500 py-12">{{ error.message }}</div>
  <div v-else-if="collection" class="max-w-6xl mx-auto mt-10 p-4">
    <div class="flex flex-col md:flex-row justify-between items-start gap-4 mb-8">
      <div>
        <h1 class="text-4xl font-bold text-gray-800 dark:text-gray-100">{{ collection.name }}</h1>
        <p class="text-gray-500 mt-1 italic">Created by {{ collection.user.username }}</p>
        <p v-if="collection.description" class="mt-4 text-gray-600 dark:text-gray-300 max-w-2xl">{{ collection.description }}</p>
      </div>
      <div v-if="isOwner" class="flex gap-2">
        <button 
          @click="handleDeleteCollection"
          class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition text-sm"
        >
          Delete Collection
        </button>
      </div>
    </div>

    <hr class="my-8 border-gray-200 dark:border-gray-700">

    <div>
      <h2 class="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-100">Movies in this collection ({{ collection.items.length }})</h2>
      <div v-if="collection.items.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div 
          v-for="item in collection.items" 
          :key="item.id" 
          class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer relative group"
          @click="$emit('show-detail', item.movie.id)"
        >
          <img v-if="item.movie.poster" :src="item.movie.poster" :alt="item.movie.title" class="h-64 w-full object-cover">
          <div v-else class="bg-gray-300 dark:bg-gray-700 h-64 w-full"></div>
          
          <div v-if="isOwner" 
               @click.stop="handleRemoveMovie(item.movie.id)"
               class="absolute top-2 right-2 p-2 bg-red-600 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-700 shadow-md"
               title="Remove from collection">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </div>

          <div class="p-4">
            <h3 class="text-md font-semibold text-gray-900 dark:text-gray-100 truncate">{{ item.movie.title }}</h3>
            <p v-if="item.movie.release_date" class="text-sm text-gray-500">{{ item.movie.release_date.substring(0, 4) }}</p>
          </div>
        </div>
      </div>
      <p v-else class="text-center text-gray-500 py-12 italic">This collection is currently empty.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useApi } from '../composables/useApi';
import { useAuthStore } from '../stores/auth';

const props = defineProps({
  collectionId: {
    type: [Number, String],
    required: true,
  },
});

const emit = defineEmits(['show-detail', 'navigate']);
const authStore = useAuthStore();
const { getCollectionById, deleteCollection, removeMovieFromCollection } = useApi();

const collection = ref(null);
const loading = ref(true);
const error = ref(null);

const isOwner = computed(() => {
  return authStore.isLoggedIn && collection.value && authStore.user && authStore.user.id === collection.value.user.id;
});

const fetchCollection = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await getCollectionById(props.collectionId);
    collection.value = response.data;
  } catch (err) {
    console.error('Error fetching collection:', err);
    error.value = err;
  } finally {
    loading.value = false;
  }
};

const handleDeleteCollection = async () => {
  if (confirm('Are you sure you want to delete this collection?')) {
    try {
      await deleteCollection(props.collectionId);
      emit('navigate', 'collections');
    } catch (err) {
      console.error('Failed to delete collection:', err);
    }
  }
};

const handleRemoveMovie = async (movieId) => {
  try {
    await removeMovieFromCollection(props.collectionId, movieId);
    await fetchCollection(); // Refresh
  } catch (err) {
    console.error('Failed to remove movie:', err);
  }
};

onMounted(fetchCollection);
</script>
