from typing import ByteString
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE


class UserModel(AbstractUser):
    class Meta:
        db_table = "UserModel"

    self_introduction = models.TextField(default="")
    profile_image = models.ImageField(upload_to="", default="anonymous.png")
    registration = models.IntegerField(default=0)

class TweetModel(models.Model):
    class Meta:
        db_table = "TweetModel"

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

class RetweetModel(models.Model):
    class Meta:
        db_table = "RetweetModel"

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE) # リツイートしたユーザー
    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)


class FollowedUserModel(models.Model): # フォローされたユーザーを表すモデル
    class Meta:
        db_table = "FollowerModel"
    
    followed_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

class FollowModel(models.Model): # フォローという行為を表すモデル
    class Meta:
        db_table = "FollowModel"

    follow_user = models.ForeignKey(UserModel, on_delete=models.CASCADE) # フォローしたユーザー
    followed_user = models.OneToOneField(FollowedUserModel, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

class StarModel(models.Model):
    class Meta:
        db_table = "StarModel"

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE) # スターを押したユーザー
    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

class ImageModel(models.Model):
    class Meta:
        db_table = "ImageModel"

    image = models.ImageField(upload_to="")
    image_name = models.TextField(unique=True)

class CommentModel(models.Model):
    class Meta:
        db_table = "CommentModel"
    
    content = models.TextField()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE) # コメントしたユーザー
    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

class FollowNotificationModel(models.Model):
    class Meta:
        db_table = "FollowNotificationModel"
    
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE) # 通知する対象となるユーザー
    follow = models.OneToOneField(FollowModel, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

class StarNotificationModel(models.Model):
    class Meta:
        db_table = "StarNotificationModel"
    
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    star = models.OneToOneField(StarModel, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

class RetweetNotificationModel(models.Model):
    class Meta:
        db_table = "RetweetNotificationModel"
    
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    retweet = models.OneToOneField(RetweetModel, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    
    
