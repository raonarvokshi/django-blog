# Generated by Django 4.2.5 on 2023-10-14 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_remove_posts_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='likes',
        ),
    ]
