from django.urls import path

from todolist.views import TaskList, TaskCreate, TaskUpdate, TaskDelete, MyLogin, MyLogout

urlpatterns = [
    path('', TaskList.as_view(), name='index'),
    path('login/', MyLogin.as_view(), name='login'),
    path('logout/', MyLogout.as_view(), name='logout'),
    path('create/', TaskCreate.as_view(), name='create'),
    path('<int:pk>/done/', TaskUpdate.as_view(), name='done'),
    path('<int:pk>/delete/', TaskDelete.as_view(), name='delete'),
]