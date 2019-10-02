from django.db import models
from users.models import Profile
import datetime
from django.utils import timezone
from django.contrib.auth import  get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse, reverse_lazy
from topictag.models import TaggedObject, Tag
from taggit.managers import TaggableManager
from topics.models import Topic



User = get_user_model()

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    content = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    date_created = models.DateTimeField(verbose_name='date published', auto_now_add=True)

    # def get_absolute_url(self):
    #     return reverse('blog:post', kwargs={'pk': self.pk})

    def __str__(self):
        return '"{title}" by {username}'.format(title=self.title,
                                                username=self.user.username)



class PostComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(verbose_name='date published', auto_now_add=True)

    def __str__(self):
        return '"{content}..." on {post_title} by {username}'.format(content=self.content[:20],
                                                                  post_title=self.post.title,
                                                                  username=self.user.username)


# class ItemSchedule(models.Model):

class Blog(models.Model):
    name = models.CharField(max_length=255, unique = True,)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    tags = TaggableManager(through=TaggedObject)
    author = models.ForeignKey(User, related_name='blog_author_set', on_delete= models.CASCADE, null = True)
    # author = models.ManyToManyField(User,)

    blog_slug = models.SlugField(unique = True, blank=True)
    def save(self, *args, **kwargs):
        self.blog_slug = slugify(self.name)
        super(Blog, self).save(*args, **kwargs)


    def get_tag_names(self):
        return [tag.name for tag in Tag.objects.get_for_object(self)]
    def get_absolute_url(self):
        return reverse('activities:specific_blog', kwargs={'blog_slug' : self.blog_slug})
    
class BlogComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(verbose_name='date published', auto_now_add=True)

    def __str__(self):
        return '{username}: {content}'.format(content=self.content,
                                                                  username=self.author.username)
