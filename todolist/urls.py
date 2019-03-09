from django.urls import path

from todolist.views import TaskList, TaskCreate, TaskUpdate, TaskDelete, SessionView

urlpatterns = [
    path('', TaskList.as_view(), name='index'),
    path('sw/', SessionView.as_view(), name='sw'),
    path('create/', TaskCreate.as_view(), name='create'),
    path('<int:pk>/done/', TaskUpdate.as_view(), name='done'),
    path('<int:pk>/delete/', TaskDelete.as_view(), name='delete'),
]