from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# ------------------------------
# Author Model
# ------------------------------
class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


# ------------------------------
# Librarian Model
# ------------------------------
class Librarian(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


# ------------------------------
# Book Model
# ------------------------------
class Book(models.Model):
    title = models.CharField(max_length=200)
    published_date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    library = models.ForeignKey('Library', on_delete=models.CASCADE, related_name='library_books', null=True,  blank=True)
    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]


# ------------------------------
# Library Model
# ------------------------------
class Library(models.Model):
    name = models.CharField(max_length=100)
    librarian = models.OneToOneField(Librarian, on_delete=models.CASCADE, null=True, blank=True)
    books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name


# ------------------------------
# Profile Model
# ------------------------------
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


# ------------------------------
# UserProfile Model
# ------------------------------
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# ------------------------------
# Signals
# ------------------------------
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
