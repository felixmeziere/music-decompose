# Generated by Django 2.0.1 on 2018-04-02 20:51
# pylint: skip-file
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0002_auto_20180402_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='segment',
            name='ind',
            field=models.PositiveIntegerField(verbose_name='Index'),
        ),
    ]
