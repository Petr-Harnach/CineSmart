from django.test import TestCase
from rest_framework.test import APIClient
from .models import Genre, Director, Movie, Review
from django.contrib.auth import get_user_model


class MovieAPITest(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.genre1 = Genre.objects.create(name='Action')
		self.genre2 = Genre.objects.create(name='Comedy')
		self.director = Director.objects.create(name='Jane Doe')
		# Create a user for authentication
		User = get_user_model()
		self.user = User.objects.create_user(username='testuser', password='testpassword')

	def test_create_movie_unauthenticated(self):
		"""Verify that unauthenticated users cannot create movies."""
		data = {'title': 'Forbidden Movie'}
		resp = self.client.post('/api/movies/', data, format='json')
		self.assertIn(resp.status_code, [401, 403])

	def test_create_and_get_movie(self):
		# Authenticate the client
		self.client.login(username='testuser', password='testpassword')

		data = {
			'title': 'Test Movie',
			'description': 'A test',
			'release_date': '2020-01-01',
			'duration_minutes': 90,
			'genre_ids': [self.genre1.id, self.genre2.id],
			'director_id': self.director.id,
		}
		resp = self.client.post('/api/movies/', data, format='json')
		self.assertEqual(resp.status_code, 201, resp.data)
		movie_id = resp.data['id']

		# retrieve (should not require auth)
		self.client.logout()
		resp2 = self.client.get(f'/api/movies/{movie_id}/')
		self.assertEqual(resp2.status_code, 200)
		self.assertEqual(resp2.data['title'], 'Test Movie')
		self.assertIn('genres', resp2.data)
		self.assertIn('director', resp2.data)


class AuthTest(TestCase):
	def setUp(self):
		self.client = APIClient()

	def test_register_and_profile(self):
		# register
		resp = self.client.post('/api/auth/register/', {'username': 'u1', 'password': 'pass12345', 'email': 'a@b.com'}, format='json')
		self.assertEqual(resp.status_code, 201)

		# obtain tokens
		token_resp = self.client.post('/api/token/', {'username': 'u1', 'password': 'pass12345'}, format='json')
		self.assertEqual(token_resp.status_code, 200)
		access = token_resp.data['access']

		# access profile
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
		prof = self.client.get('/api/auth/profile/')
		self.assertEqual(prof.status_code, 200)
		self.assertEqual(prof.data['username'], 'u1')

	def test_update_profile(self):
		"""Test that a user can update their own bio."""
		# register and login
		self.client.post('/api/auth/register/', {'username': 'u3', 'password': 'pass34567', 'email': 'c@b.com'}, format='json')
		token_resp = self.client.post('/api/token/', {'username': 'u3', 'password': 'pass34567'}, format='json')
		access = token_resp.data['access']
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

		# update bio
		update_data = {'bio': 'This is my new bio.'}
		resp = self.client.patch('/api/auth/profile/', update_data, format='json')
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.data['bio'], 'This is my new bio.')

	def test_login_sets_cookie_and_change_password(self):
		# register
		resp = self.client.post('/api/auth/register/', {'username': 'u2', 'password': 'pass23456', 'email': 'b@b.com'}, format='json')
		self.assertEqual(resp.status_code, 201)

		# login
		login = self.client.post('/api/auth/login/', {'username': 'u2', 'password': 'pass23456'}, format='json')
		self.assertEqual(login.status_code, 200)
		# cookie should be set
		self.assertIn('refresh_token', login.client.cookies)

		# change password
		access = login.data['access']
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
		ch = self.client.post('/api/auth/change-password/', {'old_password': 'pass23456', 'new_password': 'newpass123'}, format='json')
		self.assertEqual(ch.status_code, 200)

	def test_watchlist_crud(self):
		# create movie and user
		g = Genre.objects.create(name='Drama')
		d = Director.objects.create(name='D')
		m = Movie.objects.create(title='WL Movie', description='x', release_date='2020-01-01', duration_minutes=90, director=d)
		m.genres.add(g)

		resp = self.client.post('/api/auth/register/', {'username': 'wuser', 'password': 'pass7890', 'email': 'w@w.com'}, format='json')
		self.assertEqual(resp.status_code, 201)
		token_resp = self.client.post('/api/token/', {'username': 'wuser', 'password': 'pass7890'}, format='json')
		access = token_resp.data['access']
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

		# add to watchlist
		add = self.client.post('/api/watchlist/', {'movie_id': m.id}, format='json')
		self.assertEqual(add.status_code, 201)
		wid = add.data['id']

		# list
		lst = self.client.get('/api/watchlist/')
		self.assertEqual(lst.status_code, 200)
		# support both paginated and non-paginated responses
		if isinstance(lst.data, dict) and 'results' in lst.data:
			items = lst.data['results']
		else:
			items = lst.data
		self.assertEqual(len(items), 1)

		# delete
		rem = self.client.delete(f'/api/watchlist/{wid}/')
		self.assertIn(rem.status_code, (204, 200))


class ReviewAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')

        self.movie = Movie.objects.create(
            title='Reviewable Movie', 
            description='desc', 
            release_date='2021-01-01', 
            duration_minutes=100
        )

    def test_create_review(self):
        self.client.login(username='user1', password='pass1')
        data = {'movie_id': self.movie.id, 'rating': 5, 'comment': 'Great movie!'}
        resp = self.client.post('/api/reviews/', data, format='json')
        self.assertEqual(resp.status_code, 201, resp.data)
        self.assertEqual(resp.data['rating'], 5)

    def test_create_review_unauthenticated(self):
        data = {'movie_id': self.movie.id, 'rating': 5, 'comment': 'Trying to comment'}
        resp = self.client.post('/api/reviews/', data, format='json')
        self.assertIn(resp.status_code, [401, 403])

    def test_create_review_duplicate(self):
        self.client.login(username='user1', password='pass1')
        data = {'movie_id': self.movie.id, 'rating': 5, 'comment': 'First review'}
        resp1 = self.client.post('/api/reviews/', data, format='json')
        self.assertEqual(resp1.status_code, 201)

        # Try to create a second review for the same movie
        data2 = {'movie_id': self.movie.id, 'rating': 3, 'comment': 'Second attempt'}
        resp2 = self.client.post('/api/reviews/', data2, format='json')
        self.assertEqual(resp2.status_code, 400) # Bad Request

    def test_update_own_review(self):
        self.client.login(username='user1', password='pass1')
        review = Review.objects.create(user=self.user1, movie=self.movie, rating=4, comment='Initial comment')
        
        update_data = {'rating': 5, 'comment': 'Updated comment'}
        resp = self.client.patch(f'/api/reviews/{review.id}/', update_data, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['comment'], 'Updated comment')

    def test_update_other_users_review(self):
        # user1 creates a review
        review = Review.objects.create(user=self.user1, movie=self.movie, rating=4)
        
        # user2 tries to update it
        self.client.login(username='user2', password='pass2')
        update_data = {'rating': 1}
        resp = self.client.patch(f'/api/reviews/{review.id}/', update_data, format='json')
        self.assertEqual(resp.status_code, 403) # Forbidden

    def test_delete_own_review(self):
        self.client.login(username='user1', password='pass1')
        review = Review.objects.create(user=self.user1, movie=self.movie, rating=4)
        resp = self.client.delete(f'/api/reviews/{review.id}/')
        self.assertEqual(resp.status_code, 204) # No Content

    def test_delete_other_users_review(self):
        review = Review.objects.create(user=self.user1, movie=self.movie, rating=4)
        self.client.login(username='user2', password='pass2')
        resp = self.client.delete(f'/api/reviews/{review.id}/')
        self.assertEqual(resp.status_code, 403) # Forbidden
