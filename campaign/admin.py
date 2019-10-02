from django.contrib import admin
# Register your models here.
from .models import Campaign
from organizations.models import Organization
# class ExplorePostInline(admin.TabularInline):
#     model = ExplorePost

class CampaignAdmin(admin.ModelAdmin):
    campaign = Campaign
    fieldsets = [
        (None, {'fields': ['name', 'organization', 'summary', 'tags']}),
        ('Permissions', {'fields': ['active']}),
    ]
    list_filter = ['name', 'created_date']
    # inlines = [ExplorePostInline,
    #              ]
    list_display = (
    'name', 'created_date', 'summary', 'is_active', 'organization')
    search_fields = ['name']
    class Meta:
        model = Campaign

admin.site.register(Campaign, CampaignAdmin)

