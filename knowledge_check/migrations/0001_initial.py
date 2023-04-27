# Generated by Django 4.1.7 on 2023-04-13 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.CharField(max_length=200)),
                ('label', models.CharField(choices=[('statue', 'statue'), ('monument', 'monument'), ('landmark', 'landmark')], max_length=200)),
                ('image', models.ImageField(upload_to='questions_images/')),
                ('correct_chocie', models.CharField(max_length=200)),
                ('choices', models.ManyToManyField(related_name='choices', to='knowledge_check.choice')),
            ],
        ),
    ]