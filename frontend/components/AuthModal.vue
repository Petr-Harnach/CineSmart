<template>
  <transition
    enter-active-class="ease-out duration-300"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="ease-in duration-200"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-center justify-center min-h-screen px-4 text-center">
        <!-- Background overlay -->
        <div 
          class="fixed inset-0 bg-gray-900 bg-opacity-75 transition-opacity backdrop-blur-sm" 
          aria-hidden="true"
          @click="$emit('close')"
        ></div>

        <!-- Modal panel -->
        <transition
          enter-active-class="ease-out duration-300"
          enter-from-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          enter-to-class="opacity-100 translate-y-0 sm:scale-100"
          leave-active-class="ease-in duration-200"
          leave-from-class="opacity-100 translate-y-0 sm:scale-100"
          leave-to-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
        >
          <div class="inline-block align-bottom bg-white dark:bg-gray-800 rounded-2xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-md sm:w-full border border-gray-200 dark:border-gray-700">
            
            <!-- Close button -->
            <button 
              @click="$emit('close')"
              type="button" 
              class="absolute top-4 right-4 text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 focus:outline-none transition-colors"
            >
              <span class="sr-only">Zavřít</span>
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>

            <div class="px-8 py-8">
              <div class="text-center mb-8">
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white" id="modal-title">
                  {{ currentView === 'login' ? 'Vítejte zpět!' : 'Připojte se k CineSmart' }}
                </h3>
                <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">
                  {{ currentView === 'login' ? 'Přihlašte se prosím do svého účtu' : 'Vytvořte si účet a začněte objevovat' }}
                </p>
              </div>
              
              <!-- Login Form -->
              <form v-if="currentView === 'login'" @submit.prevent="handleLogin" class="space-y-6">
                <div v-if="successMessage" class="bg-green-50 text-green-700 p-3 rounded-lg text-sm flex items-center">
                  <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                  {{ successMessage }}
                </div>
                <div v-if="error" class="bg-red-50 text-red-700 p-3 rounded-lg text-sm flex items-center">
                  <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path></svg>
                  {{ error }}
                </div>
                
                <div>
                  <label for="login-username" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Uživatelské jméno</label>
                  <input type="text" v-model="loginForm.username" id="login-username" class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white transition-colors" required />
                </div>
                <div>
                  <div class="flex justify-between items-center mb-1">
                    <label for="login-password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Heslo</label>
                    <!-- Removed "Zapomenuté heslo?" link -->
                  </div>
                  <input type="password" v-model="loginForm.password" id="login-password" class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white transition-colors" required />
                </div>
                
                <button type="submit" :disabled="loading" class="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-[1.02]">
                  <span v-if="loading" class="flex items-center justify-center">
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                    Přihlašování...
                  </span>
                  <span v-else>Přihlásit se</span>
                </button>
              </form>

              <!-- Register Form -->
              <form v-else @submit.prevent="handleRegister" class="space-y-6">
                <div v-if="registerErrors.non_field_errors" class="bg-red-50 text-red-700 p-3 rounded-lg text-sm">
                  <p v-for="err in registerErrors.non_field_errors" :key="err">{{ err }}</p>
                </div>
                
                <div>
                  <label for="reg-username" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Uživatelské jméno</label>
                  <input type="text" v-model="registerForm.username" id="reg-username" class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white transition-colors" required />
                  <p v-if="registerErrors.username" class="text-red-500 text-xs mt-1">{{ registerErrors.username[0] }}</p>
                </div>
                <div>
                  <label for="reg-email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
                  <input type="email" v-model="registerForm.email" id="reg-email" class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white transition-colors" required />
                  <p v-if="registerErrors.email" class="text-red-500 text-xs mt-1">{{ registerErrors.email[0] }}</p>
                </div>
                <div>
                  <label for="reg-password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Heslo</label>
                  <input type="password" v-model="registerForm.password" id="reg-password" class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white transition-colors" required />
                  <p v-if="registerErrors.password" class="text-red-500 text-xs mt-1">{{ registerErrors.password[0] }}</p>
                </div>
                
                <button type="submit" :disabled="loading" class="w-full py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-[1.02]">
                  <span v-if="loading" class="flex items-center justify-center">
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                    Vytváření účtu...
                  </span>
                  <span v-else>Vytvořit účet</span>
                </button>
              </form>
            </div>
            
            <!-- Toggle View -->
            <div class="bg-gray-50 dark:bg-gray-700/50 px-8 py-4 border-t border-gray-100 dark:border-gray-700">
              <p class="text-sm text-gray-600 dark:text-gray-400 text-center">
                {{ currentView === 'login' ? "Nemáte účet?" : "Již máte účet?" }}
                <a href="#" @click.prevent="toggleView" class="font-semibold text-blue-600 hover:text-blue-700 ml-1 transition-colors">
                  {{ currentView === 'login' ? 'Zaregistrovat se' : 'Přihlásit se' }}
                </a>
              </p>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, reactive, watch } from 'vue';
import { useAuthStore } from '../stores/auth';

const props = defineProps({
  isOpen: Boolean,
  initialView: {
    type: String,
    default: 'login' // 'login' or 'register'
  }
});

// Removed 'forgot-password' from emit
const emit = defineEmits(['close', 'login-success']); 
const authStore = useAuthStore();

const currentView = ref(props.initialView);
const loading = ref(false);
const error = ref(null);
const successMessage = ref('');

const loginForm = reactive({ username: '', password: '' });
const registerForm = reactive({ username: '', email: '', password: '' });
const registerErrors = ref({});

watch(() => props.initialView, (newView) => {
  currentView.value = newView;
  error.value = null;
  successMessage.value = '';
  registerErrors.value = {};
});

const toggleView = () => {
  currentView.value = currentView.value === 'login' ? 'register' : 'login';
  error.value = null;
  successMessage.value = '';
  registerErrors.value = {};
};

const handleLogin = async () => {
  loading.value = true;
  error.value = null;
  const success = await authStore.login(loginForm);
  loading.value = false;

  if (success) {
    emit('login-success');
    emit('close');
    loginForm.username = '';
    loginForm.password = '';
  } else {
    error.value = 'Přihlášení selhalo. Zkontrolujte prosím své údaje.';
  }
};

const handleRegister = async () => {
  loading.value = true;
  registerErrors.value = {};
  
  // 1. Pokus o registraci
  const errorResult = await authStore.register(registerForm);
  
  if (errorResult === null) {
    // Registrace úspěšná, jdeme se hned přihlásit
    try {
      const loginSuccess = await authStore.login({
        username: registerForm.username,
        password: registerForm.password
      });
      
      if (loginSuccess) {
        emit('login-success');
        emit('close');
        // Vyčistit formuláře
        registerForm.username = '';
        registerForm.email = '';
        registerForm.password = '';
      } else {
        // Fallback: přihlášení selhalo, ale registrace prošla
        successMessage.value = 'Registrace úspěšná! Prosím, přihlašte se ručně.';
        currentView.value = 'login';
        loginForm.username = registerForm.username;
        loginForm.password = '';
      }
    } catch (e) {
      // Fallback při chybě
      successMessage.value = 'Registrace úspěšná! Prosím, přihlašte se ručně.';
      currentView.value = 'login';
    }
  } else {
    registerErrors.value = errorResult;
  }
  
  loading.value = false;
};
</script>