from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from .models import Book, Library
from .forms import RegisterForm


# -------------------------
# USER SIGNUP VIEW (Class-based)
# -------------------------
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


# -------------------------
# BOOK LIST VIEW (Function-based)
# -------------------------
def list_books(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# -------------------------
# LIBRARY DETAIL VIEW (Class-based)
# -------------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# -------------------------
# REGISTER VIEW (Function-based, uses UserCreationForm)
# -------------------------
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# -------------------------
# CUSTOM REGISTER VIEW (if using custom form)
# -------------------------
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


# -------------------------
# LOGIN VIEW
# -------------------------
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


# -------------------------
# LOGOUT VIEW
# -------------------------
def logout_view(request):
    logout(request)
    return render(request, "relationship_app/logout.html")
