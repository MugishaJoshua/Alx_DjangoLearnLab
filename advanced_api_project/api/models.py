from django.db import models

# The Author model represents a writer who can have multiple books.
# It stores basic information about the author and acts as the "parent" 
# in the one-to-many relationship (Author → Books).
class Author(models.Model):
    # The author's full name (string).
    name = models.CharField(max_length=255)

    def __str__(self):
        # This makes the author name display nicely in Django admin and the shell.
        return self.name


# The Book model stores information about a single book.
# It is linked to the Author model through a ForeignKey, meaning:
# One Author can have MANY Books (one-to-many relationship).
class Book(models.Model):
    # Title of the book.
    title = models.CharField(max_length=255)

    # The year the book was published (integer).
    publication_year = models.IntegerField()

    # ForeignKey establishes the relationship between Book and Author.
    # on_delete=models.CASCADE means if an author is deleted,
    # all related books will also be deleted.
    # related_name='books' allows reverse lookup: author.books.all()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        # Return the book title as the string representation.
        return self.title
