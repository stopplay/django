# Generated by Django 4.1.4 on 2023-11-22 03:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatgbt', '0004_remove_video_name_video_title_alter_video_segment_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='segment',
            new_name='segments',
        ),
    ]