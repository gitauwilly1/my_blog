from django import forms
from .models import Author, Blog

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