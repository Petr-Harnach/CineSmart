<template>
  <div class="relative">
    <div
      ref="carousel"
      class="flex overflow-x-auto space-x-4 pb-4 scroll-smooth hide-scrollbar"
      @scroll="handleScroll"
    >
      <slot></slot>
    </div>
    <button
      v-if="showPrev"
      @click="scrollLeft"
      class="absolute top-1/2 -left-4 -translate-y-1/2 bg-white dark:bg-gray-800 shadow-md text-gray-800 dark:text-white p-2 rounded-full hover:scale-110 transition-transform z-10"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
    </button>
    <button
      v-if="showNext"
      @click="scrollRight"
      class="absolute top-1/2 -right-4 -translate-y-1/2 bg-white dark:bg-gray-800 shadow-md text-gray-800 dark:text-white p-2 rounded-full hover:scale-110 transition-transform z-10"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const carousel = ref(null);
const showPrev = ref(false);
const showNext = ref(true);

const CARD_WIDTH = 192; // Corresponds to w-48 (12rem * 16px/rem)
const GAP_WIDTH = 16; // Corresponds to space-x-4 (1rem * 16px/rem)
const ITEM_WIDTH = CARD_WIDTH + GAP_WIDTH;

const handleScroll = () => {
  if (carousel.value) {
    const el = carousel.value;
    showPrev.value = el.scrollLeft > 1;
    showNext.value = el.scrollWidth - el.scrollLeft - el.clientWidth > 1;
  }
};

const scrollLeft = () => {
  if (carousel.value) {
    const visibleWidth = carousel.value.clientWidth;
    const scrollAmount = Math.floor(visibleWidth / ITEM_WIDTH) * ITEM_WIDTH;
    carousel.value.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
  }
};

const scrollRight = () => {
  if (carousel.value) {
    const visibleWidth = carousel.value.clientWidth;
    const scrollAmount = Math.floor(visibleWidth / ITEM_WIDTH) * ITEM_WIDTH;
    carousel.value.scrollBy({ left: scrollAmount, behavior: 'smooth' });
  }
};

onMounted(() => {
  if (carousel.value) {
    carousel.value.addEventListener('scroll', handleScroll);
    setTimeout(handleScroll, 100);
  }
});

onUnmounted(() => {
  if (carousel.value) {
    carousel.value.removeEventListener('scroll', handleScroll);
  }
});
</script>

<style>
.hide-scrollbar {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
.hide-scrollbar::-webkit-scrollbar {
  display: none; /* Chrome, Safari and Opera */
}
</style>