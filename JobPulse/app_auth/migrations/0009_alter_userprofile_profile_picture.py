# Generated by Django 5.0.2 on 2024-03-10 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0008_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='/default_profile_picture.png', upload_to='images/profile_pics/'),
        ),
    ]