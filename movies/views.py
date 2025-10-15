from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Movie, Genre, Director, Review
from .serializers import MovieSerializer, GenreSerializer, DirectorSerializer, ReviewSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
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
    if not old or not new:
        return Response({'detail': 'old_password and new_password required'}, status=status.HTTP_400_BAD_REQUEST)
    if not user.check_password(old):
        return Response({'detail': 'old password incorrect'}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(new)
    user.save()
    return Response({'detail': 'password changed'})




class MovieViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genres', 'director']  # filtrování podle žánru a režiséra
    search_fields = ['title', 'description']   # fulltext vyhledávání
    ordering_fields = ['release_date', 'title']  # možnost řazení

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
                    'director_id': 1,
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
    return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    return Response(UserSerializer(user).data)


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
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
