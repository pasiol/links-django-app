# Generated by Django 4.0.10 on 2023-04-07 07:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='link',
            name='type',
            field=models.CharField(choices=[('blog', 'Blog'), ('project', 'Project'), ('rss', 'RSS'), ('podcast', 'Podcast'), ('site', 'Site')], db_index=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='link',
            name='url',
            field=models.URLField(db_index=True, max_length=1024, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='link',
            unique_together={('url', 'type')},
        ),
    ]
