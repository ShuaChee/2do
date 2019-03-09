import uuid
from django.db import models


class Task(models.Model):
    task_text = models.CharField(max_length=128, error_messages={'required': 'Please, enter task text'}, blank=False,
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
    user_name = models.CharField(max_length=255, null=False, default=None)
    session_id = models.CharField(max_length=255, null=False)

    def new(self, user_name):
        self.user_name = user_name
        self.session_id = uuid.uuid1()
        self.save()

    def session_check(self, session_id):
        if MySession.objects.get(session_id=session_id):
            return True
        return False
