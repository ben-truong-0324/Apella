# accounts.forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate
# from .models import Topic, ExplorePost
from dal import autocomplete
from organizations.models import Organization
from .models import Post, Blog, BlogComment

class PostStoryForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('content', 'name',)
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Your POV on the matter'}),
        }

    def save(self, commit=True):
        post = super(PostStoryForm, self).save(commit=False)
        if commit:
            post.save()
        return post


class BlogAddTagForm(forms.Form):
    tag = forms.CharField(label='Tag', max_length=100)

class CreateBlogForm(forms.ModelForm):
    class Meta: 
        model = Blog
        fields = ('name',
                    'content',
                 )
        exclude = ('author',
                   )
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Content of your blog'}),
        }

class CommentBlogForm(forms.ModelForm):
    def __init__(self, **kwargs):
        self.user = kwargs.pop('user', None)
        self.blog = kwargs.pop('blog', None)
        super(CommentBlogForm, self).__init__(**kwargs)

    class Meta:
        model = BlogComment
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Your comment', 'class':'special',}),
        }
    def save(self, commit=True):
        blogcomment = super(CommentBlogForm, self).save(commit=False)
        blogcomment.author = self.user
        blogcomment.blog = self.blog
        if commit:
            blogcomment.save()
        return blogcomment
    