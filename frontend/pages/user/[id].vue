<template>
  <div v-if="loading" class="text-center text-gray-500 py-12">
    <p>Loading user profile...</p>
  </div>
  <div v-else-if="error" class="text-center text-red-500 py-12">
    <p>Failed to load user profile: {{ error.message }}</p>
  </div>
  <div v-else-if="user" class="max-w-4xl mx-auto mt-10 p-4">
    <!-- Profile Header -->
    <div class="flex flex-col items-center md:flex-row md:items-start gap-8">
      <img 
        :src="user.profile_picture || 'https://via.placeholder.com/150'" 
        alt="Profile Picture"
        class="h-32 w-32 rounded-full object-cover border-4 border-gray-200 dark:border-gray-600"
      >
      <div class="text-center md:text-left">
        <h1 class="text-4xl font-bold text-gray-800 dark:text-gray-100">{{ user.username }}</h1>
        <p v-if="user.bio" class="mt-2 text-lg text-gray-600 dark:text-gray-300">{{ user.bio }}</p>
        <p v-else class="mt-2 text-gray-500 italic">This user has not written a bio yet.</p>
      </div>
    </div>

    <hr class="my-12 border-gray-200 dark:border-gray-700">

    <!-- User's Reviews -->
    <div class="mb-12">
      <h2 class="text-3xl font-bold mb-6 text-gray-800 dark:text-gray-100">Reviews by {{ user.username }}</h2>
      <div v-if="user.reviews && user.reviews.length > 0" class="space-y-6">
        <div 
          v-for="review in user.reviews" 
          :key="review.id" 
          class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden"
        >
          <div class="p-6">
            <div class="flex items-start justify-between mb-4">
              <div>
                <h3 
                  class="text-xl font-bold text-blue-600 dark:text-blue-400 hover:underline cursor-pointer"
                >
                  <NuxtLink :to="`/movies/${review.movie.id}`">{{ review.movie.title }}</NuxtLink>
                </h3>
                <p class="text-sm text-gray-500">{{ new Date(review.created_at).toLocaleDateString() }}</p>
              </div>
              <p class="text-2xl text-yellow-500 ml-4 flex-shrink-0">{{ '⭐'.repeat(review.rating) }}</p>
            </div>
            <p class="text-gray-700 dark:text-gray-300">{{ review.comment }}</p>
          </div>
        </div>
      </div>
      <p v-else class="text-center text-gray-500 italic py-8">This user has not written any reviews yet.</p>
    </div>

    <hr class="my-12 border-gray-200 dark:border-gray-700">

    <!-- User's Public Collections -->
    <div>
      <h2 class="text-3xl font-bold mb-6 text-gray-800 dark:text-gray-100">Public Collections</h2>
      <div v-if="user.collections && user.collections.length > 0" class="space-y-6">
        <div 
          v-for="collection in user.collections" 
          :key="collection.id" 
          class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden"
        >
          <details class="group">
            <summary class="flex justify-between items-center p-6 cursor-pointer list-none">
              <div>
                <h3 class="text-xl font-bold text-gray-800 dark:text-gray-100 group-hover:text-blue-600 transition-colors">
                  {{ collection.name }}
                </h3>
                <p class="text-gray-600 dark:text-gray-400 mt-1">{{ collection.description }}</p>
              </div>
              <div class="flex items-center">
                <span class="text-sm text-gray-500 mr-2">{{ collection.items.length }} movies</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 transform group-open:rotate-180 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </summary>
            
            <div class="p-6 pt-0 border-t border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50">
              <div v-if="collection.items && collection.items.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mt-4">
                <div 
                  v-for="item in collection.items" 
                  :key="item.id" 
                  class="bg-white dark:bg-gray-800 rounded shadow-sm overflow-hidden cursor-pointer transform hover:-translate-y-1 transition-transform"
                  @click="navigateTo(`/movies/${item.movie.id}`)"
                >
                  <img v-if="item.movie.poster" :src="item.movie.poster" :alt="item.movie.title" class="h-40 w-full object-cover">
                  <div v-else class="h-40 w-full bg-gray-300 dark:bg-gray-700 flex items-center justify-center text-xs text-gray-500">No Image</div>
                  <div class="p-2">
                    <h4 class="font-semibold text-sm truncate dark:text-gray-200">{{ item.movie.title }}</h4>
                    <p class="text-xs text-gray-500">{{ item.movie.release_date ? item.movie.release_date.substring(0, 4) : 'N/A' }}</p>
                  </div>
                </div>
              </div>
              <p v-else class="text-gray-500 italic text-sm mt-2">This collection is empty.</p>
            </div>
          </details>
        </div>
      </div>
      <p v-else class="text-center text-gray-500 italic py-8">This user has no public collections.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useApi } from '../../composables/useApi'; // upravena cesta
import { useRoute, navigateTo } from '#app';

const route = useRoute();
const userId = route.params.id;

const { getUserById } = useApi();

const user = ref(null);
const loading = ref(true);
const error = ref(null);

const fetchUser = async (id) => {
  loading.value = true;
  error.value = null;
  user.value = null;
  try {
    const response = await getUserById(id);
    user.value = response.data;
  } catch (err) {
    console.error(`Error fetching user with id ${id}:`, err);
    error.value = err;
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchUser(userId);
});

// Sledovat změnu routy, pokud by se navigovalo z profilu na profil
watch(() => route.params.id, (newId) => {
  fetchUser(newId);
});
</script>
