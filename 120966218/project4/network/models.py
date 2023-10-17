from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField("User",on_delete=models.CASCADE)
    followers = models.ManyToManyField("User",related_name="follows", blank=True)
    follows = models.ManyToManyField("User",related_name="followers", blank=True)
    like = models.ManyToManyField("Post", related_name="like", blank=True)


# Need to add model for posts, like, followers 
class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    liked = models.ManyToManyField("User", related_name="liked", blank=True)
    liked_by_user = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} {self.poster} {self.body} {self.timestamp} {self.likes} {self.liked}"
