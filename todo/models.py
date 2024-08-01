from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name='Задача')
    description = models.TextField(blank=True, null=True, verbose_name=' Описание')
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='created_tasks',
                                verbose_name='Создатель')
    can_read = models.ManyToManyField(to=User, blank=True, verbose_name='Могут читать')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title


class TaskPermission(models.Model):
    task = models.ForeignKey(Task, related_name='permissions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='task_permissions', on_delete=models.CASCADE)
    can_read = models.ManyToManyField(to=User, blank=True, verbose_name='Могут читать')
    #can_update = models.ManyToManyField(to=User, blank=True, verbose_name='Могут изменять ')
