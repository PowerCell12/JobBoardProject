# Generated by Django 5.0.2 on 2024-03-17 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0015_alter_posts_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='Description',
            field=models.CharField(blank=True, null=True),
        ),
    ]