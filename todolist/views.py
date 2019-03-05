from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm


# Create your views here.

def index(request, error_message=None):
    print(error_message)
    TaskList = Task.objects.all().order_by('-id')
    return render(request, 'index.html', {'TaskList': TaskList, 'error_message': error_message})


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


def done(request, pk):
    task = Task.objects.get(pk=pk)
    task.toggle_done()
    return redirect('index')


def delete(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect('index')
