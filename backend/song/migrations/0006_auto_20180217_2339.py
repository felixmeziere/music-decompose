# Generated by Django 2.0.1 on 2018-02-17 23:39
# pylint: skip-file

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0005_auto_20180217_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songfiles',
            name='song',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='song.Song'),
            preserve_default=False,
        ),
    ]
