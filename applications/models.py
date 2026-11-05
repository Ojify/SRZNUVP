from django.db import models
from projects.models import Project
from users.models import User

class Status(models.Model):
    code = models.CharField(max_length=50, primary_key=True, verbose_name="Код")
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

class Application(models.Model):
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='applications',
        verbose_name="Проект"
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='applications',
        verbose_name="Пользователь"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.ForeignKey(
        Status, 
        on_delete=models.PROTECT, 
        related_name='applications',
        verbose_name="Статус"
    )

    def __str__(self):
        return f"Заявка №{self.pk}: {self.user.name} -> {self.project.name}"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_at']
