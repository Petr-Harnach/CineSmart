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
    <div>
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
                  @click="$emit('show-detail', review.movie.id)" 
                  class="text-xl font-bold text-blue-600 dark:text-blue-400 hover:underline cursor-pointer"
                >
                  {{ review.movie.title }}
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
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useApi } from '../composables/useApi';

const props = defineProps({
  userId: {
    type: [Number, String],
    required: true,
  },
});

const emit = defineEmits(['show-detail']);

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
  fetchUser(props.userId);
});

watch(() => props.userId, (newId) => {
  fetchUser(newId);
});
</script>
