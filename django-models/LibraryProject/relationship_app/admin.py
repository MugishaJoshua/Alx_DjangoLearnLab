from django.contrib import admin
from .models import Profile, Author, Book, Library

admin.site.register(Profile)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
