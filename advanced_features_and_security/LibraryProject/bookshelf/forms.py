from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    """
    A secure form for creating and updating Book instances.
    Uses Django's ModelForm to validate and sanitize user inputs.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        # Example: basic XSS protection by escaping HTML
        return forms.utils.escape(title)

    def clean_author(self):
        author = self.cleaned_data.get('author')
        return forms.utils.escape(author)

    def clean_publication_year(self):
        year = self.cleaned_data.get('publication_year')
        if year < 0:
            raise forms.ValidationError("Publication year cannot be negative.")
        return year
