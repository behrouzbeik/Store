# Generated by Django 4.0.1 on 2022-05-09 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='01.jpg', null=True, upload_to='profile/'),
        ),
    ]
