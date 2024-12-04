from re import A
from django.forms import ModelForm
from django import forms
from .models import *


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'body', 'tags']  # Include title, image, body, and tags
        labels = {
            'body': 'Caption',
            'tags': 'Category',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter the title...', 'class': 'form-control'}),
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a caption ...', 'class': 'form-control'}),
            'image': forms.FileInput(),
            'tags': forms.CheckboxSelectMultiple(),
        }

class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'body', 'tags']  # Include title, image, body, and tags
        labels = {
            'body': 'Caption',
            'tags': 'Category',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter the title...', 'class': 'form-control'}),
            'body': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'image': forms.FileInput(),
            'tags': forms.CheckboxSelectMultiple(),
        }
class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Add comment ...'})
        }
        labels = {
            'body': ''
        }
        
class ReplyCreateForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Add reply ...', 'class' : '!text-sm'})
        }
        labels = {
            'body': ''
        }