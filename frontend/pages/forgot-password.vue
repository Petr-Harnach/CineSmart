<template>
  <div class="max-w-md mx-auto mt-10">
    <h1 class="text-2xl font-bold mb-4 dark:text-gray-100">Zapomenuté heslo</h1>
    <form @submit.prevent="handleRequest" class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
      <p class="text-gray-600 dark:text-gray-300 mb-4">
        Zadejte svou e-mailovou adresu a my vám zašleme odkaz na resetování hesla.
      </p>
      <div v-if="successMessage" class="bg-green-100 text-green-700 p-3 mb-4 rounded">{{ successMessage }}</div>
      <div v-if="error" class="bg-red-100 text-red-700 p-3 mb-4 rounded">{{ error }}</div>
      
      <div class="mb-4">
        <label for="email" class="block text-gray-700 dark:text-gray-300">E-mail</label>
        <input 
          type="email" 
          v-model="email" 
          id="email" 
          class="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200" 
          required
        />
      </div>
      
      <button 
        type="submit" 
        :disabled="loading" 
        class="w-full bg-blue-600 text-white p-2 rounded disabled:bg-blue-300 dark:bg-blue-700 dark:disabled:bg-blue-900 hover:bg-blue-700 dark:hover:bg-blue-600"
      >
        {{ loading ? 'Odesílám...' : 'Odeslat e-mail pro resetování hesla' }}
      </button>
    </form>
    <p class="text-center mt-4">
      <a href="#" @click.prevent="openAuthModal('login')" class="text-sm text-blue-500 hover:underline">Zpět k přihlášení</a>
    </p>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue';
import { useApi } from '../composables/useApi';

const { requestPasswordReset } = useApi();
const openAuthModal = inject('openAuthModal');

const email = ref('');
const loading = ref(false);
const error = ref(null);
const successMessage = ref('');

const handleRequest = async () => {
  loading.value = true;
  error.value = null;
  successMessage.value = '';
  try {
    await requestPasswordReset(email.value);
    successMessage.value = 'Pokud u nás existuje účet s tímto e-mailem, odeslali jsme na něj pokyny k resetování hesla.';
  } catch (err) {
    console.error('Žádost o resetování hesla selhala:', err);
    // Zobrazíme obecnou zprávu, i když nastane chyba, abychom neprozradili, které e-maily existují
    successMessage.value = 'Pokud u nás existuje účet s tímto e-mailem, odeslali jsme na něj pokyny k resetování hesla.';
  } finally {
    loading.value = false;
  }
};
</script>