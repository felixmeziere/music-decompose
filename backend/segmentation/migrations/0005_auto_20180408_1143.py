# Generated by Django 2.0.1 on 2018-04-08 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0004_auto_20180408_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='segment',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='segments', to='segmentation.Segmenter'),
        ),
    ]
