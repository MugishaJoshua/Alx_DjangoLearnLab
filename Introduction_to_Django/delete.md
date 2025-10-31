# delete.md

```python
from bookshelf.models import Book

# Delete the book
book = Book.objects.get(author="George Orwell")
book.delete()

# Verify deletion
Book.objects.all()
# Expected Output:
# <QuerySet []>
