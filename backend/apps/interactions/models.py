from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Create your models here.


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='likes')  # Lazy object with string model
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']


class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="following", on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="followers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("follower", "following")
        ordering = ["-created_at"]
        # Constraint to prevent self follow on database level
        constraints = [
            models.CheckConstraint(
                # Object needed to negate it with ~, constraint doesn't accept other symbols than =
                condition=~models.Q(follower=models.F("following")),    # models.F checks value in column 'following' for the same row
                name="prevent_self_follow"
            )
        ]
        
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
    
    def clean(self):
        if self.follower == self.following:
            raise ValidationError("You can't follow yourself!")
