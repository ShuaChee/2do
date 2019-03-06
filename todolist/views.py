from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Task
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

    '''def post(self, request):
        return redirect('index')
        
    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = Task()
            task.new(form.cleaned_data['task_text'])
            return redirect('index')

    def get(self, request):
        return redirect('index')  # если GET то просто назад к списку
'''


class TaskUpdate(UpdateView):

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.toggle_done()
        return redirect('index')


class TaskDelete(DeleteView):
    '''С POST было бы короче..'''

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect('index')


def create(request):
    if request.method == 'POST':
        taskform = TaskForm(request.POST)
        if taskform.is_valid():
            task_text = taskform.cleaned_data['task_text']
            task = Task()
            task.new(task_text)
            return redirect('index')
        else:
            return index(request, error_message="Invalid task text")
    return redirect('index')
