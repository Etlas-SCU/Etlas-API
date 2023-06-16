# Generated by Django 4.2.1 on 2023-05-25 19:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('monuments', '0004_alter_articlemonument_article_and_more'),
        ('articles', '0003_alter_article_options_article_created_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article',
                                   to='articles.article')),
                ('monument',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='monument',
                                   to='monuments.monument')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('user', 'monument', 'article')},
            },
        ),
    ]
