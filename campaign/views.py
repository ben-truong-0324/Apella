from .models import Campaign
from .forms import RegisterCampaignForm
from django.shortcuts import get_object_or_404
from organizations.models import Organization

# Create your views here.
from django.views.generic import DetailView, CreateView, DeleteView
from django.views.generic.edit import FormMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden
# from .forms import  ExplorePostAddForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.


def index(request, org_slug):
    org = Organization.objects.filter(org_slug = org_slug)
    context = {'campaigns': Campaign.objects.filter(organization = org)}
    return render(request, 'campaigns/index.html', context)

# def share(request, campaign_slug):
#     user = request.user
#     campaign = Campaign.objects.get(campaign_slug=campaign_slug)
#     org.members.add(user)
#     org.save()
#     return redirect(org)
class RegisterCampaignView(CreateView):
   form_class = RegisterCampaignForm
   # org_slug= self.kwargs['org_slug']

   template_name = "campaigns/registration.html"
   success_url = reverse_lazy('organizations:index')
   #success_url = reverse('organizations:specific_org_topics:org_topic', kwargs={'topic_slug' : self.topic_slug, 'org_slug' : self.organization.org_slug})

   context = {
      'form': RegisterCampaignForm(),
      # 'org': Organization.objects.get(org_slug=org_slug),
   }
   def dispatch(self, request, *args, **kwargs):
        
        self.organization = get_object_or_404(Organization, org_slug=kwargs['org_slug'])
        return super().dispatch(request, *args, **kwargs)

   def form_valid(self, form):
     
        form.instance.organization = self.organization
        return super().form_valid(form)

class CampaignDetail(DetailView):
    model = Campaign

    template_name = "campaigns/campaign.html"
    slug_field = "campaign_slug"
    slug_url_kwarg = "campaign_slug"
    context_object_name = 'campaign'
    if request.method != 'POST':
        #no comment submitted
        form = CommentForm()
    else:
        #posted
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author=request.user
            form.save()
            campaign=Campaign.objects.get(campaign_slug=campaign_slug)
            return redirect(campaign)




   #  def post(self, request, *args, **kwargs):
   #      if not request.user.is_authenticated:
   #          return HttpResponseForbidden()
   #      topic = self.get_object()  ###suspect wth the slug and self.get_object
   #      form = TopicAddTagForm(request.POST)
   #      form_explore_post = ExplorePostAddForm(topic=topic, user=request.user, data=request.POST)
   #      if form.is_valid():
   #          topic.tags.add(form.cleaned_data['tag'])
   #          topic.organization.tags.add(form.cleaned_data['tag'])
   #      if form_explore_post.is_valid():
   #          form_explore_post.save()
   #      return self.render_to_response(self.get_context_data())
    # def get_context_data(self, **kwargs):
    #   #   topic_slug = self.kwargs.get('topic_slug') #get topic_slug from url using self.kwargs.get(), only works inside a def inside class
    #   #   self.object = self.get_object()
    #     context = super(CampaignDetail, self).get_context_data(**kwargs)

    #     context = {'campaign': Campaign.objects.get(campaign_slug=campaign_slug),
    #                # 'impacts': Organization.objects.get(org_slug=org_slug).org_impacts.all(),
    #               #  'form': TopicAddTagForm(),
    #               #   'form_explore_post': ExplorePostAddForm(),
    #               #   'explore_posts': Topic.objects.get(topic_slug=topic_slug).topic_explore_posts.all(),
    #             #    'membership': Topic.objects.get(topic_slug=topic_slug).organization.all(),

    #                 #'explore_posts': ExplorePost.objects.get(self.topic.topic_slug = topic_slug),
    #                }
    #     return context
