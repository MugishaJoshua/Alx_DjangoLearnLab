from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # make sure this is the correct path
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Fields to display in the admin list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff')
    
    # Fields to use for searching
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Field sets for the user detail page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Field sets for creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'date_of_birth', 'profile_photo'),
        }),
    )
