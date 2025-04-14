from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model extending AbstractUser to include 'bio' and 'is_active' fields.
    """
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)  # For soft deletion, if needed

    def __str__(self):
        return self.username


class Post(models.Model):
    """
    Model representing a user post.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"


class Comment(models.Model):
    """
    Model representing a comment on a post.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on Post {self.post.id}"


class Like(models.Model):
    """
    Model representing a like on a post.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post') # Ensure a user can like a post only once

    def __str__(self):
        return f"Like by {self.user.username} on Post {self.post.id}"


class Follow(models.Model):
    """
    Model representing the follow relationship between users.
    """
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_relations')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_relations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following') # Ensure a user can follow another user only once

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"