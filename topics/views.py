from .models import Topic, ExplorePost
from .forms import RegisterTopicForm, TopicAddTagForm

# Create your views here.
from django.views.generic import DetailView, CreateView, DeleteView
from django.views.generic.edit import FormMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden
from .forms import  ExplorePostAddForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.


def index(request):
    context = {'topics': Topic.objects.all()}
    return render(request, 'topics/index.html', context)
#

class RegisterTopicView(CreateView):
   form_class = RegisterTopicForm
   template_name = "topics/registration.html"
   success_url = reverse_lazy('organizations:index')
   #success_url = reverse('organizations:specific_org_topics:org_topic', kwargs={'topic_slug' : self.topic_slug, 'org_slug' : self.organization.org_slug})

   context = {
      'form': RegisterTopicForm()
   }


def specific_topic(request, org_slug, topic_slug):
    context = {'topic': Topic.objects.get(topic_slug = topic_slug),
               'impacts':Impact.objects.all()
               }

    return render(request, "topics/specific_topic.html", context,)

class TopicDetail(DetailView):
    model = Topic

    # def get_success_url(self):
    #     return reverse('organizations:specific_org_topics:org_topic',
    #                    kwargs={'topic_slug': self.topic_slug, 'org_slug': self.organization.org_slug})

    template_name = "topics/specific_topic.html"
    slug_field = "topic_slug"
    slug_url_kwarg = "topic_slug"

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        topic = self.get_object()  ###suspect wth the slug and self.get_object
        form = TopicAddTagForm(request.POST)
        form_explore_post = ExplorePostAddForm(topic=topic, user=request.user, data=request.POST)
        if form.is_valid():
            topic.tags.add(form.cleaned_data['tag'])
            topic.organization.tags.add(form.cleaned_data['tag'])
        if form_explore_post.is_valid():
            form_explore_post.save()
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        topic_slug = self.kwargs.get('topic_slug') #get topic_slug from url using self.kwargs.get(), only works inside a def inside class
        self.object = self.get_object()
        context = super(TopicDetail, self).get_context_data(**kwargs)

        context = {'topic': Topic.objects.get(topic_slug=topic_slug),
                   # 'impacts': Organization.objects.get(org_slug=org_slug).org_impacts.all(),
                   'form': TopicAddTagForm(),
                    'form_explore_post': ExplorePostAddForm(),
                    'explore_posts': Topic.objects.get(topic_slug=topic_slug).topic_explore_posts.all(),
                #    'membership': Topic.objects.get(topic_slug=topic_slug).organization.all(),

                    #'explore_posts': ExplorePost.objects.get(self.topic.topic_slug = topic_slug),
                   }
        return context




def list_topics(request, org_slug):
    context = {'topics': Topic.objects.filter(organization__org_slug = org_slug)}
    return render(request, "topics/index.html", context)

class TopicExplore(DetailView):
    model = Topic
    template_name = "topics/specific_topic_explore.html"
    slug_field = "topic_slug"
    slug_url_kwarg = "topic_slug"
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        topic = self.get_object()  ###suspect wth the slug and self.get_object

        form_explore_post = ExplorePostAddForm(topic=topic, user=request.user, data=request.POST)
        
        if form_explore_post.is_valid():
            form_explore_post.save()
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        topic_slug = self.kwargs.get('topic_slug') #get topic_slug from url using self.kwargs.get(), only works inside a def inside class
        self.object = self.get_object()
        context = super(TopicExplore, self).get_context_data(**kwargs)

        context = {'topic': Topic.objects.get(topic_slug=topic_slug),
                            'form_explore_post': ExplorePostAddForm(),
                   }
        return context

class TopicOutcomes(DetailView):
    model = Topic
    template_name = "topics/specific_topic_outcomes.html"
    slug_field = "topic_slug"
    slug_url_kwarg = "topic_slug"
    

# class PostView(generic.DetailView):
#     model = Post
#     template_name = 'blog/post.html'

#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         # Add in the username
#         comments = Comment.objects.filter(post=self.kwargs['pk'])
#         context['comments'] = comments
#         return context


# @login_required(login_url="/login/")


# class PostCreate(LoginRequiredMixin, CreateView):
#     model = Post
#     fields = ['title', 'body']
#     template_name = 'blog/create_post.html'
#     login_url = reverse_lazy('login')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)


# class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Post
#     fields = ['title', 'body']
#     template_name = 'blog/create_post.html'
#     login_url = reverse_lazy('login')

#     def test_func(self):
#         return Post.objects.get(id=self.kwargs['pk']).user == self.request.user


# class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Post
#     success_url = reverse_lazy('blog:home')
#     login_url = reverse_lazy('login')

#     def test_func(self):
#         return Post.objects.get(id=self.kwargs['pk']).user == self.request.user
