from django import forms
from .models import Author, Blog, CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    """Form for user registration with email instead of username."""
    email = forms.EmailField(
        label=_("Email Address"),
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'your.email@example.com'
        })
    )
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'Enter password'
        })
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'Confirm password'
        })
    )
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',)

class CustomAuthenticationForm(AuthenticationForm):
    """Form for user login with email instead of username."""
    username = forms.CharField(
        label=_("Email Address"),
        max_length=254,
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': 'your.email@example.com',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'
        })
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'
        })
    )

class BlogForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), empty_label='Select an author')
    
    class Meta:
        model = Blog
        fields = ['author', 'title', 'content', 'image', 'published_date']
        widgets = {
            'title': forms.TextInput(),
            'content': forms.Textarea(attrs={'rows': 8}),
            'image': forms.FileInput(),
            'published_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        field_class = (
            'mt-1 block w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 '
            'text-slate-900 shadow-sm transition placeholder:text-slate-400 '
            'focus:border-amber-500 focus:outline-none focus:ring-4 focus:ring-amber-500/20'
        )
        select_class = field_class + ' appearance-none'

        for field_name, field in self.fields.items():
            existing_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_class} {field_class}'.strip()

        self.fields['author'].widget.attrs['class'] = select_class
        self.fields['content'].widget.attrs['rows'] = 8