from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/done/', views.done, name='done'),
    path('<int:pk>/delete/', views.delete, name='delete')
]