# Generated by Django 4.2.5 on 2023-10-13 20:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_posts_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 10, 13, 20, 42, 28, 111320)),
        ),
    ]