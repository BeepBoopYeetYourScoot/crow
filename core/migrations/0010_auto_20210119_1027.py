# Generated by Django 3.1.5 on 2021-01-19 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20210119_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='games',
            field=models.ManyToManyField(to='core.Game'),
        ),
    ]
