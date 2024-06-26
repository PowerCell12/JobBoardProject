# Generated by Django 5.0.2 on 2024-03-09 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0005_moderators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='../static/default_profile_picture.png', upload_to='images/profile_pics'),
        ),
    ]
