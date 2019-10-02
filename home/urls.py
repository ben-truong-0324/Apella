from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path('', views.landing, name='landing'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('home/', views.index, name='index'),

]