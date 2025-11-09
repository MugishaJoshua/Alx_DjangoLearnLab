from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from . import views_roles

urlpatterns = [
    # Authentication routes
    path(
        'login/',
        LoginView.as_view(template_name='relationship_app/login.html'),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(template_name='relationship_app/logout.html'),
        name='logout'
    ),

    # Registration route (custom view)
    path('register/', views.register, name='register'),

    # Existing routes (if you already created them earlier)
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('admin-view/', views_roles.admin_view, name='admin_view'),
    path('librarian-view/', views_roles.librarian_view, name='librarian_view'),
    path('member-view/', views_roles.member_view, name='member_view'),
     path('admin-view/', views.admin_view, name='admin_view'),
]
