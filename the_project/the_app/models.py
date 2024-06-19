from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    """Model for tasks."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def is_expired(self):
        """Method is needed to check if the task is expired."""
        return self.date < timezone.now() and not self.completed


class Post(models.Model):
    """Model for the bulletin board posts."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Model for comment"""
    post = models.ForeignKey(Post, related_name='comments',
                             on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
