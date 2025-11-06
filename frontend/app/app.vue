<template>
  <div class="bg-gray-100 min-h-screen">
    <TheNavbar />
    <main class="container mx-auto p-4">
      <PageHome />
    </main>
  </div>
</template>

<script setup>
import TheNavbar from '../components/TheNavbar.vue';
import PageHome from '../components/PageHome.vue';
</script>
