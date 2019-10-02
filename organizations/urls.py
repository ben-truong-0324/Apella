from django.urls import path,include
from . import views
from django.contrib.auth.decorators import login_required

app_name = "organizations"

urlpatterns = [
    # path('', views.IndexView.as_view(), name='<slug>.index'),

    path('', views.index, name = "index"),
    path('register/new_org/', views.RegisterView.as_view(), name = "register"),
    #path('<slug:org_slug>/', views.specific_org, name = "specific_org"),
    path('<slug:org_slug>/', views.OrgDetail.as_view(), name = "specific_org"),

    #to detail of tags
    path('<slug:org_slug>/tags/', views.OrgTagList.as_view(), name = "specific_org_tags"),

    path('<slug:org_slug>/', include('topics.urls', namespace = "specific_org_topics")),

    path('<slug:org_slug>/campaigns/', include('campaign.urls', namespace = 'org_campaigns')),
    path('<slug:org_slug>/join/', login_required(views.join), name='join'),
    ]