# Generated by Django 5.0.2 on 2024-03-21 22:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0024_remove_jobapplication_application_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='PostFk',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Company.posts'),
            preserve_default=False,
        ),
    ]
