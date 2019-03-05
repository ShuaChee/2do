from django import forms


class TaskForm(forms.Form):
    task_text = forms.CharField(required=True, min_length=3, max_length=255)
