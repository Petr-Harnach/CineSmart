# CineSmart

Simple Django REST API for managing a movie catalog (genres, directors, movies).

## Quick start (development)

Prerequisites:
- Python 3.11+ and pip
- PostgreSQL (or update `DATABASES` in `cinesmart/settings.py` to use SQLite for quick tests)

Steps:

1. Create and activate a virtual environment:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create the database and update credentials in `cinesmart/settings.py`.

4. Run migrations and create a superuser:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

5. Run the development server:

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/ to see the browsable API.

## API endpoints

The `movies` app exposes these endpoints via a DRF router:

- GET /movies/ — list movies (supports filtering by `genres` and `director`, search `title`/`description`, ordering by `release_date` or `title`)
- POST /movies/ — create a movie. Use `genre_ids` (list of genre PKs) and `director_id` (PK) to link relationships.
- GET /movies/{id}/ — retrieve a movie (nested `genres` and `director` returned)
- PUT/PATCH /movies/{id}/ — update using `genre_ids` / `director_id` for relationships
- DELETE /movies/{id}/ — delete a movie

- GET /genres/ — list/create genres
- GET /genres/{id}/ — retrieve genre

- GET /directors/ — list/create directors
- GET /directors/{id}/ — retrieve director

Example POST body to create a movie:

```json
{
	"title": "My Movie",
	"description": "A fun film",
	"release_date": "2020-01-01",
	"duration_minutes": 120,
	"genre_ids": [1, 2],
	"director_id": 1
}
```

## Tests

Run tests with:

```powershell
python manage.py test
```

If you prefer to use SQLite quickly for local testing, set `DATABASES['default']['ENGINE']` to `django.db.backends.sqlite3` and update the `NAME` to `BASE_DIR / 'db.sqlite3'`.

---

# CineSmart - Maturitní Projekt

## 1. Použité technologie

### Backend
*   **Jazyk:** Python 3.11+
*   **Framework:** Django 5.2.5+
*   **API Framework:** Django REST Framework 3.14+
*   **Filtrování API:** Django Filter 23.1+
*   **Autentizace:** Django REST Framework Simple JWT 5.2.0+ (pro JWT tokeny a HttpOnly cookies)
*   **CORS:** Django CORS Headers 4.0.0+ (pro povolení komunikace mezi frontendem a backendem)
*   **Dokumentace API:** DRF Spectacular 0.27.0+ (pro automatické generování OpenAPI/Swagger dokumentace)
*   **Zpracování obrázků:** Pillow 10.0.0+ (pro nahrávání profilových obrázků a plakátů)

### Frontend
*   **Jazyk:** JavaScript (s Vue 3 Composition API)
*   **Framework:** Nuxt.js (Server-Side Rendering, struktura aplikace)
*   **Stylování:** Tailwind CSS
*   **Správa stavu:** Pinia
*   **HTTP Klient:** Axios

### Databáze
*   **Vývoj/Testování:** SQLite
*   **Produkce (plánováno):** PostgreSQL

## 2. Ukázkový kód

Zde jsou vybrané ukázky kódu demonstrující klíčové části aplikace.

### Backend - Zobrazení seznamu filmů (movies/views.py)

```python
# movies/views.py
from rest_framework import viewsets
from .models import Movie
from .serializers import MovieSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# ViewSet definuje logiku pro API endpoint.
# ModelViewSet automaticky poskytuje operace GET, POST, PUT, DELETE.
class MovieViewSet(viewsets.ModelViewSet):
    # Určuje, jaká data se mají z databáze načíst.
    queryset = Movie.objects.all()
    # Určuje, jak se mají data převést do formátu JSON.
    serializer_class = MovieSerializer
    # Nastavuje oprávnění: kdokoli může číst, jen přihlášení mohou zapisovat.
    permission_classes = [IsAuthenticatedOrReadOnly]
    # Povoluje vestavěné filtry pro vyhledávání, řazení a filtrování.
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genres', 'director']  # Pole pro filtrování.
    search_fields = ['title', 'description']   # Pole pro full-textové vyhledávání.
    ordering_fields = ['release_date', 'title'] # Pole pro řazení.
```

### Backend - Serializér filmu (movies/serializers.py)

