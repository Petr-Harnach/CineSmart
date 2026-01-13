<template>
  <div class="max-w-md mx-auto mt-10">
    <h1 class="text-2xl font-bold mb-4 dark:text-gray-100">Obnovit heslo</h1>
    <form @submit.prevent="handleReset" class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
      <div v-if="error" class="bg-red-100 text-red-700 p-3 mb-4 rounded">{{ error }}</div>
      
      <div class="mb-4">
        <label for="password" class="block text-gray-700 dark:text-gray-300">Nové heslo</label>
        <input 
          type="password" 
          v-model="password" 
          id="password" 
          class="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200" 
          required
        />
      </div>

      <div class="mb-4">
        <label for="password-confirm" class="block text-gray-700 dark:text-gray-300">Potvrzení nového hesla</label>
        <input 
          type="password" 
          v-model="passwordConfirm" 
          id="password-confirm" 
          class="w-full p-2 border rounded bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200" 
          required
        />
      </div>
      
      <button 
        type="submit" 
        :disabled="loading" 
        class="w-full bg-blue-600 text-white p-2 rounded disabled:bg-blue-300 dark:bg-blue-700 dark:disabled:bg-blue-900 hover:bg-blue-700 dark:hover:bg-blue-600"
      >
        {{ loading ? 'Obnovování...' : 'Obnovit heslo' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue';
import { useApi } from '../composables/useApi';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const token = route.query.token;

const { confirmPasswordReset } = useApi();
const openAuthModal = inject('openAuthModal');

const password = ref('');
const passwordConfirm = ref('');
const loading = ref(false);
const error = ref(null);

const handleReset = async () => {
  if (password.value !== passwordConfirm.value) {
    error.value = "Hesla se neshodují.";
    return;
  }

  loading.value = true;
  error.value = null;
  try {
    await confirmPasswordReset(token, password.value);
    // Přesměrování na domovskou stránku a otevření přihlašovacího modalu
    router.push('/');
    setTimeout(() => {
        if (openAuthModal) openAuthModal('login');
        alert('Vaše heslo bylo úspěšně obnoveno. Nyní se můžete přihlásit.');
    }, 500);
  } catch (err) {
    console.error('Obnovení hesla selhalo:', err);
    error.value = err.response?.data?.detail || 'Nepodařilo se obnovit heslo. Odkaz může být neplatný nebo expirovaný.';
  } finally {
    loading.value = false;
  }
};
</script>