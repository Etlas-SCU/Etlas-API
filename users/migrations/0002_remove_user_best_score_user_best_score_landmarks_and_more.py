# Generated by Django 4.2.1 on 2023-05-22 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='best_score',
        ),
        migrations.AddField(
            model_name='user',
            name='best_Score_landmarks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='best_score_monuments',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='best_score_statues',
            field=models.IntegerField(default=0),
        ),
    ]
