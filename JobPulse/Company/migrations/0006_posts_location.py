# Generated by Django 5.0.2 on 2024-03-12 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0005_posts_moderator_alter_posts_recruiter'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='Location',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
