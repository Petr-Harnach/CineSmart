<template>
  <div class="bg-gray-100 dark:bg-gray-900 min-h-screen flex flex-col">
    <TheNavbar 
      @navigate="navigateTo" 
      @filter-change="handleFilterChange" 
      @show-detail="showMovieDetail"
      :show-filters="currentPage === 'home'" 
    />
    <main class="container mx-auto p-4 flex-grow">
      <PageHome 
        v-if="currentPage === 'home'" 
        @show-detail="showMovieDetail"
        @show-actor-detail="showActorDetail" 
        :filters="activeFilters" 
        @navigate="navigateTo"
      />
      <PageLogin v-else-if="currentPage === 'login'" @navigate="navigateTo" :success-message="appSuccessMessage" />
      <PageRegister v-else-if="currentPage === 'register'" @navigate="navigateTo" />
      <PageMovieDetail 
        v-else-if="currentPage === 'movie-detail'" 
        :movie-id="selectedMovieId" 
        @navigate="navigateTo" 
        @show-actor-detail="showActorDetail"
        @show-director-detail="showDirectorDetail"
        @show-detail="showMovieDetail"
      />
      <PageActorDetail 
        v-else-if="currentPage === 'actor-detail'"
        :actor-id="selectedActorId"
        @navigate="navigateTo"
        @show-detail="showMovieDetail"
      />
      <PageDirectorDetail 
        v-else-if="currentPage === 'director-detail'"
        :director-id="selectedDirectorId"
        @navigate="navigateTo"
        @show-detail="showMovieDetail"
      />
      <PageProfile 
        v-else-if="currentPage === 'profile'"
        @navigate="navigateTo"
      />
      <PageForgotPassword 
        v-else-if="currentPage === 'forgot-password'"
        @navigate="navigateTo"
      />
      <PageResetPassword
        v-else-if="currentPage === 'reset-password'"
        :token="selectedResetToken"
        @navigate="navigateTo"
      />
      <PageViewUserProfile 
        v-else-if="currentPage === 'user-profile'"
        :user-id="selectedUserProfileId"
        @navigate="navigateTo"
        @show-detail="showMovieDetail"
      />
      <PageWatchlist 
        v-else-if="currentPage === 'watchlist'" 
        @navigate="navigateTo" 
        @show-detail="showMovieDetail" 
      />
    </main>
    <TheFooter />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import TheNavbar from '../components/TheNavbar.vue';
import PageHome from '../components/PageHome.vue';
import PageLogin from '../components/PageLogin.vue';
import PageRegister from '../components/PageRegister.vue';
import PageMovieDetail from '../components/PageMovieDetail.vue';
import PageActorDetail from '../components/PageActorDetail.vue';
import PageDirectorDetail from '../components/PageDirectorDetail.vue';
import PageProfile from '../components/PageProfile.vue';
import PageViewUserProfile from '../components/PageViewUserProfile.vue';
import PageForgotPassword from '../components/PageForgotPassword.vue';
import PageResetPassword from '../components/PageResetPassword.vue';
import PageWatchlist from '../components/PageWatchlist.vue';
import TheFooter from '../components/TheFooter.vue';

const currentPage = ref('home');
const selectedMovieId = ref(null);
const selectedActorId = ref(null);
const selectedDirectorId = ref(null);
const selectedUserProfileId = ref(null);
const selectedResetToken = ref(null);
const appSuccessMessage = ref(null);
const activeFilters = ref({});

onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search);
  const page = urlParams.get('page');
  const token = urlParams.get('token');

  if (page === 'reset-password' && token) {
    selectedResetToken.value = token;
    currentPage.value = 'reset-password';
  }
});

const navigateTo = (page, message = null) => {
  console.log('Navigating to:', page, 'with message:', message);
  currentPage.value = page;
  selectedMovieId.value = null; 
  selectedActorId.value = null;
  selectedDirectorId.value = null;
  selectedUserProfileId.value = null;
  selectedResetToken.value = null;
  appSuccessMessage.value = message;
};

const showMovieDetail = (id) => {
  console.log('Showing movie detail, clearing message');
  selectedMovieId.value = id;
  currentPage.value = 'movie-detail';
  appSuccessMessage.value = null;
};

const showActorDetail = (id) => {
  selectedActorId.value = id;
  currentPage.value = 'actor-detail';
};

const showDirectorDetail = (id) => {
  selectedDirectorId.value = id;
  currentPage.value = 'director-detail';
};

const showUserProfile = (id) => {
  selectedUserProfileId.value = id;
  currentPage.value = 'user-profile';
};

const handleFilterChange = (filters) => {
  activeFilters.value = filters;
};
</script>
