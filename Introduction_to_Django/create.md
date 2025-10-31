# create.md

```python
from bookshelf.models import Book

book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()

Book.objects.all()
# Expected Output:
# <QuerySet [<Book: 1984 by George Orwell (1949)>]>
