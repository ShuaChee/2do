import uuid
from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    task_text = models.CharField(max_length=128, error_messages={'required': 'Please, enter task text'}, blank=False,
                                 null=False)
    task_done = models.BooleanField(default=False)
    task_archived = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete='CASCADE')

    class Meta:
        ordering = ['-id']
        managed = True

    def __str__(self):
        return self.task_text

    def toggle_done(self):
        self.task_done = not self.task_done
        self.save()

    def toggle_archived(self):
        self.task_archived = not self.task_archived
        self.save()


class MySession(models.Model):
    user = models.ForeignKey(User, on_delete='CASCADE')
    session_id = models.CharField(max_length=255, null=False)

    class Meta:
        managed = True

    def new(self, user):
        self.user = user
        self.session_id = uuid.uuid1()
        self.save()

    @staticmethod
    def get_logged_in_user(session_id):
        try:
            session = MySession.objects.get(session_id=session_id)
            return session.user
        except MySession.DoesNotExist:
            return False

        