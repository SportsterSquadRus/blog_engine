from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.contrib import auth
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class Like(models.Model):
    user = models.ForeignKey('auth.User', related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Comment(models.Model):
    author = models.ForeignKey('auth.User', related_name='comment', on_delete=models.CASCADE, null=True)
    body = models.TextField(verbose_name='Текст комментярия')
    date_pub = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation(Like)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')


        




class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    body = RichTextField(verbose_name='Текст поста')
    date_pub = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey('auth.User', blank=True, null=True, on_delete=models.CASCADE)
    cover_url = models.URLField(verbose_name='Ссылка на обложку', max_length=300, blank=True, null=True)
    draft_status = models.BooleanField(verbose_name='Черновик', default=False)
    truncate = models.IntegerField(default=0)
    tags = TaggableManager(verbose_name='Теги')
    likes = GenericRelation(Like)
    comments = GenericRelation(Comment)

    @property
    def total_likes(self):
        return self.likes.count()

    # @property
    # def get_content_type(self):
    #     return ContentType.objects.get_for_models(self.__class__)

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




