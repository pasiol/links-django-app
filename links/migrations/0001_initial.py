# Generated by Django 4.0.10 on 2023-04-01 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('description', models.TextField(db_index=True, max_length=1024)),
                ('url', models.URLField(db_index=True, max_length=1024)),
                ('type', models.CharField(choices=[('blog', 'Blog'), ('rss', 'RSS'), ('podcast', 'Podcast'), ('site', 'Site')], db_index=True, max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
