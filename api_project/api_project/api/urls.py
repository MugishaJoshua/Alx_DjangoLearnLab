from django.urls import path, include
from .views import BookList
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Include the old BookList view
    path('books/', BookList.as_view(), name='book-list'),

    # Include the router for BookViewSet
    path('', include(router.urls)),
]
