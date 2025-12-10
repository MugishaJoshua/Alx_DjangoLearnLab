from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm,  ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .models import Comment
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import  Tag
from django.core.paginator import Paginator

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log user in immediately
            return redirect('profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'blog/profile.html')


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'blog/profile.html', {'form': form})

# blog/views.py
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def form_valid(self, form):
        form.instance.author = self.get_object().author
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        # Expecting post_pk in URL to link the comment to a Post
        self.post = get_object_or_404(Post, pk=kwargs.get('post_pk'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)

    # after create redirect to the post detail (get_absolute_url on Comment does that)
    def get_success_url(self):
        return self.object.get_absolute_url()

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        # redirect back to the associated post detail page
        return reverse_lazy('blog:post-detail', kwargs={'pk': self.object.post.pk})


# ============================
# FUNCTION-BASED VIEWS (TAGS)
# ============================

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            tags = form.cleaned_data.get('tag_field', [])
            _attach_tags_to_post(post, tags)

            return redirect(post.get_absolute_url())
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()

            tags = form.cleaned_data.get('tag_field', [])
            post.tags.clear()
            _attach_tags_to_post(post, tags)

            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {'form': form, 'post': post})


def _attach_tags_to_post(post, tags_list):
    """Attach tags to a post, creating new ones if needed."""
    for tname in tags_list:
        tag_obj, created = Tag.objects.get_or_create(name=tname)
        post.tags.add(tag_obj)


def search_posts(request):
    query = request.GET.get('q', '').strip()
    results = Post.objects.none()
    if query:
        # search in title, content, and tag name
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-created_at')

    # paginate
    paginator = Paginator(results, 10)
    page = request.GET.get('page')
    posts_page = paginator.get_page(page)

    return render(request, 'blog/search_results.html', {'query': query, 'posts': posts_page})

def posts_by_tag(request, tag_name):
    # exact match on tag name
    tag = get_object_or_404(Tag, name=tag_name)
    posts = tag.posts.all().order_by('-created_at')  # related_name='posts'
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts_page = paginator.get_page(page)
    return render(request, 'blog/posts_by_tag.html', {'tag': tag, 'posts': posts_page})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        return self.request.user == self.get_object().author
