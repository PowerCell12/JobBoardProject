# Generated by Django 5.0.2 on 2024-03-14 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0009_alter_company_companyimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='Seniority',
            field=models.CharField(blank=True, choices=[('Team Lead', 'Team Lead'), ('Senior', 'Senior'), ('Mid-Level', 'Mid-Level'), ('Junior/Intern', 'Junior/Intern')], null=True),
        ),
    ]
