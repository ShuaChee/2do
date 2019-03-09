from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from .models import Task, MySession
from .forms import TaskForm


# Create your views here.

class TaskList(ListView):
    model = Task
    context_object_name = 'task_list'


class TaskCreate(CreateView):
    form_class = TaskForm
    model = Task

    def form_valid(self, form):
        form.save()
        return redirect('index')

    def form_invalid(self, form):
        task_list = Task.objects.all()
        errors = form.errors
        return render(self.request, 'todolist/task_list.html', {'task_list': task_list, 'errors': errors})


class TaskUpdate(UpdateView):

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.toggle_done()
        return redirect('index')


class TaskDelete(DeleteView):

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect('index')


class SessionView(View):

    def get(self, request):
        cookie = request.COOKIES.get('my_session_id')
        return cookie

    def set(self):
        session = MySession()
        response = HttpResponse.set_cookie('my_session_id', session.session_id)
        session.save()
        return response