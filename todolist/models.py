from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    task_text = models.CharField(max_length=255, error_messages={'required': 'Please, enter task text'}, blank=False,
                                 null=False)
    task_done = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.task_text

    def toggle_done(self):
        self.task_done = not self.task_done
        self.save()


class MySession(models.Model):
    session_id = models.CharField(max_length=255, null=False)
