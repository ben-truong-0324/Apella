from django.shortcuts import render
# from .models import Topic, ExplorePost
# from .forms import RegisterTopicForm, TopicAddTagForm, ExplorePostAddForm

# Create your views here.
from django.views.generic import DetailView, CreateView, DeleteView
from django.views.generic.edit import FormMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from topics.models import Topic
from .forms import PostStoryForm, CreateBlogForm, BlogAddTagForm, CommentBlogForm
from .models import Post, Blog, BlogComment

# #scraping
# import requests
# requests.packages.urllib3.disable_warnings()
# from bs4 import BeautifulSoup

# def scrape():
#     session = requests.Session()
#     session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
#     url = "https://www.theonion.com/"
#     content = session.get(url, verify=False).content

#     soup = BeautifulSoup(content, "html.parser")
#     columns = soup.find_all('div', 
#     {'class': 'curation_modelue__zone grid__zone'}) #find all returns list
#     print(len(columns))

# Create your views here.
class PostStoryView(CreateView):
    form_class = PostStoryForm
    model = Post
    template_name = "activities/post.html"
    def get_success_url(self):
        return reverse('organizations:specific_org_topics:org_topic', 
                kwargs={
                'topic_slug' : self.kwargs['topic_slug'], 
                'org_slug' : self.kwargs['org_slug'],
                })

    context = {
        'form': PostStoryForm()
    }
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.topic = Topic.objects.get(topic_slug=self.kwargs['topic_slug']) 
        obj.save()        
        return HttpResponseRedirect(self.get_success_url())

class CreateBlogView(LoginRequiredMixin, CreateView):
    form_class = CreateBlogForm
    model = Blog

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)
    template_name="activities/create_blog.html"
    def get_success_url(self):
        return reverse('home:index')
    
def blog_index(request):
    context = {'blogs': Blog.objects.all(),
               }
    return render(request, "activities/blog_index.html", context)

class BlogDetail(DetailView):
    model = Blog
    template_name = 'activities/specific_blog.html'
    slug_field = "blog_slug"
    slug_url_kwarg = "blog_slug"
    # This was my attempt to work it into the View...
    def post(self, request, *args, **kwargs):
        blog = self.get_object()  ###suspect wth the slug and self.get_object
        form = BlogAddTagForm(request.POST)

        form_comment = CommentBlogForm(blog=blog, user=request.user, data=request.POST)

        if form.is_valid():
            blog.tags.add(form.cleaned_data['tag'])
        if form_comment.is_valid():
            form_comment.save()
        return self.render_to_response(self.get_context_data())

    
    def get_context_data(self, **kwargs):
        blog_slug = self.kwargs.get('blog_slug')
        self.object = self.get_object()
        context = super(BlogDetail, self).get_context_data(**kwargs)
        blog = Blog.objects.get(blog_slug=blog_slug)
        context = {'blog': blog,
                        'form': BlogAddTagForm(),
                        'form_comment':CommentBlogForm(),
                        'comments': BlogComment.objects.filter(blog = blog)
                   }
        return context
