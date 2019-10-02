from django.contrib import admin
# Register your models here.
from .models import Topic, ExplorePost
from organizations.models import Organization
# Register your models here.
#
# class OrganizationsInline(admin.TabularInline):
#      model = Organization
class ExplorePostInline(admin.TabularInline):
    model = ExplorePost

class TopicAdmin(admin.ModelAdmin):
    topic = Topic
    fieldsets = [
        (None, {'fields': ['name', 'organization', 'summary', 'tags']}),
        ('Permissions', {'fields': ['active']}),
    ]
    list_filter = ['name', 'created_date']
    inlines = [ExplorePostInline,
                 ]
    list_display = (
    'name', 'created_date', 'summary', 'is_active', 'organization')
    search_fields = ['name']
    class Meta:
        model = Topic

admin.site.register(Topic, TopicAdmin)

