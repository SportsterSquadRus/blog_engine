from datetime import date
from django.db import models
from django.contrib import auth
from blog.models import Post
from comment.models import Comment



class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    date_birth = models.DateField(verbose_name='День рождения', blank=True, null=True)


    def rating(self, user):
        posts = Post.objects.filter(author = user)
        comments = Comment.objects.filter(author = user)
        func = lambda x: x.total_likes
        rating = sum(map(func, posts)) + sum(map(func, comments)) + posts.count() * 10 + comments.count() * 2

        level = 1
        lvl_min = 0
        lvl_max = 50
        while rating > lvl_max:
            lvl_min, lvl_max = lvl_max, lvl_max + (lvl_max - lvl_min)*2
            level += 1

        part = int(100 * (rating - lvl_min) / (lvl_max - lvl_min))
        return rating, part, lvl_min, lvl_max, level, posts,

    def age(self):
        today = date.today()
        print(self.date_birth)
        # age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))  