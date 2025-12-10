from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


# ✅ ONLY ONE PostForm — with tag_field & NO 'published'
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Taggit field included here
    class Meta:
        model = Post
        fields = ['title', 'content']  # No published field!

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            tags_qs = self.instance.tags.all()
            self.fields['tag_field'].initial = ",".join([t.name for t in tags_qs])

    def clean_tag_field(self):
        val = self.cleaned_data.get('tag_field', '')
        tags = [t.strip() for t in val.split(',') if t.strip()]
        return list(dict.fromkeys(tags))  # unique and order preserved


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add a public comment...'
            }),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError('Comment cannot be empty.')
        if len(content) > 2000:
            raise forms.ValidationError('Comment too long (max 2000 characters).')
        return content
