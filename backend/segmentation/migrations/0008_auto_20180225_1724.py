# Generated by Django 2.0.1 on 2018-02-25 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0007_auto_20180222_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='segmentlist',
            name='segmentation_status',
            field=models.CharField(choices=[('not_started', 'Not started'), ('pending', 'Pending...'), ('failed', 'Failed'), ('done', 'Done')], default='not_started', max_length=15),
        ),
    ]
