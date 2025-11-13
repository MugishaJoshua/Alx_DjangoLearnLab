# CRUD Operations for Book Model

This file documents all CRUD operations performed on the `Book` model in the Django shell.

---

## 1. Create Operation

```python
from bookshelf.models import Book

# Create a Book instance
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()

# Verify creation
Book.objects.all()
# Expected Output:
# <QuerySet [<Book: 1984 by George Orwell (1949)>]>

# Retrieve the book
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)
# Expected Output:
# 1984 George Orwell 1949

# Update the book title
book.title = "Nineteen Eighty-Four"
book.save()

# Verify update
Book.objects.all()
# Expected Output:
# <QuerySet [<Book: Nineteen Eighty-Four by George Orwell (1949)>]>

# Delete the book
book.delete()
# Verify deletion
Book.objects.all()
# Expected Output:
# <QuerySet []>
