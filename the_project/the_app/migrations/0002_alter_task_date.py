# Generated by Django 5.0.6 on 2024-06-13 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateTimeField(),
        ),
    ]