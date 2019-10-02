
# Create your models here.
from django.db import models
# Create your models here.
import uuid
from django.template.defaultfilters import slugify
from django.urls import reverse, reverse_lazy
from taggit.managers import TaggableManager
from django.conf import settings
from topictag.models import TaggedObject, Tag
from django.contrib.auth import get_user_model
User = get_user_model()


class Organization(models.Model):
    name = models.CharField(max_length= 255)
    location_street = models.CharField(max_length = 255)
    location_city = models.CharField(max_length = 255)
    location_state = models.CharField(max_length = 255)
    location_country = models.CharField(max_length = 255)
    location_ZIP = models.IntegerField()
    summary = models.TextField()
    created_date = models.DateTimeField('Created date', auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

    org_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    active  = models.BooleanField(default=False) #need verification
    confirmed_identity = models.BooleanField(default=False)
    government = models.BooleanField(default = False)
    private = models.BooleanField(default=False)

    #decision_makers = models.ManyToManyField(User, related_name='+')
    #constituent = models.ManyToManyField(User, related_name='+')
    #username_field and password are required by default

    # objects = OrganizationManager()

    tags = TaggableManager(through=TaggedObject)


    def get_tag_names(self):
        return [tag.name for tag in Tag.objects.get_for_object(self)]

    def get_name(self):
        return self.name
    #property
    def is_government(self):
        return self.government
    def is_private(self):
        return self.private
    def is_active(self):
        return self.active
    def is_confirmed_identity(self):
        return self.confirmed_idenity

    org_slug = models.SlugField(max_length=250, unique=True)

    def save(self, *args, **kwargs):
        self.org_slug = slugify(self.name)
        super(Organization, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('organizations:specific_org', kwargs={'org_slug' : self.org_slug})
    def get_tag_list_url(self):
        return reverse('organizations:specific_org_tags', kwargs={'org_slug' : self.org_slug})


    #add in org_type, adding additional files of org
    # org_model = models.ForeignKey(OrgModel, on_delete=models.CASCADE)

    ORG_TYPE_CHOICES = (
        (0, 'not specified'),
        (1, 'city'),
        (2, 'state'),
        (3, 'federal'),
        (4, 'agency'),
        (5, 'department'),
        (6, 'company'),
        (7, 'house'),
        (8, 'school'),
    )

    org_type = models.PositiveSmallIntegerField(choices=ORG_TYPE_CHOICES, blank=True, default = 0)
    members = models.ManyToManyField(User, blank=True, related_name='orgs')    
# class Member(models.Model):
#     member = models.ForeignKey(User, related_name='members', on_delete=models.CASCADE,)
#     organization = models.ForeignKey(Organization, related_name='organizations', on_delete=models.CASCADE,)
    
#     class Meta:
#         unique_together = ('member', 'organization')

#     def __unicode__(self):
#         return u'%s is member of %s' % (self.member, self.organization)

class OrgProfile(models.Model):
    pass

class CommunityWiki(models.Model):

    pass

# class OrgModel(models.Model):
#     org_type = models.CharField(max_length=255, blank = True)
#     org_type_description = models.TextField(blank=True)
#     org_files = models.



# class OrgMembership(models.Model):
#     membership_type = models.CharField(max_length=255, blank=True)
#     membership_type_description = models.TextField(blank=True)
#     ass_model = models.ForeignKey(OrgModel)
#     member = models.ForeignKey( related_name="org_member", on_delete=models.CASCADE, blank = True, null = True)


#     roles = models.CharField(max_length=255, blank = True)
#     hierch_0 = models.BooleanField(default=True) #observer
#     hierch_1 = models.BooleanField(default=False) #member
#     hierch_2 = models.BooleanField(default=False) # staff
#     hierch_3 = models.BooleanField(default=False) # DeliDeX's specific org's managers

#go wth:
# class OrgMember:
#   permission= 
#class OrgAdmin:
#   permission= ....
#hardcode for now
# class Role(models.Model):
#   '''
#   The Role entries are managed by the system,
#   automatically created via a Django data migration.
#   '''
#   STUDENT = 1
#   TEACHER = 2
#   SECRETARY = 3
#   SUPERVISOR = 4
#   ADMIN = 5
#   ROLE_CHOICES = (
#       (STUDENT, 'student'),
#       (TEACHER, 'teacher'),
#       (SECRETARY, 'secretary'),
#       (SUPERVISOR, 'supervisor'),
#       (ADMIN, 'admin'),
#   )

#   id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

#   def __str__(self):
#       return self.get_id_display()

# class OrgMember(models.Model):

