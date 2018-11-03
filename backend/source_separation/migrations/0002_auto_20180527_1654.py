# pylint: skip-file

# Generated by Django 2.0.1 on 2018-05-27 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0001_initial'),
        ('source_separation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='segmentgrouper',
            name='hop_length',
            field=models.PositiveIntegerField(default=256),
        ),
        migrations.AddField(
            model_name='segmentgrouper',
            name='n_fft',
            field=models.PositiveIntegerField(default=1024),
        ),
        migrations.AddField(
            model_name='segmentgrouper',
            name='win_length',
            field=models.PositiveIntegerField(default=1024),
        ),
        migrations.AlterUniqueTogether(
            name='segmentgrouper',
            unique_together={('parent', 'method', 'n_fft', 'hop_length', 'win_length')},
        ),
    ]
