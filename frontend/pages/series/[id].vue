<template>
  <div class="max-w-6xl mx-auto mt-10 p-4">
    <NuxtLink to="/" class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600 mb-4 inline-block">&larr; Zpět</NuxtLink>
    
    <div v-if="loading" class="text-center text-gray-500 py-12">Načítám detaily seriálu...</div>
    <div v-else-if="error" class="text-center text-red-500 py-12">Nepodařilo se načíst seriál: {{ error.message }}</div>

    <div v-else-if="series" class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
      <!-- Hlavička seriálu -->
      <div class="md:flex">
        <div class="md:flex-shrink-0 relative group">
          <img v-if="series.poster" :src="series.poster" :alt="series.title" class="h-96 w-full object-cover md:w-80">
          <div v-else class="bg-gray-300 dark:bg-gray-700 h-96 w-full md:w-80 flex items-center justify-center text-gray-500">Žádný plakát</div>
          
          <!-- Tlačítko Watchlist (Overlay) -->
          <button 
            @click.stop="toggleWatchlist"
            class="absolute top-2 right-2 bg-gray-900/60 text-white p-2 rounded-full hover:bg-gray-900/80 transition-all opacity-0 group-hover:opacity-100"
            :title="watchlistItem ? 'Odebrat ze seznamu' : 'Přidat do seznamu'"
          >
            <svg v-if="!watchlistItem" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </button>
        </div>
        
        <div class="p-8 w-full">
          <h1 class="text-4xl font-bold text-gray-900 dark:text-gray-100 mb-2">{{ series.title }}</h1>
          <div class="flex flex-wrap items-center mb-6 text-gray-600 dark:text-gray-300 text-lg gap-4">
            <!-- Roky vysílání -->
            <span v-if="series.release_date">
              {{ series.release_date.substring(0, 4) }}
              <span v-if="series.end_date"> – {{ series.end_date.substring(0, 4) }}</span>
              <span v-else> – Současnost</span>
            </span>
            <span v-else>TBA</span>
            
            <!-- Počet sérií -->
            <span v-if="series.seasons && series.seasons.length" class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded dark:bg-blue-900 dark:text-blue-200">
              {{ series.seasons.length }} {{ series.seasons.length === 1 ? 'Série' : (series.seasons.length < 5 ? 'Série' : 'Sérií') }}
            </span>

            <AvgRating :rating="series.avg_rating" />
          </div>
          
          <div v-if="series.description" class="mb-6">
            <h3 class="font-bold text-gray-900 dark:text-gray-100 mb-1">Popis</h3>
            <p class="text-gray-700 dark:text-gray-200 leading-relaxed">{{ series.description }}</p>
          </div>

          <!-- Štáb (Showrunners/Main Cast) -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div v-if="series.directors && series.directors.length">
              <span class="font-bold text-gray-900 dark:text-gray-100">Tvůrci/Režie:</span>
              <span class="text-gray-600 dark:text-gray-300 ml-2">
                <template v-for="(d, i) in series.directors" :key="d.id">
                  <NuxtLink :to="`/directors/${d.id}`" class="hover:underline">{{ d.name }}</NuxtLink><span v-if="i < series.directors.length - 1">, </span>
                </template>
              </span>
            </div>
            <div v-if="series.genres && series.genres.length">
              <span class="font-bold text-gray-900 dark:text-gray-100">Žánry:</span>
              <span class="text-gray-600 dark:text-gray-300 ml-2">{{ series.genres.map(g => g.name).join(', ') }}</span>
            </div>
          </div>
        </div>
      </div>

      <hr class="border-gray-200 dark:border-gray-700">

      <!-- SEKCIE SÉRIE A EPIZODY -->
      <div class="p-8 bg-gray-50 dark:bg-gray-900/50">
        <h2 class="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-100">Epizody</h2>
        
        <div v-if="series.seasons && series.seasons.length > 0">
          <!-- Taby pro výběr série -->
          <div class="flex overflow-x-auto space-x-2 mb-6 pb-2 border-b border-gray-200 dark:border-gray-700">
            <button 
              v-for="(season, index) in series.seasons" 
              :key="season.id"
              @click="selectedSeasonIndex = index"
              class="px-4 py-2 whitespace-nowrap rounded-t-lg font-medium transition-colors"
              :class="selectedSeasonIndex === index 
                ? 'bg-white dark:bg-gray-800 text-blue-600 dark:text-blue-400 border-b-2 border-blue-600' 
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'"
            >
              {{ season.season_number }}. Série
            </button>
          </div>

          <!-- Seznam epizod pro vybranou sérii -->
          <div v-if="currentSeason" class="space-y-4">
            <div class="mb-4">
              <h3 class="text-xl font-bold text-gray-800 dark:text-gray-100">
                {{ currentSeason.title || `${currentSeason.season_number}. Série` }}
              </h3>
              <p v-if="currentSeason.release_date" class="text-sm text-gray-500">
                Premiéra: {{ new Date(currentSeason.release_date).getFullYear() }}
              </p>
              <p v-if="currentSeason.overview" class="text-gray-600 dark:text-gray-300 mt-2">
                {{ currentSeason.overview }}
              </p>
            </div>

            <div v-if="currentSeason.episodes && currentSeason.episodes.length > 0" class="space-y-4">
              <div 
                v-for="episode in currentSeason.episodes" 
                :key="episode.id" 
                class="flex flex-col sm:flex-row bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden hover:shadow-md transition-shadow"
              >
                <!-- Obrázek epizody -->
                <div class="sm:w-48 flex-shrink-0 relative">
                  <!-- LOGIKA OBRÁZKU: Still -> Season Poster -> Series Poster -> Placeholder -->
                  <img 
                    v-if="getEpisodeImage(episode)" 
                    :src="getEpisodeImage(episode)" 
                    :alt="episode.title" 
                    class="w-full h-32 object-cover"
                  >
                  <div v-else class="w-full h-32 bg-gray-300 dark:bg-gray-700 flex items-center justify-center text-gray-500 text-xs">
                    Bez náhledu
                  </div>
                  <div class="absolute bottom-1 right-1 bg-black bg-opacity-75 text-white text-xs px-1 rounded">
                    {{ episode.episode_number }}
                  </div>
                </div>
                
                <!-- Info o epizodě -->
                <div class="p-4 flex-grow">
                  <div class="flex justify-between items-start">
                    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100">
                      {{ episode.episode_number }}. {{ episode.title }}
                    </h4>
                    <span v-if="episode.runtime" class="text-xs font-mono bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-gray-600 dark:text-gray-300">
                      {{ episode.runtime }} min
                    </span>
                  </div>
                  <p class="text-xs text-gray-500 mb-2">
                    {{ episode.air_date ? new Date(episode.air_date).toLocaleDateString('cs-CZ') : 'Datum neznámé' }}
                  </p>
                  <p class="text-sm text-gray-600 dark:text-gray-300 line-clamp-2">
                    {{ episode.overview || 'Popis epizody není k dispozici.' }}
                  </p>
                  
                  <!-- Štáb epizody (rozbalovací?) -->
                  <div v-if="episode.directors?.length || episode.guest_stars?.length" class="mt-3 text-xs text-gray-500 dark:text-gray-400">
                    <span v-if="episode.directors?.length">
                      <strong>Režie:</strong> {{ episode.directors.map(d => d.name).join(', ') }}
                    </span>
                    <span v-if="episode.guest_stars?.length" class="ml-3">
                      <strong>Hosté:</strong> {{ episode.guest_stars.map(a => a.name).join(', ') }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-500 italic">
              Tato série zatím nemá žádné epizody.
            </div>
          </div>
        </div>
        <div v-else class="text-center py-12 text-gray-500 italic">
          Informace o sériích nejsou k dispozici.
        </div>
      </div>

      <hr class="border-gray-200 dark:border-gray-700">

      <!-- Sekce Recenze (Stejná jako u filmů) -->
      <div class="p-8">
        <h2 class="text-2xl font-bold mb-4 dark:text-gray-100">Recenze</h2>
        <!-- (Zde by byl kód pro recenze, pro stručnost zkopíruji jen základní zobrazení, nebo můžeme použít komponentu) -->
        <div v-if="series.reviews && series.reviews.length > 0" class="space-y-4">
          <div v-for="review in series.reviews" :key="review.id" class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
            <div class="flex justify-between">
              <span class="font-bold dark:text-gray-200">{{ review.user.username }}</span>
              <span class="text-yellow-500">{{ '⭐'.repeat(review.rating) }}</span>
            </div>
            <p class="text-gray-700 dark:text-gray-300 mt-1">{{ review.comment }}</p>
          </div>
        </div>
        <p v-else class="text-gray-500 italic">Zatím žádné recenze.</p>
        
        <!-- Odkaz na přidání recenze (zjednodušeně) -->
        <div v-if="authStore.isLoggedIn" class="mt-4">
           <!-- Formular na recenzi by zde byl stejny jako u filmu -->
           <p class="text-sm text-blue-600 cursor-pointer hover:underline" @click="scrollToReviews">Napsat recenzi (viz sekce filmu)</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useApi } from '../../composables/useApi';
