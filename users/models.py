# Create your models here.
# users/models.py
from django.utils import timezone
from django.urls import reverse
from django.db import models
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Count, F
from django.db.models.expressions import Func
#includes: user authen, user profile, and user acitvities
from taggit.managers import TaggableManager
from topictag.models import Tag, TaggedObject


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email adress")
        if not password:
            raise ValueError("Users must have a password")
        if not username:
            raise ValueError("Users must have a username")

        user_obj = self.model(
            username = username,
            email = self.normalize_email(email),
            password = password
        )
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj
    def create_staffuser(self, username, email, password=None):
        user = self.create_user(
            username, email, password=password, is_staff=True
        )
        return user
    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username, email, password=password, is_staff=True, is_admin=True
        )
        return user


class User(AbstractBaseUser):
    #id, password, last_login
    username    = models.CharField(max_length = 255, unique=True)
    #demand real first and last name
    email   = models.EmailField(unique=True, max_length = 255)
    USERNAME_FIELD = 'username'
    
    timestamp = models.DateTimeField(auto_now_add=True)

    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    active  = models.BooleanField(default=True) #can login
    staff    = models.BooleanField(default=False)
    admin   = models.BooleanField(default=False) #superuser
    confirmed_email = models.BooleanField(default=False) #superuser
    confirmed_email_time = models.DateTimeField(auto_now_add=True)

    #

    #username_field and password are required by default
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True

    def get_first_name(self):
        return self.first_name

    def is_staff(self):
        return self.staff
    def is_admin(self):
        return self.admin
    def is_active(self):
        return self.active
    def is_confirmed_email(self):
        return self.confirmed_email

    def get_absolute_url(self):
        return reverse('users:index',)

    is_member = models.BooleanField(default=False)
    is_decision_maker = models.BooleanField(default=False)


    
    
    #user_slug is username

    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(default='', blank=True, null=True)
    bio = models.TextField(verbose_name="Biography", blank = True, null = True,) 
    first_name = models.CharField(max_length=255, blank = True, null = True)
    last_name = models.CharField(max_length=255, blank = True, null = True) 
    location_city = models.CharField(verbose_name="City living in", blank = True, null = True, max_length =255,)
    location_state = models.CharField(verbose_name="State living in", blank = True, null = True, max_length = 255,)
    location_country = models.CharField(verbose_name="Country living in", blank = True, null = True,max_length = 255,)
    def __str__(self):
        return self.user.username
    followers = models.ManyToManyField('Profile',
                                        related_name="followers_profile",
                                        blank=False,)
    following = models.ManyToManyField('Profile',
                                        related_name="following_profile",
                                        blank=False,)
    #add test: if following no one return empty
    def get_number_of_followers(self):
        if self.followers.count():
            return self.followers.count()
        else:
            return 0

    def get_number_of_following(self):
        if self.following.count():
            return self.following.count()
        else:
            return 0

    MEMBER_TYPE_CHOICES = (
        (0, 'observer'), #an observer can view deliberations of other orgs, open to all
        (1, 'member'), #an observer becoming a member gives them deliberative power, need to have profile and authentication.
        (2, 'decision maker'), #a member becoming a decision maker gives them representative duties
        (3, 'messenger'), #a member or a consultant can become a messenger that is a neutral party between member and decision maker
        (4, 'consultant'), #an observer can be invited by an outside org to be their consultant
    )
    member_type = models.PositiveSmallIntegerField(choices=MEMBER_TYPE_CHOICES, blank=True, default = 0)

    membership_validated = models.BooleanField(default=False)
    def is_membership_validated(self):
        return self.membership_validated
    
  

    MEMBER_BADGE_CHOICES = (
        (1, 'observer'), 
        (2, 'active'),
        (3, 'informed and engaged'), 
    )
    member_badge = models.PositiveSmallIntegerField(choices=MEMBER_BADGE_CHOICES, blank=True, default = 1)
    
    tags = TaggableManager(through=TaggedObject)

    def get_tag_names(self):
        return [tag.name for tag in Tag.objects.get_for_object(self)]


    # User.objects.filter(user=self).annotate(
    #                                         mrank=Func(F('posts') / 10, function 'CEIL'),
    #                                     )
    # def _get_member_badge(self):
    #     mrank = getattr(self, 'mrank', None)
    #     if mrank is None:
    #         mrank = 0
    #     return MEMBER_BADGE_CHOICES[mrank]
    # member_badge = property(_get_member_badge)

    # OBSERVER_BADGE_CHOICES = ['unfamiliar', 'familiar', 'informed',]
    # OFFICIAL_BADGE_CHOICES = ['elitist', 'representative', 'populist',]
    # MESSENGER_BADGE_CHOICES = ['unresponsive','responsive','interactive',]
    # CONSULTANT_BADGE_CHOICES = ['newly commissioned', 'contributor', 'trusted',]
    # [person.fullname for person in Person.objects.all()]
    # use this to access non-field property of model

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

#badges for regulars: regular, citizen, active citizen, informed citizen
#badges for gov officials: populist, representative, elitist
#badges for bus officials: responsive, listenner, responsible, elitist, hardliner



class UserEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update = models.DateTimeField(auto_now = True)
    timestamp= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


def upload_to(instance, filename):
    return 'images/%s/%s' % (instance.user.user.user_id, filename)
class UserAvatar(models.Model):
    avatar = models.ImageField(upload_to=upload_to)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username









