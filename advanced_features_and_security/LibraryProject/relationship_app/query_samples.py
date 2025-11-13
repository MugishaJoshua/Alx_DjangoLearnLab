from relationship_app.models import Author, Book, library, Librarian

def get_books_by_author(author_name):
    try:
        author  = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"\n📚 Books written by {author_name}: ")
        for book in books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"\n ❌ Author '{author_name}' not found my guy.")


def list_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"\n🏛️ Books available in {library_name}: ")  
        for book in books:
            print(f"- {book.title}")
    except Library.DoesNotExist:
        print(f"\n ❌ Library '{library_name}' not found.")  

def get_librarian_for_library(library_name):
    try:
        library_instance = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library_instance)
        if librarian:
            print(f"\n👲 librarian for {librarian.name}: {librarian.user.username}")
        else:
            print(f"\n💀{library_instance.name} does not have a librarian assigned. ")
    except Library.DoesNotExist:
        print(f"\n ❌ Library '{library_name}' not found.")
    except Librarian.DoesNotExist:
        print(f"\n ❌ No librarian found for library '{library_name}'.")

if __name__ == "__main__":
    get_books_by_author("John Doe")
    list_books_in_library("City library")
    get_librarian_for_library("City Library")