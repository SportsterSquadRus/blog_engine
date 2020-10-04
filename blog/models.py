from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.contrib import auth
from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    body = models.TextField(verbose_name='Текст')
    date_pub = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey('auth.User', blank=True, null=True, on_delete=models.CASCADE)
    cover_url = models.URLField(verbose_name='Ссылка на обложку', max_length=300, blank=True, null=True)
    draft_status = models.BooleanField(verbose_name='Черновик', default=False)
    truncate = models.IntegerField(default=0)
    tags = TaggableManager(verbose_name='Теги')
    likes = models.ManyToManyField(auth.models.User, related_name='blog_posts')

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_pub']
