# Generated by Django 4.1.4 on 2023-04-24 17:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QRCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=255, null=True)),
                ('source', models.CharField(max_length=255, null=True)),
                ('brand', models.CharField(max_length=255, null=True)),
                ('gtin', models.CharField(max_length=255, null=True)),
                ('pixel', models.CharField(max_length=255, null=True)),
                ('qr_code_link', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScanEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('qr_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qrflogi.qrcode')),
            ],
        ),
    ]
