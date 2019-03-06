from django.urls import path

from . import views
from todolist.views import TaskList, TaskCreate, TaskUpdate, TaskDelete

urlpatterns = [
    path('', TaskList.as_view(), name='index'),
    path('create/', TaskCreate.as_view(), name='create'),
    path('<int:pk>/done/', TaskUpdate.as_view(), name='done'),
    path('<int:pk>/delete/', TaskDelete.as_view(), name='delete'),
]