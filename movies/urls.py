from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, GenreViewSet, DirectorViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'directors', DirectorViewSet)

urlpatterns = router.urls
