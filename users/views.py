
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView, DetailView, ListView, UpdateView
#from topics.models import Topic
User = get_user_model()
from .forms import loginform, RegisterForm, ProfileForm, FollowForm, UserAddTagForm
from .models import Profile
from organizations.models import Organization
from dal.autocomplete import Select2QuerySetView


class OrgAutocomplete(Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor 's permission!
        if not self.request.user.is_authenticated():
            return Organization.objects.none()
        qs = Organization.objects.all()

        qs = qs.filter(
                           usermembership_set__is = self.request.user, #suspect!!!! but important for security reasons
            )

        return qs


class RegisterView(CreateView):
   form_class = RegisterForm
   template_name = "users/registration.html"
   success_url = reverse_lazy('users:login')
   context = {
      'form': RegisterForm()
   }
class UpdateProfileView(UpdateView):
    def is_authen(self):
        if not request.user.is_authenticated():
            redirect('users:login')
    form_class = ProfileForm
    model = Profile
    template_name = 'users/profile_update.html'
    def get_success_url(self):
        return reverse('users:user_profile', kwargs={'username': self.kwargs.get('username')})
    def get_object(self, queryset=None):
        obj = Profile.objects.get(user = self.request.user)
        return obj


class LoginView(FormView):
   form_class = loginform
   # success_url = reverse_lazy('users:index')
   template_name = "users/login.html"
   def form_valid(self,form):
       request = self.request
       next_ = request.GET.get('next')
       next_post = request.POST.get('next')
       #redirect_path = next_ or next_post or None
       redirect_path = reverse_lazy('users:index')
       username = form.cleaned_data.get("username")
       password = form.cleaned_data.get("password")
       user = authenticate(request, username=username, password=password)

       if user is not None:
          if user.is_active:
             login(request, user)
          try:
             del request.session['guest_email_id']
          except:
             pass
          if is_safe_url(redirect_path, request.get_host()):
             return redirect(redirect_path)
          else:
             return redirect("/")
       return super(LoginView, self).form_invalid(form)
#
def logout_view(request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('users:index'))

def index(request):
    def get_queryset(self):
        queryset = self.request.user
        return queryset

    def post(self, request, *args, **kwargs):
        form = UserAddTagForm(request.POST)
        if form.is_valid():
            user.tags.add(form.cleaned_data['new_tag'])
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        context = {
                   'form': UserAddTagForm(),
                   }
        return context
    return render(request, 'users/index.html')


class IndexView(ListView):
    template_name = 'users/index.html'
    #queryset = Topic.objects.all()
    #model = Topic
    #paginate_by = 10
    #ordering = ['-created_date']
    # if use this comment out model = Topic and add context_object_name
    context_object_name = "topics"
    def get_queryset(self):
        queryset = (Topic.objects
                    .all()
                    .order_by('-created_date'))
        # queryset = Topic.objects.all().prefetch_related('bids').filter(user=self.request.user)) #uncomment model = Topic
        #
        return queryset


class UserDetail(DetailView):
    model = User

    # def get_success_url(self):
    #     return reverse('organizations:specific_org_topics:org_topic',
    #                    kwargs={'topic_slug': self.topic_slug, 'org_slug': self.organization.org_slug})

    template_name = "users/specific_user.html"
    slug_field = "username"
    slug_url_kwarg = "username"

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        return self.render_to_response(self.get_context_data())

        form_follow = FollowForm()
        if form_follow.is_valid():
            form_follow.save()
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        username = self.kwargs.get('username') #get username from url using self.kwargs.get(), only works inside a def inside class
        self.object = self.get_object()
        context = super(UserDetail, self).get_context_data(**kwargs)

        context = {'specific_user': User.objects.get(username=username),
                    'form_follow': FollowForm(),
                   }
        return context




