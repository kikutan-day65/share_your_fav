# Generated by Django 5.1 on 2024-12-01 11:22

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_location_likes_count_likes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Likes',
            new_name='Like',
        ),
    ]
