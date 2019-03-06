from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    task_text = forms.CharField(required=True, min_length=3, max_length=255)

    class Meta:
        model = Task
        fields = ['task_text']
