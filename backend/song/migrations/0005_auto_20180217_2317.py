# Generated by Django 2.0.1 on 2018-02-17 23:17
# pylint: skip-file

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0004_auto_20180217_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songfiles',
            name='song',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files', to='song.Song'),
        ),
    ]
