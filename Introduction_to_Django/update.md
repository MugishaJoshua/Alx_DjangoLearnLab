# update.md

```python
from bookshelf.models import Book

# Update the book title
book = Book.objects.get(author="George Orwell")
book.title = "Nineteen Eighty-Four"
book.save()

# Verify update
Book.objects.all()
# Expected Output:
# <QuerySet [<Book: Nineteen Eighty-Four by George Orwell (1949)>]>
