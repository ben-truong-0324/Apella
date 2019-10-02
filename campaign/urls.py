from django.urls import path, include
from . import views

app_name = "campaigns"

urlpatterns = [
    # path('', views.IndexView.as_view(), name='<slug>.index'),

    path('', views.index, name = "index"),
    path('create_new/', views.RegisterCampaignView.as_view(), name = "create_campaign"),
    
    path('<slug:campaign_slug>/', views.CampaignDetail.as_view(), name="campaign"),
    # path('<slug:campaign_slug>/share/', login_required(views.share), name='share'),

    # path('<slug:campaign_slug>/share-pov/', views.SharePOV.as_view(), name="share_pov"),
    # path('topics/<slug:topic_slug>/explore/', views.TopicExplore.as_view(), name="topic_explore"),
    # path('topics/<slug:topic_slug>/', include('activities.urls', namespace="specific_topic_act")),

    # path('topics/', views.list_topics, name="org_list_topics"),
]