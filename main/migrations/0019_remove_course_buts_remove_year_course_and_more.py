# Generated by Django 4.1.1 on 2022-12-29 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_ue_department_alter_professor_resources_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='BUTs',
        ),
        migrations.RemoveField(
            model_name='year',
            name='course',
        ),
        migrations.RemoveField(
            model_name='year',
            name='first_semester',
        ),
        migrations.RemoveField(
            model_name='year',
            name='second_semester',
        ),
        migrations.RemoveField(
            model_name='group',
            name='year',
        ),
        migrations.AlterField(
            model_name='grade',
            name='note',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.DeleteModel(
            name='BUT',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='Year',
        ),
    ]