# Generated by Django 4.2.1 on 2023-05-15 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monuments', '0001_initial'),
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='monuments',
            field=models.ManyToManyField(blank=True, related_name='articles', to='monuments.monument'),
        ),
    ]
