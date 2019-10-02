from django.urls import path
from . import views

app_name = "activities"

urlpatterns = [
    path('share-story/', views.PostStoryView.as_view(), name = "share_story"),
    path('blogs/', views.blog_index, name="blogs_list"),
    path('blogs/create_blog/', views.CreateBlogView.as_view(), name ="create_blog"),
    path('blogs/<slug:blog_slug>/', views.BlogDetail.as_view(), name='specific_blog'),
]