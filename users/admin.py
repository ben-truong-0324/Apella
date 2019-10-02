# Register your models here.
# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import User, UserEmail, Profile
from .forms import UserAdminChangeForm, UserAdminCreationForm
User = get_user_model()

# class UserMembershipInline(admin.TabularInline):
#     model = UserMembership

class UserEmailInline(admin.TabularInline):
    model = UserEmail
class ProfileInline(admin.TabularInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    form = UserAdminChangeForm #edit view
    add_form = UserAdminCreationForm #create view
    fieldsets = [
        (None, {'fields': ['email', 'username', 'password']}),
        ('User Information', {'fields': [], 'classes': ['collapse']}),
        ('Permissions', {'fields': ['admin','staff', 'confirmed_email'], 'classes': ['collapse']}),
    ]
    inlines = [ UserEmailInline, ProfileInline,
               ]
    list_filter = ['username', 'staff','active']
    list_display = ('email', 'user_id','confirmed_email', 'timestamp','is_admin', 'is_staff', 'is_confirmed_email',)
    search_fields = ['username', 'first_name', 'email']
    # class Meta:
    #     model = User



admin.site.register(User, UserAdmin)
#admin.site.unregister(Groups)