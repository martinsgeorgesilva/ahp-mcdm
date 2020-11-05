from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import Http404

from research.models import Research, Excution
from groups.models import Groups, GroupRelationship
from django.http import JsonResponse


from django.views.generic import TemplateView





class ResearchList(ListView):
    model = Research

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        context = Research.objects.filter(created_by=self.request.user)
        return context




class ResearchDetail(DetailView):
    model = Research
    groupId = None

    def get_initial(self, **kwargs):
        initial = super().get_initial()
        self.groupId = self.kwargs['pk']
        return initial

    def file_download(request):
        fsock = open('my_research.csv', 'r')
        response = HttpResponse(fsock, content_type='text')
        response['Content-Disposition'] = "attachment; filename=dados.csv"
        return response

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['groupId'] = self.groupId
        data['executions'] = Excution.objects.filter(group=self.object.Groups)
        a = list(Excution.objects.filter(group=self.object.Groups).values(
            'who', 
            'company', 
            'occupation',
            'ic',
            'criterions',
            'preferences',
            'age',
            'time_emp',
            'time_xp',
            'sexo',
            'escolaridade'
            )
        )
        # print(a)
        print(Groups.name)
        for el in a:
            print(el)
            for il in el['criterions']:
                print(il)
        df = pd.DataFrame(list(Excution.objects.filter(group=self.object.Groups).values()))
        df.to_csv('my_research.csv', sep='\t', encoding='utf-8')
        self.file_download()
        print(df)
        return data

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

import pandas as pd

class ResearchCreate(CreateView):
    model = Research
    fields = ['Groups', 'objective']
    success_url = reverse_lazy('research:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        print('aaaa', form.cleaned_data['Groups'])
        form.instance.created_by = self.request.user
        form.instance.Groups = form.cleaned_data['Groups']
        return super().form_valid(form)


class ResearchUpdate(UpdateView):
    model = Research
    fields = ['name']
    success_url = reverse_lazy('research:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ResearchDelete(DeleteView):
    model = Research
    success_url = reverse_lazy('research:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

from criterion.models import Criterion
from groups.models import GroupRelationship
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


from decimal import Decimal




from django.views.generic import TemplateView

class Success(TemplateView):
    template_name = "research/success.html"



class ExecutionView(CreateView):
    model = Excution
    fields = ['who', 'company', 'occupation', 'age', 'time_emp', 'time_xp', 'sexo', 'escolaridade']
    success_url = reverse_lazy('research:success')
    groupId = None
    template_name = 'research/excution_form.html'	
    http_method_names = ['get', 'post']
    quant_crit = None
    criterions = None
    email =  None
    ic = None
    vector_w = None

    
    def form_valid(self, form):
        form.instance.group = Groups.objects.get(pk=self.groupId)
        form.instance.ic = self.ic
        form.instance.criterions = self.criterions
        form.instance.preferences = self.vector_w
        form.instance.email = self.email
        aux_object = {}
        for el in range(len(self.criterions)):
            aux_object.update({self.criterions[el]:self.vector_w[el]})
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        ExGroup = Groups.objects.get(pk=self.groupId)
        ResearchActual = Research.objects.get(Groups=self.groupId)
        items = GroupRelationship.objects.filter(group=ExGroup)
        data['relations_list'] = [[items[i].criterion.name,items[j].criterion.name] for i in range(len(items)) for j in range(i+1, len(items))]
        data['len_relations'] = ExGroup.amount_questions()
        data['objects'] = ExGroup
        data['objective'] = ResearchActual
        data['id'] = ExGroup.id
        data['len_criterios'] = ExGroup.relations_count()
        return data



    def post(self, request, *args, **kwargs):
        az = Groups.objects.get(pk=request.POST['object_id'])
        items = GroupRelationship.objects.filter(group=az)
        criterions1 = []
        for el in items:
            criterions1.append(el.criterion.name)
        a = processPost(request.POST, criterions1)
        self.criterions = a[0]
        self.email = request.POST['email']
        self.ic = a[2]
        self.vector_w = a[1]
        return super().post(request, *args, **kwargs)



    def get_initial(self, **kwargs):
        initial = super().get_initial()
        self.groupId = self.kwargs['pk']
        return initial
    
    # def get_success_url(self):
    #     try:
    #         group = Groups.objects.get(pk=self.groupId)
    #         url = group.get_absolute_url()
    #     except AttributeError:
    #         raise ImproperlyConfigured(
    #             "No URL to redirect to.  Either provide matrix_a url or define"
    #             " matrix_a get_absolute_url method on the Model.")
    #     return url
    

import numpy as np 
import decimal 

    
def processPost(arg, criterion_list):
    response_array = []
    matrix_length = int(arg['qtd'])
    len_relations = int(arg['len_relations'])
    matrix_a = np.identity(matrix_length)
    matrix_b = np.identity(matrix_length)

    for integer in range(len_relations):
        response_array.append(relations_values(int(arg['range_'+ str(integer)])))

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

    new_object = []
    i = 0
    for el in criterion_list:
        new_object.append(round(vector_w[i],2))
        i += 1

    context = []
    context.append(criterion_list)
    context.append(new_object)
    aux = []
    for i in range(len(vector_c)):
        aux.append(vector_c[i] / vector_w[i])

    lambda_max = np.mean(aux)
    CI = (lambda_max - matrix_length) / (matrix_length-1)
    incosistency = round(CI/random_index_reference(matrix_length) * 100, 2)
    context.append(incosistency)
    return context
    

def random_index_reference(n):
    auxiliar_array = [0,0,0.58,0.9,1.12,1.24,1.32,1.41,1.45,1.49,1.51,1.48,1.56,1.57,1.59]
    return auxiliar_array[n-1]


