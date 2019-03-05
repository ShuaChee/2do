from django.db import models


# Create your models here.


class Task(models.Model):
    task_text = models.CharField(max_length=255)
    task_done = models.BooleanField(default=False)

    def __str__(self):
        return self.task_text
