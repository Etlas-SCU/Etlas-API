# Generated by Django 4.2.1 on 2023-07-01 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monuments', '0005_alter_monument_options_monument_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='monument',
            name='model_obj',
            field=models.FileField(blank=True, help_text='Upload a .obj file', null=True, upload_to='monuments_obj/', verbose_name='Model'),
        ),
        migrations.AddField(
            model_name='monument',
            name='model_texture',
            field=models.ImageField(blank=True, help_text='Upload a .png file', null=True, upload_to='monuments_images/', verbose_name='Texture'),
        ),
    ]
