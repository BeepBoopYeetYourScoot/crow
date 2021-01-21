# Generated by Django 3.1.5 on 2021-01-19 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210119_1022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='game',
        ),
        migrations.AddField(
            model_name='profile',
            name='games',
            field=models.ManyToManyField(to='core.Game'),
        ),
    ]