import { useAuthStore } from '../../stores/auth';
import { useToast } from '../../composables/useToast';
import AvgRating from '../../components/AvgRating.vue';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const toast = useToast();
const { getMovieById, getWatchlist, addToWatchlist, removeFromWatchlist } = useApi();

const seriesId = route.params.id;
const series = ref(null);
const loading = ref(true);
const error = ref(null);
const selectedSeasonIndex = ref(0);

const watchlist = ref([]);
const isProcessingWatchlist = ref(false);

const currentSeason = computed(() => {
  if (!series.value || !series.value.seasons || series.value.seasons.length === 0) return null;
  return series.value.seasons[selectedSeasonIndex.value];
});

const watchlistItem = computed(() => {
  if (!watchlist.value) return null;
  return watchlist.value.find(item => item.movie.id === Number(seriesId));
});

const fetchSeries = async () => {
  loading.value = true;
  try {
    const response = await getMovieById(seriesId);
    series.value = response.data;
    if (series.value.type !== 'series') {
        router.replace(`/movies/${seriesId}`);
    }
    
    if (authStore.isLoggedIn) {
      await fetchWatchlistData();
    }
  } catch (err) {
    console.error(err);
    error.value = err;
  } finally {
    loading.value = false;
  }
};

const fetchWatchlistData = async () => {
  try {
    const response = await getWatchlist();
    watchlist.value = response.data.results;
  } catch (err) {
    console.error(err);
  }
};

const toggleWatchlist = async () => {
  if (!authStore.isLoggedIn) {
    alert("Pro přidání do seznamu se prosím přihlašte.");
    return;
  }
  isProcessingWatchlist.value = true;
  try {
    if (watchlistItem.value) {
      await removeFromWatchlist(watchlistItem.value.id);
    } else {
      await addToWatchlist(seriesId);
    }
    await fetchWatchlistData();
  } catch (err) {
    toast.error("Chyba při aktualizaci seznamu.");
  } finally {
    isProcessingWatchlist.value = false;
  }
};

const getEpisodeImage = (episode) => {
  if (episode.still_path) return episode.still_path;
  if (currentSeason.value && currentSeason.value.poster) return currentSeason.value.poster;
  if (series.value && series.value.poster) return series.value.poster;
  return null;
};

const scrollToReviews = () => {
    // Implement scroll
};

onMounted(fetchSeries);
</script>