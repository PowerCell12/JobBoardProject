# Generated by Django 5.0.2 on 2024-03-19 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0016_alter_posts_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='Description',
            field=models.CharField(blank=True, null=True),
        ),
    ]
