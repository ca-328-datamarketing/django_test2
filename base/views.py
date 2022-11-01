from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Task
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
# Create your views here.
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class CustomerLoginView(LoginView):
    template_name = 'base/login.html'
    fields = "__all__"
    redict_authenticated_user=True
    success_url = reverse_lazy('tasks')
    # def get_sussess_url(self):
    #     return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = "base/register.html"
    form_class = UserCreationForm
    redict_authenticated_user=True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)


class tasklist(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = "tasks"

    # def get_context_data(self, **kwargs):
    #     context = super(tasklist,self).get_context_data(**kwargs)
    #     context['tasks'] = context['tasks'].filter(user=self.request.user)
    #     # context['count'] = context['tasks'].filter(complete=False).count()
    #     return context

    # def get_queryset(self, *args, **kwargs):
    #     return super().get_queryset(*args, **kwargs).filter(
    #         user=self.request.user
    #     )



class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = "task"
    template_name = "base/task.html"

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete']
    context_object_name = "create"
    template_name = 'base/task_form.html'
    success_url = reverse_lazy("tasks")

    def form_invalid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields =  ['title','description','complete']
    context_object_name = "update"
    template_name = 'base/task_form.html'
    success_url = reverse_lazy("tasks")

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    fields = "__all__"
    context_object_name = "delete" ##viewsの中の変数の母体は'delete'という名前を付与
    template_name = 'base/task_confirm.html'
    success_url = reverse_lazy("tasks")
