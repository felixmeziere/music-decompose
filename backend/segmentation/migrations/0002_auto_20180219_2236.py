# Generated by Django 2.0.1 on 2018-02-19 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0007_song_tempo'),
        ('segmentation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='segmentlist',
            name='method',
            field=models.CharField(choices=[('blind', 'Blind'), ('flexible', 'Flexible')], default='blind', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='segment',
            name='audio_file',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='segmentlist',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='segment_lists', to='song.Song'),
        ),
        migrations.AlterUniqueTogether(
            name='segment',
            unique_together={('index', 'segment_list')},
        ),
        migrations.AlterUniqueTogether(
            name='segmentlist',
            unique_together={('song', 'method')},
        ),
    ]