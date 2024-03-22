from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget


# Add Post Form
class PostForm(forms.ModelForm):
    class Meta:
        model = Post      
        fields = ('title','description', 'image', 'status', 'tags')
        
        

# Update Form
class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'image')


# Comment Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'comment', 'active', 'author')
        

