# Generated by Django 3.1.5 on 2021-01-19 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20210119_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='Баланс'),
        ),
    ]
