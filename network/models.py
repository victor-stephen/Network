from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userPoster")
    post = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default='0')

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "post": self.post,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "like": self.like
        }

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")
    following = models.ManyToManyField(User, blank=True, related_name="followers")

    def __str__(self):
        return (f"{self.user} is following {self.following.all()[0]}")
