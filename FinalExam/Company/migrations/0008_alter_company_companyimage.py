# Generated by Django 5.0.2 on 2024-03-12 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0007_alter_posts_moderator_alter_posts_recruiter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='CompanyImage',
            field=models.ImageField(default='/default_company_image', upload_to='images/company_pics/'),
        ),
    ]
