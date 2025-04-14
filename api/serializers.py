from rest_framework import serializers
from .models import User, Post, Comment, Like, Follow

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'date_joined'] # Include fields you want to expose in API
        read_only_fields = ['id', 'date_joined'] # Fields that should not be updated directly via API


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # Nested serializer to represent the post creator
    likes_count = serializers.SerializerMethodField() # Field to display the count of likes
    comments_count = serializers.SerializerMethodField() # Field to display the count of comments

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'created_at', 'updated_at', 'likes_count', 'comments_count']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'likes_count', 'comments_count']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # Nested serializer for comment author

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'post', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # Nested serializer for user who liked
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all()) # Use PrimaryKeyRelatedField for Post to avoid full nested representation

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True) # Nested serializer for follower
    following = UserSerializer(read_only=True) # Nested serializer for user being followed

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']
        read_only_fields = ['id', 'follower', 'following', 'created_at']