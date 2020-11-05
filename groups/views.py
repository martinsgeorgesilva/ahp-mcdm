from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import Http404

from groups.models import Groups, GroupRelationship
from criterion.models import Criterion


from django.views.generic import TemplateView





class GroupsList(ListView):
    model = Groups

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        context = Groups.objects.filter(created_by=self.request.user)
        return context


class GroupsDetail(DetailView):
    model = Groups
    http_method_names = ['get', 'post']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['criterion_list'] = Criterion.objects.filter(created_by=self.request.user)
        data['relations_list'] = GroupRelationship.objects.filter(group=self.object)
        return data


import numpy as np 


class PublishView(DetailView):
    template_name = 'groups/groups_publish.html'	
    model = Groups
    http_method_names = ['get', 'post']
    quant_crit = None
    criterions = []

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['criterion_list'] = Criterion.objects.filter(created_by=self.request.user)
        items = GroupRelationship.objects.filter(group=self.object)
        self.criterions = []
        for el in items:
            self.criterions.append(el.criterion.name)
        data['relations_list'] = [[items[i].criterion.name,items[j].criterion.name] for i in range(len(items)) for j in range(i+1, len(items))]
        data['len_relations'] = self.object.amount_questions()
        data['objects'] = self.object
        data['id'] = self.object.id
        data['len_criterios'] = self.object.relations_count()
        return data

    def post(self, request, *args, **kwargs):
        print(request.POST)
        processPost(request.POST, self.criterions)



# def relations_values(i):
#     from_for = {
#         '0':9,
#         '1':6,
#         '2':3,
#         '3':1,
#         '4':1/3,
#         '5':1/6,
#         '6':1/9,
#     }
#     return from_for[str(i)]

def relations_values(i):
    from_for = {
        '0':9,
        '1':8,
        '2':7,
        '3':6,
        '4':5,
        '5':4,
        '6':3,
        '7':2,
        '8':1,
        '9':1/2,
        '10':1/3,
        '11':1/4,
        '12':1/5,
        '13':1/6,
        '14':1/7,
        '15':1/8,
        '16':1/9,
    }
    return from_for[str(i)]

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

@csrf_exempt
def AjaxPostView(request):
    objectDict = json.loads(request.body.decode("utf-8"))
    print
    items = GroupRelationship.objects.filter(group=objectDict['object_id'])
    aux = []
    for el in items:
        aux.append(el.criterion.name)
    values =  processPost(objectDict, aux)
    return HttpResponse(values)

def processPost(arg, criterion_list):
    print(criterion_list)
    response_array = []
    matrix_length = int(arg['qtd'])
    len_relations = int(arg['len_relations'])
    matrix_a = np.identity(matrix_length)
    matrix_b = np.identity(matrix_length)

    for integer in range(len_relations):
        response_array.append(relations_values(int(arg['range_'+ str(integer)])))
    print(response_array)

    stepper_control = 0
    for line in range(matrix_length-1):
        boolean_control = False
        for column in range(matrix_length-1):
            if matrix_a[line][column] == 1 and not boolean_control:
                boolean_control = True
            if boolean_control:
                matrix_a[line][column+1] = response_array[stepper_control]
                stepper_control += 1

    for line in range(matrix_length):
        for column in range(matrix_length):
            if  column < line:
                matrix_a[line][column] = 1/matrix_a[column][line]

    for line in range(matrix_length):
        for column in range(matrix_length):
            matrix_b[line][column] = matrix_a[line][column]/matrix_a.sum(axis=0)[column]

    vector_w = np.mean(matrix_b, axis=1)
    vector_c = matrix_a.dot(vector_w)

    new_object = {}
    i = 0
    for el in criterion_list:
        new_object.update({el:vector_w[i]})
        i += 1

    context = {}
    context.update({'prioridades': new_object })
    print(new_object)


    aux = []
    for i in range(len(vector_c)):
        aux.append(vector_c[i] / vector_w[i])

    lambda_max = np.mean(aux)
    CI = (lambda_max - matrix_length) / (matrix_length-1)
    incosistency = round(CI/random_index_reference(matrix_length) * 100, 2)
    context.update({'inconsistencia': incosistency })
    return JsonResponse(context, safe=False)
    

def random_index_reference(n):
    auxiliar_array = [0,0,0.58,0.9,1.12,1.24,1.32,1.41,1.45,1.49,1.51,1.48,1.56,1.57,1.59]
    return auxiliar_array[n-1]



class GroupsCreate(CreateView):
    model = Groups
    fields = ['name']
    success_url = reverse_lazy('groups:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

from django.http import JsonResponse

class RelationshipCreate(CreateView):
    model = GroupRelationship
    fields = ['group', 'criterion']
    returId = None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        self.returId = form.cleaned_data['group'].id
        return super().form_valid(form)

    def get_success_url(self):
        try:
            group = Groups.objects.get(pk=self.returId)
            url = group.get_absolute_url()
        except AttributeError:
            raise ImproperlyConfigured(
                "No URL to redirect to.  Either provide matrix_a url or define"
                " matrix_a get_absolute_url method on the Model.")
        return url

    def get_initial(self, **kwargs):
        initial = super().get_initial()
        initial['group'] = self.kwargs['pk']
        return initial

        

class GroupsUpdate(UpdateView):
    model = Groups
    fields = ['name']
    success_url = reverse_lazy('groups:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class GroupsDelete(DeleteView):
    model = Groups
    success_url = reverse_lazy('groups:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)