import uuid
from django.db import models


class Link(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=1024, db_index=True, null=False)
    url = models.URLField(max_length=1024, db_index=True, null=False)
    type_choices = [
        ('blog', 'Blog'),
        ('blog-post', 'Blog-post'),
        ('project', 'Project'),
        ('docs', 'Documentation'),
        ('feed', 'Feed'),
        ('podcast', 'Podcast'),
        ('site', 'Site'),
        ('git', 'Git-repo'),
        ('forum', 'Forum'),
        ('forum-post', 'Forum-post'),
        ('video', 'Video'),
    ]
    type = models.CharField(max_length=10, choices=type_choices, db_index=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ('url', 'type',)

    def formatted_data(self):
        return f"{self.id}: {self.url}"
