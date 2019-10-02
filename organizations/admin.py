from django.contrib import admin
# Register your models here.
from .models import Organization
from topics.models import Topic
from django import forms

# Register your models here.

class TopicsInline(admin.TabularInline):
    model = Topic

class OrganizationAdmin(admin.ModelAdmin):
    organization = Organization
    fieldsets = [
        (None, {'fields': ['name','org_type', 'tags']}),
        ('Permissions', {'fields': ['active', 'confirmed_identity', 'government', 'private'], 'classes': ['collapse']}),
    ]
    list_filter = ['name', 'created_date',]
    inlines = [TopicsInline,
                 ]
    list_display = (
    'name', 'created_date',  'is_active', 
    'topics_display', 'org_type',
    )
    search_fields = ['name',]



    def topics_display(self, obj):
        return '\n'.join([o.name for o in obj.organization_topics.all()
        ])
    class Meta:
        model = Organization

admin.site.register(Organization, OrganizationAdmin)

