from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse

from extra_views import SortableListMixin

from project_share.models import Application, Project, Classroom, Approval
from project_share.forms import ProjectForm, ApprovalForm

class ApplicationList(ListView):
    model = Application

class ApplicationDetail(DetailView):
    model = Application

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.update({'content_type': 'application/x-java-jnlp-file'})
        return super(ApplicationDetail, self).render_to_response(context, **response_kwargs)

class ProjectList(SortableListMixin, ListView):
    sort_fields_aliases = [('name', 'by_name'), ('id', 'by_id'), ('votes', 'by_likes'), ]
    model = Project
    queryset = Project.approved_objects.all()

class ProjectDetail(DetailView):
    model = Project
    queryset = Project.approved_objects.all()

class ProjectJNLP(DetailView):
    model = Project
    template_name = "project_share/project_jnlp.xml"


    def render_to_response(self, context, **response_kwargs):
        response_kwargs.update({'content_type': 'application/x-java-jnlp-file'})
        return super(ProjectJNLP, self).render_to_response(context, **response_kwargs)

class ProjectCreate(CreateView):
    model = Project
    form_class = ProjectForm

    def dispatch(self, request, *args, **kwargs):
      self.kwargs = kwargs
      self.request = request
      return super(ProjectCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
      form.instance.owner = self.request.user
      return super(ProjectCreate, self).form_valid(form)

class ProjectUpdate(UpdateView):
    model = Project
    form_class = ProjectForm
    
    template_name = "project_share/project_edit.html"

class ApprovalCreate(CreateView):
    model = Approval
    form_class = ApprovalForm

    def dispatch(self, request, *args, **kwargs):
      self.kwargs = kwargs
      self.request = request
      return super(ApprovalCreate, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        form.instance.project_id = self.kwargs['project_pk']
        return super(ApprovalCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('approval-confirm')
