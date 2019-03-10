from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from .models import Task, MySession
from .forms import TaskForm
from todolist.session import get_user


class TaskList(ListView):
    model = Task
    context_object_name = 'task_list'
    paginate_by = 10

    def get_queryset(self):
        user = get_user(self.request)
        query_set = Task.objects.filter(user=user, task_archived=False)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user(self.request)
        context['user_name'] = user.username
        context['main_list'] = 'True'
        return context


class TaskArchiveList(ListView):
    model = Task
    context_object_name = 'task_list'
    paginate_by = 10

    def get_queryset(self):
        query_set = Task.objects.filter(user=get_user(self.request), task_archived=True)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user(self.request)
        context['user_name'] = user.username
        return context


class TaskCreate(CreateView):
    form_class = TaskForm
    model = Task

    def form_valid(self, form):
        form.instance.user = get_user(self.request)
        form.save()
        return redirect('index')

    def form_invalid(self, form):
        # todo: тут явно что то не так :)
        # по хорошему нужно вернуть ошибку юзеру
        task_list = Task.objects.all()
        user = get_user(self.request)
        return render(self.request, 'todolist/task_list.html',
                      {'task_list': task_list, 'form': form, 'user_name': user.username})


class TaskUpdate(UpdateView):

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.toggle_done()
        return redirect('index')


class TaskArchive(UpdateView):

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.task_archived:
            response = redirect('archive_list')
        else:
            response = redirect('index')
        task.toggle_archived()
        return response


class TaskDelete(DeleteView):

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect('archive_list')


class MyLogin(View):
    def get(self, request):
        return render(self.request, 'todolist/login.html')

    def post(self, request):
        user_name = request.POST['user_name']
        password = request.POST['user_password']

        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return render(self.request, 'todolist/login.html', {'errors': 'Invalid username or password'})

        if not user.check_password(password):
            return render(self.request, 'todolist/login.html', {'errors': 'Invalid username or password'})
        else:
            session = MySession()
            session.new(user=user)
            response = redirect('index')
            response.set_cookie(settings.MY_SESSION_ID, session.session_id)
            return response


class MyLogout(View):
    def get(self, request):
        try:
            session_id = request.COOKIES[settings.MY_SESSION_ID]
        except KeyError:
            return redirect('login')
        response = redirect('login')
        response.delete_cookie(settings.MY_SESSION_ID)
        try:
            session = MySession.objects.get(session_id=session_id)
            session.delete()
        finally:
            return response
