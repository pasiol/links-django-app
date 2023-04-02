import uuid
from django.db import models


class Link(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=1024, db_index=True, null=False)
    url = models.URLField(max_length=1024, db_index=True, null=False)
    type_choices = [
        ('blog', 'Blog'),
        ('rss', 'RSS'),
        ('podcast', 'Podcast'),
        ('site', 'Site'),
    ]
    type = models.CharField(max_length=10, choices=type_choices, db_index=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def formatted_data(self):
        return f"{self.id}: {self.url}"
