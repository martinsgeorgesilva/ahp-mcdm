from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.http import Http404

from user.models import User
from user.forms import UserCreateForm

class UserList(ListView):
    model = User


class UserDetail(DetailView):
    model = User


class UserCreate(CreateView):
    model = User
    form_class = UserCreateForm    
    success_url = reverse_lazy('user:list')


class UserUpdate(UpdateView):
    model = User
    fields = ['email', 'username']
    success_url = reverse_lazy('user:list')


class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('user:list')


    

    
    


