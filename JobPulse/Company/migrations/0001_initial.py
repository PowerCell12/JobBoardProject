# Generated by Django 5.0.2 on 2024-03-06 18:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50, unique=True)),
                ('CompanyImage', models.URLField(null=True)),
                ('Description', models.CharField(blank=True, max_length=255, null=True)),
                ('Address', models.CharField(blank=True, max_length=255, null=True)),
                ('CompanyEmail', models.EmailField(max_length=254, null=True)),
                ('Owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('JobName', models.CharField(max_length=50)),
                ('Salary', models.CharField(blank=True, max_length=255, null=True)),
                ('CompanyFK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Company.company')),
            ],
        ),
    ]