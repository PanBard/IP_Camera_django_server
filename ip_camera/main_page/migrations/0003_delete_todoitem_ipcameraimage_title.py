# Generated by Django 5.2 on 2025-04-12 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0002_ipcameraimage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ToDoItem',
        ),
        migrations.AddField(
            model_name='ipcameraimage',
            name='title',
            field=models.CharField(default='Default Title', max_length=200),
        ),
    ]
