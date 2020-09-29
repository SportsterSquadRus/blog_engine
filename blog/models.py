from django.db import models

class Post(models.Model):

    title = models.CharField(verbose_name='Название', max_length=150)
    body = models.TextField(verbose_name='Текст')
    date_pub = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.title

