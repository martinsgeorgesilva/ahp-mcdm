from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import Http404

from criterion.models import Criterion


from django.views.generic import TemplateView





class CriterionList(ListView):
    model = Criterion

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CriterionList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        context = Criterion.objects.filter(created_by=self.request.user)
        return context


class CriterionDetail(DetailView):
    model = Criterion

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CriterionDetail, self).dispatch(*args, **kwargs)


class CriterionCreate(CreateView):
    model = Criterion
    fields = ['name']
    success_url = reverse_lazy('criterion:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CriterionCreate, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CriterionUpdate(UpdateView):
    model = Criterion
    fields = ['name']
    success_url = reverse_lazy('criterion:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CriterionUpdate, self).dispatch(*args, **kwargs)


class CriterionDelete(DeleteView):
    model = Criterion
    success_url = reverse_lazy('criterion:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CriterionDelete, self).dispatch(*args, **kwargs)

    

    
    


