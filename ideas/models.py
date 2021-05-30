from django.db import models

# Create your models here.
class Idea(models.Model):
    description = models.TextField()
    user = models.ForeignKey('users.User', related_name="user_ideas", on_delete=models.CASCADE)
    number_of_likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

