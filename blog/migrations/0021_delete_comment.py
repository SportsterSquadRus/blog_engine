# Generated by Django 3.1.2 on 2020-10-06 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_auto_20201006_1104'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]