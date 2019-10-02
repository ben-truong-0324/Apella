from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    # path('register/org', views.RegisterOrgView.as_view(), name='org_register'),
    path('login/', views.LoginView.as_view(), name = 'login'),
    path('logout/', views.logout_view, name='logout'),
    path('org_autocomplete/', views.OrgAutocomplete.as_view(), name='org_autocomplete'),
    path('<slug:username>/profile/', views.UserDetail.as_view(), name ='user_profile'),
    path('<slug:username>/profile/update/', views.UpdateProfileView.as_view(), name ='profile_update'),

]