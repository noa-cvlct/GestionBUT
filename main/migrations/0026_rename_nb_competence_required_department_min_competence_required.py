# Generated by Django 4.1.1 on 2023-01-26 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_department_min_competence_grade_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='nb_competence_required',
            new_name='min_competence_required',
        ),
    ]
