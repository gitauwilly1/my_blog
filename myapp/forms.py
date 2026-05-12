from django import forms
fromm .models import Author, Blog

class BlogForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), empty_label="Select Author")

    class Meta:
        model = Blog
        fields = ['title', 'author', 'content', 'published_date']
        widgets = {
            'published_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }