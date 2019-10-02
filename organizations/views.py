from django.shortcuts import render
from django.views.generic import DetailView
from .models import Organization
# Create your views here.
#from topics.models import Topic
from django.views.generic import DetailView, ListView
from django.shortcuts import render
from django.views.generic import CreateView, FormView, UpdateView
from .forms import RegisterForm, OrgAddTagForm
from django.urls import reverse_lazy
from django.shortcuts import redirect


#
# class OrganizationView(DetailView):
#     model = Organization
#     template_name = "organizations/specific_org.html"
#     context_object_name = 'org'
#
#     slug_field = "org_slug"
#     slug_url_kwarg = "org_slug"



    #
    # paginate_by = 10
    # queryset = Organization.objects.filter(name="Cloyne")
    # context_object_name = "organization_list"


    # organization = Organization.objects.filter(name=slug_field)
    # def get_queryset(self):
    #     queryset = (Topic.objects
    #                 .filter(organization.name = self.slug_field)
    #
    #                 .order_by('-created_date'))
    #     child.name for child in obj.children.all()
    #
    #     return queryset

def index(request):
    context = {'orgs': Organization.objects.all(),
    # 'orgs_sorted_tags': Organization.objects.filter(tags__name__in=["laundry", ]).distinct(),
    #'user_org': Organization.objects.filter(user = request.user),
    # 'user_membership': request.user.usermembership_set.all(),
               }
    return render(request, 'organizations/index.html', context)


class RegisterView(CreateView):
   form_class = RegisterForm
   template_name = "organizations/registration.html"
   success_url = reverse_lazy('organizations:index')
   context = {
      'form': RegisterForm()
   }

def specific_org(request, org_slug):
    context = {'org': Organization.objects.get(org_slug=org_slug),
               'impacts': Organization.objects.get(org_slug=org_slug).org_impacts.all(),
               }

        # return self.render_to_response(self.get_context_data())
    
def join(request, org_slug):
    user = request.user
    org = Organization.objects.get(org_slug=org_slug)
    org.members.add(user)
    org.save()
    return redirect(org)


# def unjoin(request, target_id):
#     follow = Follow.objects.filter(user=request.user, target_id=target_id).first()
#     if follow is not None:
#         follow.delete()
#     return redirect("/")

class OrgDetail(DetailView):
    model = Organization
    template_name = 'organizations/specific_org.html'
    slug_field = "org_slug"
    slug_url_kwarg = "org_slug"
    # This was my attempt to work it into the View...
    def post(self, request, *args, **kwargs):
        organization = self.get_object()  ###suspect wth the slug and self.get_object
        form = OrgAddTagForm(request.POST)
        if form.is_valid():
            organization.tags.add(form.cleaned_data['tag'])
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        org_slug = self.kwargs.get('org_slug')
        self.object = self.get_object()
        context = super(OrgDetail, self).get_context_data(**kwargs)

        context = {'org': Organization.objects.get(org_slug=org_slug),
                   #'impacts': Organization.objects.get(org_slug=org_slug).org_impacts.all(),
                   'form': OrgAddTagForm(),
                   }
        return context
class OrgTagList(DetailView):
    # queryset = Organization
    # def get_queryset(self):  #(self, **kwargs):
    #     queryset =
    #     # if self.request.GET.get("browse"):
    #     #     selection = self.request.GET.get("browse")
    #     #     if selection == "Cats":
    #     #         queryset = Cats.objects.all()
    #     org_slug = self.kwargs.get('org_slug')
    #     self.object = self.get_object()
    #     context = super().get_context_data(**kwargs)
    #     context['org'] = Organization.objects.get(org_slug=org_slug)
    #     return queryset
    model = Organization
    template_name = 'organizations/specific_org_tag_list.html'

    slug_field = "org_slug"
    slug_url_kwarg = "org_slug"

    # This was my attempt to work it into the View...

    def get_context_data(self, **kwargs):
        org_slug = self.kwargs.get('org_slug')
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        context = {'org': Organization.objects.get(org_slug=org_slug),
                   # 'impacts': Organization.objects.get(org_slug=org_slug).org_impacts.all(),
                   'form': OrgAddTagForm(),
                   }
        return context


#
# class OrgTagDetail(DetailView):
#     def get_object(self):
#         org_slug = self.kwargs.get('organiser')
#         tag_slug = self.kwargs.get('event')
