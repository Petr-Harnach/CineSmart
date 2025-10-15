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
