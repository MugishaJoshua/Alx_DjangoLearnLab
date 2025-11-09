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
#from .views import list_books
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

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "relationship_app/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("logout")
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return render(request, "relationship_app/logout.html")
