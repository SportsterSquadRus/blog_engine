# Generated by Django 3.1.2 on 2020-10-10 14:20

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('body', ckeditor.fields.RichTextField(verbose_name='Текст поста')),
                ('date_pub', models.DateTimeField(blank=True, null=True)),
                ('cover_url', models.URLField(blank=True, max_length=300, null=True, verbose_name='Ссылка на обложку')),
                ('draft_status', models.BooleanField(default=False, verbose_name='Черновик')),
                ('truncate', models.IntegerField(default=0)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_pub'],
            },
        ),
    ]
