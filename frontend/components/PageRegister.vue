<template>
  <div class="max-w-md mx-auto mt-10">
    <h1 class="text-2xl font-bold mb-4 dark:text-gray-100">Register</h1>
    <form @submit.prevent="handleRegister" class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
      <div v-if="errors.non_field_errors" class="bg-red-100 text-red-700 p-3 mb-4 rounded">
        <p v-for="err in errors.non_field_errors" :key="err">{{ err }}</p>
      </div>
      <div v-if="errors.detail" class="bg-red-100 text-red-700 p-3 mb-4 rounded">{{ errors.detail }}</div>

      <div class="mb-4">
        <label for="username" class="block text-gray-700 dark:text-gray-300">Username</label>
        <input type="text" v-model="username" id="username" class="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200" />
        <p v-if="errors.username" class="text-red-500 text-sm mt-1">{{ errors.username[0] }}</p>
      </div>
      <div class="mb-4">
        <label for="email" class="block text-gray-700 dark:text-gray-300">Email</label>
        <input type="email" v-model="email" id="email" class="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200" />
        <p v-if="errors.email" class="text-red-500 text-sm mt-1">{{ errors.email[0] }}</p>
      </div>
      <div class="mb-4">
        <label for="password" class="block text-gray-700 dark:text-gray-300">Password</label>
        <input type="password" v-model="password" id="password" class="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200" />
        <p v-if="errors.password" class="text-red-500 text-sm mt-1">{{ errors.password[0] }}</p>
      </div>
      <button type="submit" :disabled="loading" class="w-full bg-green-600 text-white p-2 rounded disabled:bg-green-300 dark:bg-green-700 dark:disabled:bg-green-900 hover:bg-green-700 dark:hover:bg-green-600">
        {{ loading ? 'Registering...' : 'Register' }}
      </button>
    </form>
    <p class="text-center mt-4 text-gray-700 dark:text-gray-300">
      Already have an account? 
      <a href="#" @click.prevent="$emit('navigate', 'login')" class="text-blue-500 hover:underline">Log in</a>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';

const emit = defineEmits(['navigate']);
const authStore = useAuthStore();

const username = ref('');
const email = ref('');
const password = ref('');
const loading = ref(false);
const errors = ref({});

const handleRegister = async () => {
  loading.value = true;
  errors.value = {};
  const errorResult = await authStore.register({ 
    username: username.value, 
    email: email.value, 
    password: password.value 
  });
  loading.value = false;

  if (errorResult === null) {
    // Úspěch, navigovat na login s úspěšnou zprávou (volitelné)
    emit('navigate', 'login', 'Registrace byla úspěšná! Nyní se můžete přihlásit.');
  } else {
    // Přiřadit chyby pro zobrazení v šabloně
    errors.value = errorResult;
  }
};
</script>
