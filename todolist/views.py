from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from .models import Task, MySession
from .forms import TaskForm


class TaskList(ListView):
    model = Task
    context_object_name = 'task_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_name'] = self.get_user()
        return context

    def get_user(self):
        session_id = self.request.COOKIES[settings.MY_SESSION_ID]
        session_user = MySession.objects.get(session_id=session_id)
        return session_user.user_name


class TaskCreate(CreateView):
    form_class = TaskForm
    model = Task

    def form_valid(self, form):
        form.save()
        return redirect('index')

    def form_invalid(self, form):
        task_list = Task.objects.all()
        user_name = TaskList.get_user(self)
        return render(self.request, 'todolist/task_list.html',
                      {'task_list': task_list, 'form': form, 'user_name': user_name})


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


class MyLogin(View):
    def get(self, request):
        return render(self.request, 'todolist/login.html')

    def post(self, request):
        self.user_name = request.POST['user_name']
        self.password = request.POST['user_password']
        try:
            self.user = User.objects.get(username=self.user_name)
        except User.DoesNotExist:
            errors = 'Invalid username or password'
            return render(self.request, 'todolist/login.html', {'errors': errors})
        if not self.user.check_password(self.password):
            errors = 'Invalid username or password'
            return render(self.request, 'todolist/login.html', {'errors': errors})
        else:
            session = MySession()
            session.new(user_name=self.user_name)
            response = redirect('index')
            response.set_cookie(settings.MY_SESSION_ID, session.session_id)
            return response


class MyLogout(View):
    def get(self, request):
        try:
            session_id = request.COOKIES[settings.MY_SESSION_ID]
        except:
            return redirect('login')
        response = redirect('login')
        response.delete_cookie(settings.MY_SESSION_ID)
        try:
            session = MySession.objects.get(session_id=session_id)
            session.delete()
        finally:
            return response
