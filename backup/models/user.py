from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    github_url = models.URLField()

    def __str__(self):
        return self.username
