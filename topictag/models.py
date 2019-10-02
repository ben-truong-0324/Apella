from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Tag(TagBase):
    # ... fields here
    name = models.CharField(max_length=255, unique = True,)
    description = models.TextField(blank=True)
    user_bookmarked = models.BooleanField(default = False,)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    # ... methods (if any) here


class TaggedObject(GenericTaggedItemBase):
    tag = models.ForeignKey(Tag,
                            related_name="%(app_label)s_%(class)s_items",
                            on_delete=models.CASCADE)