<template>
  <div v-if="loading" class="text-center text-gray-500 py-12">
    <p>Loading actor details...</p>
  </div>
  <div v-else-if="error" class="text-center text-red-500 py-12">
    <p>Failed to load actor details: {{ error.message }}</p>
  </div>
  <div v-else-if="actor" class="max-w-6xl mx-auto mt-10 p-4">
    <div class="flex flex-col md:flex-row gap-8">
      <div class="md:w-1/3 text-center">
        <img v-if="actor.photo" :src="actor.photo" :alt="actor.name" class="w-full h-auto rounded-lg shadow-lg mx-auto">
        <div v-else class="w-full h-96 bg-gray-300 dark:bg-gray-700 rounded-lg flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
        </div>
      </div>
      <div class="md:w-2/3">
        <h1 class="text-4xl font-bold text-gray-800 dark:text-gray-100">{{ actor.name }}</h1>
        <p v-if="actor.bio" class="mt-4 text-gray-600 dark:text-gray-300 whitespace-pre-wrap">{{ actor.bio }}</p>
        <p v-else class="mt-4 text-gray-500 italic">No biography available.</p>
      </div>
    </div>

    <hr class="my-12 border-gray-200 dark:border-gray-700">

    <div>
      <h2 class="text-3xl font-bold mb-6 text-gray-800 dark:text-gray-100">Filmography</h2>
      <div v-if="actor.movies && actor.movies.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div 
          v-for="movie in actor.movies" 
          :key="movie.id" 
          class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer"
          @click="navigateTo(`/movies/${movie.id}`)"
        >
          <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" class="h-64 w-full object-cover">
          <div v-else class="bg-gray-300 dark:bg-gray-700 h-64 w-full"></div>
          <div class="p-4">
            <h3 class="text-md font-semibold text-gray-900 dark:text-gray-100 truncate">{{ movie.title }}</h3>
            <p v-if="movie.release_date" class="text-sm text-gray-500">{{ new Date(movie.release_date).getFullYear() }}</p>
          </div>
        </div>
      </div>
      <p v-else class="text-center text-gray-500 italic">No movies found in our database for this actor.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useApi } from '../../composables/useApi';
import { useRoute, navigateTo } from '#app';

const route = useRoute();
const actorId = route.params.id;

const { getActorById } = useApi();

const actor = ref(null);
const loading = ref(true);
const error = ref(null);

const fetchActor = async (id) => {
  loading.value = true;
  error.value = null;
  actor.value = null;
  try {
    const response = await getActorById(id);
    actor.value = response.data;
  } catch (err) {
    console.error(`Error fetching actor with id ${id}:`, err);
    error.value = err;
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchActor(actorId);
});

// Znovu načíst data, pokud se změní actorId
watch(() => route.params.id, (newId) => {
  fetchActor(newId);
});
</script>
