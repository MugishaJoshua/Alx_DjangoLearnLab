from django.db import models
from django.contrib.auth.models import User


class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    published_date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title


class library(models.Model):
    name = models.CharField(max_length=100)
    librarian = models.OneToOneField(Librarian, on_delete=models.CASCADE, null=True, blank=True)
    books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name
