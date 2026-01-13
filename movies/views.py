from rest_framework import viewsets, filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Movie, Genre, Director, Review, Actor, CustomUser, Collection, CollectionItem, Season, Episode
from .serializers import (
    MovieSerializer, MovieDetailSerializer, GenreSerializer, DirectorSerializer, ReviewSerializer, ActorSerializer,
    MyProfileSerializer, PublicUserSerializer, CollectionSerializer, CollectionItemSerializer
)
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from .filters import MovieFilter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from datetime import timedelta
from django.conf import settings


class CookieTokenObtainPairView(TokenObtainPairView):
    """Extends TokenObtainPairView to set refresh token in an HttpOnly cookie."""
    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        # If refresh token provided, set it as HttpOnly cookie
        refresh = resp.data.get('refresh')
        if refresh:
            # cookie lifetime from settings SIMPLE_JWT REFRESH_TOKEN_LIFETIME
            lifetime = getattr(settings, 'SIMPLE_JWT', {}).get('REFRESH_TOKEN_LIFETIME', timedelta(days=1))
            max_age = int(lifetime.total_seconds())
            resp.set_cookie(
                'refresh_token',
                refresh,
                max_age=max_age,
                httponly=True,
                samesite='Lax',
                secure=False,
            )
        return resp


class CookieTokenRefreshView(TokenRefreshView):
    """Extends TokenRefreshView to update refresh cookie when rotating tokens."""
    def post(self, request, *args, **kwargs):
        # If client did not send refresh in body, attempt to read it from HttpOnly cookie
        data = request.data if request.data else {}
        if 'refresh' not in data:
            cookie_refresh = request.COOKIES.get('refresh_token')
            if cookie_refresh:
                serializer = TokenRefreshSerializer(data={'refresh': cookie_refresh})
            else:
                # fallback to default behaviour (will raise error)
                return super().post(request, *args, **kwargs)
        else:
            serializer = TokenRefreshSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        # Build response similar to TokenRefreshView
        resp = Response(validated, status=status.HTTP_200_OK)

        # If serializer returned a new refresh token (rotation), update cookie
        refresh = validated.get('refresh')
        if refresh:
            lifetime = getattr(settings, 'SIMPLE_JWT', {}).get('REFRESH_TOKEN_LIFETIME', timedelta(days=1))
            max_age = int(lifetime.total_seconds())
            resp.set_cookie('refresh_token', refresh, max_age=max_age, httponly=True, samesite='Lax', secure=False)

        return resp


@api_view(['POST'])
def token_logout_view(request):
    resp = Response({'detail': 'logout'}, status=status.HTTP_200_OK)
    resp.delete_cookie('refresh_token')
    return resp


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    user = request.user
    old = request.data.get('old_password')
    new = request.data.get('new_password')
    
    print(f"DEBUG: Change password for user: {user.username}")
    print(f"DEBUG: Old password provided: {old}")
    
    if not old or not new:
        return Response({'detail': 'old_password and new_password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    is_valid = user.check_password(old)
    print(f"DEBUG: Password check result: {is_valid}")

    if not is_valid:
        return Response({'detail': 'old password incorrect'}, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new)
    user.save()
    return Response({'detail': 'password changed'})


class ProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve or update the authenticated user's profile."""
    serializer_class = MyProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


from django.db.models import Avg, F, Count
from django.db.models.functions import Lower

class MovieViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Movie.objects.all()
    # serializer_class is handled by get_serializer_class
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MovieFilter
    search_fields = ['title'] 
    ordering_fields = ['release_date', 'title', 'avg_rating', '?'] 

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieSerializer

    def get_queryset(self):
        queryset = Movie.objects.annotate(avg_rating=Avg('reviews__rating'))
        ordering = self.request.query_params.get('ordering')

        if ordering in ['title', '-title']:
            # Apply case-insensitive ordering for the 'title' field
            if ordering.startswith('-'):
                return queryset.annotate(title_lower=Lower('title')).order_by('-title_lower')
            return queryset.annotate(title_lower=Lower('title')).order_by('title_lower')
        
        if ordering == 'avg_rating':
            return queryset.order_by(F('avg_rating').asc(nulls_last=True))
        
        if ordering == '-avg_rating':
            return queryset.order_by(F('avg_rating').desc(nulls_last=True))
            
        return queryset

    @extend_schema(
        request=MovieSerializer,
        examples=[
            OpenApiExample(
                'Create movie example',
                value={
                    'title': 'Example Movie',
                    'description': 'A short description',
                    'release_date': '2020-01-01',
                    'duration_minutes': 100,
                    'genre_ids': [1],
                    'director_ids': [1],
                },
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


@api_view(['POST'])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response(MyProfileSerializer(user).data, status=status.HTTP_201_CREATED)


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class DirectorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ActorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class WatchlistViewSet(viewsets.ModelViewSet):
    """Watchlist items for authenticated users."""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        WatchlistItem = __import__('django').apps.apps.get_model('movies', 'WatchlistItem')
        return WatchlistItem.objects.filter(user=self.request.user).select_related('movie')

    def list(self, request, *args, **kwargs):
        """Return only the requesting user's watchlist items."""
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        from .serializers import WatchlistItemSerializer
        return WatchlistItemSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['movie']
    ordering_fields = ['created_at', 'likes_count']

    def get_queryset(self):
        return Review.objects.annotate(likes_count=Count('likes'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        review = self.get_object()
        user = request.user
        ReviewLike = __import__('django').apps.apps.get_model('movies', 'ReviewLike')

        try:
            like = ReviewLike.objects.get(review=review, user=user)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReviewLike.DoesNotExist:
            ReviewLike.objects.create(review=review, user=user)
            return Response(status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """A viewset for viewing user profiles."""
    queryset = CustomUser.objects.all()
    serializer_class = PublicUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        from django.db.models import Q
        user = self.request.user
        if user.is_authenticated:
            # Veřejné kolekce + vlastní kolekce uživatele
            return Collection.objects.filter(Q(is_public=True) | Q(user=user)).distinct().order_by('-created_at')
        return Collection.objects.filter(is_public=True).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_movie(self, request, pk=None):
        collection = self.get_object()
        if collection.user != request.user:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        
        movie_id = request.data.get('movie_id')
        if not movie_id:
            return Response({'detail': 'movie_id required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            movie = Movie.objects.get(id=movie_id)
            CollectionItem.objects.get_or_create(collection=collection, movie=movie)
            return Response(status=status.HTTP_201_CREATED)
        except Movie.DoesNotExist:
            return Response({'detail': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_movie(self, request, pk=None):
        collection = self.get_object()
        if collection.user != request.user:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        
        movie_id = request.data.get('movie_id')
        item = CollectionItem.objects.filter(collection=collection, movie_id=movie_id).first()
        if item:
            item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)