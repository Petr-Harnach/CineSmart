<template>
  <div class="flex items-center text-sm">
    <span v-if="rating" class="text-yellow-500 mr-1">⭐</span>
    <span v-if="rating" class="text-gray-700 dark:text-gray-300">{{ formattedRating }}</span>
    <span v-else class="text-gray-500 dark:text-gray-400">N/A</span>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  rating: {
    type: Number,
    default: 0,
  },
});

const formattedRating = computed(() => {
  return props.rating ? props.rating.toFixed(1) : 'N/A';
});
</script>
