<script setup>
import { RouterView } from 'vue-router'
import TheNavbar from './components/TheNavbar.vue'
</script>

<template>
  <div id="app-container" class="bg-gray-100 min-h-screen">
    <TheNavbar />
    <main class="container mx-auto p-4">
      <RouterView />
    </main>
  </div>
</template>

<style>
/* Global styles can go here if needed, but we primarily use Tailwind classes */
body {
  font-family: 'Inter', sans-serif;
}
</style>
