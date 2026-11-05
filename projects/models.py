from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    deadline = models.DateField(verbose_name="Дедлайн")
    max_participants = models.PositiveIntegerField(verbose_name="Максимум участников")
    current_participants = models.PositiveIntegerField(default=0, verbose_name="Текущее количество")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ['deadline']
