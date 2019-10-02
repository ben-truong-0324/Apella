from django.urls import path, include
from . import views

app_name = "topics"

urlpatterns = [
    # path('', views.IndexView.as_view(), name='<slug>.index'),

    path('', views.index, name = "index"),
    path('topics/create_new/', views.RegisterTopicView.as_view(), name = "create_topic"),
    #path('<slug:topic_slug>/', views.specific_topic, name = "specific_topic"),

    #path('topics/<slug:topic_slug>/', views.specific_topic, name= "org_topic"),
    path('topics/<slug:topic_slug>/', views.TopicDetail.as_view(), name="org_topic"),
    path('topics/<slug:topic_slug>/outcomes/', views.TopicOutcomes.as_view(), name="topic_outcomes"),
    path('topics/<slug:topic_slug>/explore/', views.TopicExplore.as_view(), name="topic_explore"),
    path('topics/<slug:topic_slug>/', include('activities.urls', namespace="specific_topic_act")),

    path('topics/', views.list_topics, name="org_list_topics"),

    # path('<org_slug:org_slug>/', views.OrganizationView.as_view(), name = "specific_org"),
    # path('orgs/<slug:org_slug>/topics/', include('topics.urls', namespace = 'topics')),
    

    # path('topics/<slug:topic_slug>/explore/', ExploreView.as_view(), name='explore'),
    # path('topics/<slug:topic_slug>/explore/post/', PostCreate.as_view(), name='create_post'),
    # path('topics/<slug:topic_slug>/explore/update', PostUpdate.as_view(), name='update_post'),
#    path('post/<int:pk>/delete/', PostDelete.as_view(), name='delete_post'),

]