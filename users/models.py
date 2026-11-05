from django.db import models

class User(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    skills = models.CharField(max_length=255, blank=True, verbose_name="Навыки")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['name']
