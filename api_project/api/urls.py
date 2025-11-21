from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookViewSet

# Router for BookViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('auth-token/', obtain_auth_token, name='api_token_auth'),  # <- token endpoint
    path('', include(router.urls)),  # existing router
]
