<template>
  <nav class="bg-gray-800 p-4">
    <div class="container mx-auto flex justify-between items-center">
      <router-link to="/" class="text-white text-lg font-bold">CineSmart</router-link>
      <div class="space-x-4">
        <router-link to="/" class="text-gray-300 hover:text-white">Home</router-link>
        <!-- Add other links like Login/Register later -->
      </div>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>
