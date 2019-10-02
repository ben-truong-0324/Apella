
# Create your models here.
from django.db import models
# Create your models here.
import uuid
from django.contrib.auth import  get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse, reverse_lazy
from organizations.models import Organization
from users.models import Profile
import datetime
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from topictag.models import TaggedObject, Tag
from taggit.managers import TaggableManager


User = get_user_model()
#
# class TopicTag(TagBase): #custom taggist model
#     name = models.CharField(max_length=255, blank= True)
#     summary = models.TextField(verbose_name="Description of topic",)
#     f_tagged = models.IntegerField(default=0) #to events
#     f_picked = models.IntegerField(default=0)# to users
#     f_talked = models.IntegerField(default=0) #to conversations/posts
#
# class EventTopic(GenericTaggedItemBase):
#     tag = models.ForeignKey(TopicTag,
#                             #related_name="",



class Topic(models.Model): #rename this it event/tracking later
    name = models.CharField(max_length= 255)
    summary = models.TextField()
    created_date = models.DateTimeField('date started', auto_now_add=True)

    def __str__(self):
        return self.name
    active = models.BooleanField(default=False)
    def is_active(self):
        return self.active
    #change active to current = models. and resolved = models.Boo in the future

    decision_makers = models.ManyToManyField(User, related_name='+')
    constituent = models.ManyToManyField(User, related_name='+')

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     #limit_choices_to={'confirmed_identity': True},
                                     related_name="organization_topics", null = True, blank = True)

    # tags = TaggableManager(verbose_name="Tags", help_text="Tags of topic", through=None, blank=False)
    tags = TaggableManager(through=TaggedObject)

    def get_tag_names(self):
        return [tag.name for tag in Tag.objects.get_for_object(self)]

    topic_slug = models.SlugField(max_length=250, unique=True)

    def save(self, *args, **kwargs):
        self.topic_slug = slugify(self.name)
        super(Topic, self).save(*args, **kwargs)
    def get_absolute_url(self):
       return reverse('topics:specific_topic', kwargs={'topic_slug' : self.topic_slug})

    def get_absolute_url_mod(self):
       return reverse('organizations:specific_org_topics:org_topic', kwargs={'topic_slug' : self.topic_slug, 'org_slug' : self.organization.org_slug})



#each explore posts will be interactable like tinder cards: like, unlike, or favorited
class ExplorePost(models.Model):
    content = models.TextField(blank=True, verbose_name="Explore Post")
    def __str__(self):
        return self.content
    created_date = models.DateTimeField('date posted', auto_now_add=True)
    
    favorite = models.BooleanField(verbose_name ="User favorited", default=False)
    liked = models.BooleanField(verbose_name="Negative sentiment", default=False)
    unliked = models.BooleanField(verbose_name="Negative sentiment", default=False)
    def is_favorite(self):
        return self.favorite
    def is_liked(self):
        return self.liked
    def is_unliked(self):
        return self.unliked

    topic = models.ForeignKey(Topic, on_delete = models.CASCADE,
                                related_name="topic_explore_posts", null = True, blank = True,
                                )
    user = models.ForeignKey(User, related_name="user_explore_posts", on_delete=models.CASCADE, 
                                blank = True, null = True,
                                )
    # organization = models.ForeignKey(Organization, related_name="org_explore_posts",
    #                             on_delete=models.CASCADE, null = True, blank = True,
    #                             )

class UserPost(models.Model):
    user_profile = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, null = True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(verbose_name="Post content",blank = True, null = True,)
    posted_on = models.DateTimeField(default=timezone.now)

    def get_number_of_comments(self):
        return self.comment_set.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(UserPost, null = True, blank = True, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE,)
    comment = models.CharField(max_length=144)
    posted_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment







