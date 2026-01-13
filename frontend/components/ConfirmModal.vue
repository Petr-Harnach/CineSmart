<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm" @click.self="cancel">
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-md p-6 transform transition-all scale-100">
      <h3 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">{{ title }}</h3>
      <p class="text-gray-600 dark:text-gray-300 mb-6">{{ message }}</p>
      
      <div class="flex justify-end space-x-3">
        <button 
          @click="cancel"
          class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600 transition"
        >
          Zrušit
        </button>
        <button 
          @click="confirm"
          class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
        >
          Potvrdit
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  isOpen: Boolean,
  title: {
    type: String,
    default: 'Potvrdit akci'
  },
  message: {
    type: String,
    default: 'Opravdu chcete pokračovat?'
  }
});

const emit = defineEmits(['confirm', 'close']);

const confirm = () => {
  emit('confirm');
};

const cancel = () => {
  emit('close');
};
</script>
