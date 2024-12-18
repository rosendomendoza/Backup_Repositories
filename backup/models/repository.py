from django.db import models
from .user import User

class Repository(models.Model):
    owner = models.ForeignKey(User, related_name='repositories', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    github_url = models.URLField() 

    def __str__(self):
        return self.name
