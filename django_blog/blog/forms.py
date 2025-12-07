from django import forms
from .models import Post
from .models import Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import  Tag

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Write your post...'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError("Title must not be empty.")
        return title

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
        # Optional: enforce length limits
        if len(content) > 2000:
            raise forms.ValidationError('Comment too long (max 2000 characters).')
        return content


class PostForm(forms.ModelForm):
    # input for comma separated tags
    tag_field = forms.CharField(
        required=False,
        help_text="Add tags separated by commas. Example: python,django,aws"
    )

    class Meta:
        model = Post
        fields = ['title', 'content']  # add other fields you already use

    def __init__(self, *args, **kwargs):
        # if instance exists, populate tag_field with existing tags
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            tags_qs = self.instance.tags.all()
            self.fields['tag_field'].initial = ','.join([t.name for t in tags_qs])

    def clean_tag_field(self):
        val = self.cleaned_data.get('tag_field', '')
        # split, strip, unique, remove empty
        tags = [t.strip() for t in val.split(',') if t.strip()]
        # lowercase or keep as is — pick one consistent format:
        return list(dict.fromkeys(tags))  # preserves order, unique