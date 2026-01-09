from .models import Post
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add title'}),
            'body': forms.Textarea(attrs={'class': 'form-control','placeholder': "Add content"})
        }