# Generated by Django 4.1.1 on 2023-01-25 14:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_remove_ue_department_competence_department_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
