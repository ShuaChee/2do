from django.shortcuts import render, redirect
from .models import Task


# Create your views here.

def index(request):
    TaskList = Task.objects.all()
    return render(request, 'index.html', {'TaskList': TaskList})


def create(request):
    task_text = request.POST['task_text']
    task = Task()
    task.task_text = task_text
    task.save()
    return redirect('index')


def done(request, pk):
    task = Task.objects.filter(id=pk).get()
    print(task)
    task.task_done = not task.task_done
    task.save()
    return redirect('index')


def delete(request, pk):
    task = Task.objects.filter(id=pk)
    task.delete()
    return redirect('index')
