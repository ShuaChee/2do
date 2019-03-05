from django.shortcuts import render, redirect
from .models import Task


# Create your views here.

def index(request):
    TaskList = Task.objects.all()
    return render(request, 'index.html', {'TaskList': TaskList})


def create(request):
    task_text = request.POST['task_text']
    task = Task()
    task.new(task_text)
    return redirect('index')


def done(request, pk):
    task = Task.objects.get(pk=pk)
    task.toggle_done()
    return redirect('index')


def delete(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect('index')
