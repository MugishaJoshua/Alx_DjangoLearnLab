# Create Operation

In the Django shell, we created a new `Book` record as follows:

```python
from bookshelf.models import Book

# Create a book instance
Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)
