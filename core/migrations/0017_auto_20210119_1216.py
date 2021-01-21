# Generated by Django 3.1.5 on 2021-01-19 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20210119_1115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamesetting',
            name='game',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='games',
        ),
        migrations.RemoveField(
            model_name='step',
            name='game',
        ),
        migrations.AddField(
            model_name='game',
            name='settings',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='settings', to='core.gamesetting'),
        ),
        migrations.AddField(
            model_name='game',
            name='step',
            field=models.ManyToManyField(related_name='step', to='core.Step'),
        ),
        migrations.AddField(
            model_name='game',
            name='user',
            field=models.ManyToManyField(related_name='profile', to='core.Profile', verbose_name='Профиль игрока'),
        ),
    ]