```python
# movies/serializers.py
from rest_framework import serializers
from .models import Movie, Genre, Director

# Serializer převádí komplexní datové typy (jako modely Django)
# na nativní Python datové typy, které lze snadno převést na JSON.

class MovieSerializer(serializers.ModelSerializer):
    # Pro čtení (GET) chceme zobrazit celé informace o žánrech a režisérovi.
    genres = GenreSerializer(many=True, read_only=True)
    director = DirectorSerializer(read_only=True)
    
    # Pro zápis (POST, PUT) chceme přijímat pouze ID, ne celý objekt.
    # 'write_only=True' znamená, že se tato pole nebudou zobrazovat v odpovědi.
    # 'source' propojí toto pole s polem modelu (např. 'genre_ids' s 'genres').
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True, write_only=True, source='genres'
    )
    director_id = serializers.PrimaryKeyRelatedField(
        queryset=Director.objects.all(), write_only=True, source='director', allow_null=True
    )

    class Meta:
        model = Movie # Propojení s modelem Movie.
        # Seznam polí, která se mají zahrnout do API odpovědi.
        fields = [
            'id', 'title', 'description', 'release_date', 'duration_minutes', 'poster',
            'genres', 'genre_ids', 'director', 'director_id'
        ]
```

### Backend - Model filmu (movies/models.py)

```python
# movies/models.py
from django.db import models

# Model definuje strukturu dat v databázi.
# Každá třída je tabulka, každý atribut je sloupec.

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name

class Director(models.Model):
    name = models.CharField(max_length=150, unique=True)
    def __str__(self): return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration_minutes = models.IntegerField()
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    
    # Vztah Many-to-Many: jeden film může mít více žánrů a jeden žánr více filmů.
    genres = models.ManyToManyField(Genre, related_name="movies")
    
    # Vztah Foreign Key (Many-to-One): jeden režisér může mít více filmů.
    # on_delete=models.SET_NULL znamená, že pokud smažeme režiséra, filmy zůstanou.
    director = models.ForeignKey(
        "Director", on_delete=models.SET_NULL, null=True, blank=True, related_name="movies"
    )
    
    def __str__(self): return self.title
```

### Frontend - API služba (frontend/composables/useApi.js)

```javascript
// frontend/composables/useApi.js
import axios from 'axios';
import { useAuthStore } from '../stores/auth'; // Import pro přístup k tokenu

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // Adresa našeho Django API
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor pro automatické přidání JWT tokenu do hlavičky
apiClient.interceptors.request.use(config => {
  const authStore = useAuthStore();
  const token = authStore.accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

export const useApi = () => {
  const getMovies = () => apiClient.get('movies/'); // Funkce pro získání seznamu filmů
  const getMovieById = (id) => apiClient.get(`movies/${id}/`); // Funkce pro získání detailu filmu
  const login = (credentials) => apiClient.post('auth/login/', credentials); // Přihlášení
  const register = (userData) => apiClient.post('auth/register/', userData); // Registrace
  const getProfile = () => apiClient.get('auth/profile/'); // Získání profilu uživatele

  return {
    getMovies,
    getMovieById,
    login,
    register,
    getProfile,
  };
};
```

### Frontend - Zobrazení seznamu filmů (frontend/components/PageHome.vue)

```vue
<!-- frontend/components/PageHome.vue -->
<template>
  <div>
    <h1 class="text-3xl font-bold mb-6 text-gray-800">Featured Movies</h1>
    
    <div v-if="loading" class="text-center text-gray-500">
      <p>Loading movies...</p>
    </div>
    
    <div v-else-if="error" class="text-center text-red-500">
      <p>Failed to load movies: {{ error.message }}</p>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div 
        v-for="movie in movies" 
        :key="movie.id" 
        class="bg-white rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer"
        @click="showMovieDetail(movie.id)"
      >
        <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" class="h-64 w-full object-cover">
        <div v-else class="bg-gray-300 h-64 w-full"></div>
        
        <div class="p-4">
          <h2 class="text-lg font-semibold text-gray-900 truncate">{{ movie.title }}</h2>
          <p class="text-gray-600 text-sm mt-1">{{ movie.release_date }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useApi } from '../composables/useApi'; // Manuální import useApi

const emit = defineEmits(['show-detail']); // Emit události pro zobrazení detailu

const { getMovies } = useApi(); // Použití API služby
const movies = ref([]);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const response = await getMovies();
    movies.value = response.data.results; // Získání dat z paginované odpovědi
  } catch (err) {
    error.value = err;
    console.error('Error fetching movies:', err);
  } finally {
    loading.value = false;
  }
});

const showMovieDetail = (movieId) => {
  emit('show-detail', movieId); // Emit události s ID filmu
};
</script>
```