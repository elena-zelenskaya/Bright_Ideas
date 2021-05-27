from django.db import models
from users.models import User

# Create your models here.
class Idea(models.Model):
    description = models.TextField()
    user = models.ForeignKey(User, related_name="ideas", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
