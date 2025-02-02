# Generated by Django 4.1.4 on 2023-11-22 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chatgbt', '0005_rename_segment_video_segments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='segmentimage',
            name='segment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='chatgbt.segment'),
        ),
        migrations.AlterField(
            model_name='video',
            name='segments',
            field=models.ManyToManyField(blank=True, related_name='videos', to='chatgbt.segment'),
        ),
    ]
