# Generated by Django 4.0.2 on 2022-04-18 12:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0017_alter_commnet_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='commnet',
            name='comment_like',
            field=models.ManyToManyField(blank=True, null=True, related_name='com_like', to=settings.AUTH_USER_MODEL),
        ),
    ]