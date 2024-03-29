# Generated by Django 4.2.1 on 2023-05-11 20:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryTimeline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeline_name', models.CharField(max_length=200)),
                ('timeline_start', models.IntegerField(default=float("-inf"))),
                ('timeline_end', models.IntegerField(default=float("inf"))),
                ('timeline_description', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Era',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('era_name', models.CharField(max_length=200)),
                ('era_start', models.IntegerField(default=float("-inf"))),
                ('era_end', models.IntegerField(default=float("inf"))),
                ('era_description', models.TextField(default='')),
                ('image', models.ImageField(blank=True, null=True, upload_to='era_images')),
                ('history_timeline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eras',
                                                       to='timeline.historytimeline')),
            ],
        ),
    ]
