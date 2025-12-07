# blog/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post
from .models import Tag


User = get_user_model()

class PostCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='author', password='pass')
        self.other = User.objects.create_user(username='other', password='pass')
        self.post = Post.objects.create(title='Test', content='Content', author=self.user)

    def test_list_view(self):
        resp = self.client.get(reverse('blog:post-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.post.title)

    def test_detail_view(self):
        resp = self.client.get(reverse('blog:post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.post.content)

    def test_create_requires_login(self):
        resp = self.client.get(reverse('blog:post-create'))
        self.assertNotEqual(resp.status_code, 200)
        self.client.login(username='author', password='pass')
        resp = self.client.get(reverse('blog:post-create'))
        self.assertEqual(resp.status_code, 200)

    def test_update_only_author(self):
        update_url = reverse('blog:post-update', kwargs={'pk': self.post.pk})
        self.client.login(username='other', password='pass')
        resp = self.client.get(update_url)
        self.assertNotEqual(resp.status_code, 200)
        self.client.login(username='author', password='pass')
        resp = self.client.get(update_url)
        self.assertEqual(resp.status_code, 200)

    def test_delete_only_author(self):
        delete_url = reverse('blog:post-delete', kwargs={'pk': self.post.pk})
        self.client.login(username='other', password='pass')
        resp = self.client.get(delete_url)
        self.assertNotEqual(resp.status_code, 200)
        self.client.login(username='author', password='pass')
        resp = self.client.post(delete_url)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='author', password='pass')
        self.other = User.objects.create_user(username='other', password='pass')
        self.post = Post.objects.create(title='Test', content='Content', author=self.user)
        self.comment = Comment.objects.create(post=self.post, author=self.user, content='Nice post')

    def test_comment_list_shown_on_post_detail(self):
        resp = self.client.get(reverse('blog:post-detail', kwargs={'pk': self.post.pk}))
        self.assertContains(resp, self.comment.content)

    def test_create_comment_requires_login(self):
        url = reverse('blog:comment-create', kwargs={'post_pk': self.post.pk})
        resp = self.client.post(url, {'content': 'New comment'})
        self.assertNotEqual(resp.status_code, 200)  # should redirect to login or 302
        self.client.login(username='other', password='pass')
        resp = self.client.post(url, {'content': 'New comment'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'New comment')

    def test_update_comment_only_author(self):
        update_url = reverse('blog:comment-update', kwargs={'pk': self.comment.pk})
        self.client.login(username='other', password='pass')
        resp = self.client.get(update_url)
        self.assertNotEqual(resp.status_code, 200)
        self.client.login(username='author', password='pass')
        resp = self.client.get(update_url)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(update_url, {'content': 'Edited'}, follow=True)
        self.assertContains(resp, 'Edited')

    def test_delete_comment_only_author(self):
        delete_url = reverse('blog:comment-delete', kwargs={'pk': self.comment.pk})
        self.client.login(username='other', password='pass')
        resp = self.client.post(delete_url)
        self.assertNotEqual(resp.status_code, 200)
        self.client.login(username='author', password='pass')
        resp = self.client.post(delete_url, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, self.comment.content)


User = get_user_model()

class TagSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', password='p')
        self.p1 = Post.objects.create(author=self.user, title='Django tips', content='Django content')
        self.p2 = Post.objects.create(author=self.user, title='AWS guide', content='Cloud stuff')
        Tag.objects.create(name='django')
        t = Tag.objects.get(name='django')
        self.p1.tags.add(t)

    def test_posts_by_tag_view(self):
        resp = self.client.get(reverse('posts_by_tag', kwargs={'tag_name': 'django'}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Django tips')
        self.assertNotContains(resp, 'AWS guide')

    def test_search_by_title(self):
        resp = self.client.get(reverse('search_posts') + '?q=aws')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'AWS guide')

    def test_search_by_tag(self):
        resp = self.client.get(reverse('search_posts') + '?q=django')
        self.assertContains(resp, 'Django tips')
