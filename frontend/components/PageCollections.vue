<template>
  <div class="max-w-6xl mx-auto mt-10 p-4">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-gray-800 dark:text-gray-100">Movie Collections</h1>
      <button 
        v-if="authStore.isLoggedIn"
        @click="showCreateForm = !showCreateForm"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
      >
        {{ showCreateForm ? 'Cancel' : '+ Create Collection' }}
      </button>
    </div>

    <!-- Create Collection Form -->
    <div v-if="showCreateForm" class="mb-12 bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
      <h2 class="text-xl font-bold mb-4 dark:text-gray-100">New Collection</h2>
      <form @submit.prevent="handleCreate">
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Name</label>
          <input v-model="newCollection.name" type="text" class="w-full mt-1 p-2 border rounded-md dark:bg-gray-900 dark:border-gray-600 dark:text-gray-200" required>
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Description</label>
          <textarea v-model="newCollection.description" rows="3" class="w-full mt-1 p-2 border rounded-md dark:bg-gray-900 dark:border-gray-600 dark:text-gray-200"></textarea>
        </div>
        <div class="mb-6 flex items-center">
          <input v-model="newCollection.is_public" type="checkbox" id="is_public" class="h-4 w-4 text-blue-600 border-gray-300 rounded">
          <label for="is_public" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">Make this collection public</label>
        </div>
        <button type="submit" :disabled="isCreating" class="w-full py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:bg-green-400">
          {{ isCreating ? 'Creating...' : 'Create Collection' }}
        </button>
      </form>
    </div>

    <!-- Collections List -->
    <div v-if="loading" class="text-center text-gray-500 py-12">Loading collections...</div>
    <div v-else-if="collections.length === 0" class="text-center text-gray-500 py-12 italic">
      No collections found. Why not create the first one?
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="collection in collections" 
        :key="collection.id"
        class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 hover:border-blue-500 transition-colors cursor-pointer"
        @click="$emit('show-collection-detail', collection.id)"
      >
        <div class="flex justify-between items-start mb-2">
          <h3 class="text-xl font-bold text-gray-900 dark:text-gray-100 truncate pr-4">{{ collection.name }}</h3>
          <span v-if="!collection.is_public" class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400 text-xs rounded">Private</span>
        </div>
        <p class="text-gray-600 dark:text-gray-400 text-sm mb-4 line-clamp-2 h-10">{{ collection.description || 'No description provided.' }}</p>
        <div class="flex justify-between items-center mt-auto">
          <span class="text-xs text-gray-500">By {{ collection.user.username }}</span>
          
          <div class="flex items-center gap-3">
            <span class="text-xs font-semibold text-blue-600 dark:text-blue-400">{{ collection.items.length }} items</span>
            <button 
              v-if="authStore.user && collection.user.id === authStore.user.id"
              @click.stop="handleDelete(collection.id)"
              class="text-gray-400 hover:text-red-500 transition-colors"
              title="Delete Collection"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Confirm Modal -->
    <ConfirmModal 
      :is-open="isConfirmModalOpen" 
      :title="'Delete Collection'"
      :message="'Are you sure you want to delete this collection? This action cannot be undone.'"
      @confirm="confirmDelete" 
      @close="isConfirmModalOpen = false" 
    />
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useApi } from '../composables/useApi';
import { useAuthStore } from '../stores/auth';
import { useToast } from '../composables/useToast';
import ConfirmModal from './ConfirmModal.vue';

const emit = defineEmits(['show-collection-detail']);
const authStore = useAuthStore();
const toast = useToast();
const { getCollections, createCollection, deleteCollection } = useApi();

const collections = ref([]);
const loading = ref(true);
const showCreateForm = ref(false);
const isCreating = ref(false);

// Confirm Modal state
const isConfirmModalOpen = ref(false);
const collectionToDeleteId = ref(null);

const newCollection = reactive({
  name: '',
  description: '',
  is_public: true
});

const fetchCollections = async () => {
  loading.value = true;
  try {
    const response = await getCollections();
    collections.value = response.data.results;
  } catch (err) {
    console.error('Error fetching collections:', err);
  } finally {
    loading.value = false;
  }
};

const handleCreate = async () => {
  isCreating.value = true;
  try {
    await createCollection(newCollection);
    newCollection.name = '';
    newCollection.description = '';
    newCollection.is_public = true;
    showCreateForm.value = false;
    await fetchCollections();
    toast.success('Collection created!');
  } catch (err) {
    console.error('Error creating collection:', err);
    toast.error('Failed to create collection.');
  } finally {
    isCreating.value = false;
  }
};

const handleDelete = (id) => {
  collectionToDeleteId.value = id;
  isConfirmModalOpen.value = true;
};

const confirmDelete = async () => {
  if (!collectionToDeleteId.value) return;
  try {
    await deleteCollection(collectionToDeleteId.value);
    await fetchCollections();
    toast.success('Collection deleted.');
  } catch (err) {
    console.error('Error deleting collection:', err);
    toast.error('Failed to delete collection.');
  } finally {
    isConfirmModalOpen.value = false;
    collectionToDeleteId.value = null;
  }
};

onMounted(fetchCollections);
</script>
