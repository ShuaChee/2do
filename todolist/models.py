from django.db import models


# Create your models here.


class Task(models.Model):
    task_text = models.CharField(max_length=255, error_messages={'required': 'Please, enter task text'}, blank=False,
                                 null=False)
    task_done = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']


    def __str__(self):
        return self.task_text

    def new(self, task_text):
        self.task_text = task_text
        self.save()

    def toggle_done(self):
        self.task_done = not self.task_done
        self.save()
