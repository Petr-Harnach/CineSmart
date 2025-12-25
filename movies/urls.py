from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
	MovieViewSet, GenreViewSet, DirectorViewSet, ActorViewSet, register_view, ProfileView,
	CookieTokenObtainPairView, CookieTokenRefreshView, token_logout_view, change_password_view,
	WatchlistViewSet, ReviewViewSet,
)

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'directors', DirectorViewSet)
router.register(r'actors', ActorViewSet)
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = router.urls

urlpatterns += [
	# authentication helpers
	path('auth/register/', register_view, name='auth-register'),
	path('auth/profile/', ProfileView.as_view(), name='auth-profile'),
	path('auth/login/', CookieTokenObtainPairView.as_view(), name='auth-login'),
	path('auth/refresh/', CookieTokenRefreshView.as_view(), name='auth-refresh'),
	path('auth/logout/', token_logout_view, name='auth-logout'),
	path('auth/change-password/', change_password_view, name='auth-change-password'),
]
