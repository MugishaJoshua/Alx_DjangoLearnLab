from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Book
from .views import list_books
from .models import Library

# Function-based view: List all books
def list_books(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view: display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name  =  'relationship_app/library_detail.html'
    context_object_name = 'library'

from django.shortcuts import render
from .models import Book  # ✅ Import your Book model


def list_books(request):
    books = Book.objects.all()  # ✅ Fetch all books from the database
    return render(request, 'relationship_app/list_books.html', {'books': books})
