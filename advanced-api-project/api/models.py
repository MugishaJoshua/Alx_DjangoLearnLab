from django.db import models

# Author model represents a writer
class Author(models.Model):
    # Author's full name
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Book model represents a book written by an author
class Book(models.Model):
    # Title of the book
    title = models.CharField(max_length=255)

    # Year of publication
    publication_year = models.IntegerField()

    # Link to the Author model (one-to-many relationship)
    # related_name='books' allows reverse access: author.books.all()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title
