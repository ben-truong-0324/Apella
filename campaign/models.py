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


class Campaign(models.Model): 
    name = models.CharField(max_length= 255)
    summary = models.TextField()
    author = models.ManyToManyField(User, related_name='campaigns')
    created_date = models.DateTimeField('date started', auto_now_add=True)
    def __str__(self):
        return self.name

    active = models.BooleanField(default=True)
    def is_active(self):
        return self.active
    def is_resolved(self):
        return not self.active

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name="campaigns", null = True, blank = True)

    # tags = TaggableManager(verbose_name="Tags", help_text="Tags of topic", through=None, blank=False)
    tags = TaggableManager(through=TaggedObject)

    def get_tag_names(self):
        return [tag.name for tag in Tag.objects.get_for_object(self)]

    campaign_slug = models.SlugField(max_length=250, unique=True)

    def save(self, *args, **kwargs):
        self.campaign_slug = slugify(self.name)
        super(Campaign, self).save(*args, **kwargs)
    # def get_absolute_url(self):
    #    return reverse('campaign:specific_campaign', kwargs={'campaign_slug' : self.campaign_slug})

    def get_absolute_url_mod(self):
       return reverse('organizations:org_campaigns:campaign', kwargs={'campaign_slug' : self.campaign_slug, 'org_slug' : self.organization.org_slug})

class Share(models.Model):
    author = models.ForeignKey(User, 
    related_name='shares', 
    on_delete=models.CASCADE,
    )
    campaign = models.ForeignKey(Campaign,
    related_name='shares',
    on_delete=models.CASCADE,
    )
    text = models.TextField()
    date_created = models.DateTimeField(verbose_name='date published', auto_now_add=True)
    def __str__(self):
        return str(self.text)