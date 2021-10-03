from django.contrib import admin
from .models import UserModel, TweetModel, RetweetModel, FollowModel, FollowedUserModel, StarModel, ImageModel, CommentModel, FollowNotificationModel, StarNotificationModel, RetweetNotificationModel



admin.site.register(UserModel)
admin.site.register(TweetModel)
admin.site.register(RetweetModel)
admin.site.register(FollowModel)
admin.site.register(FollowedUserModel)
admin.site.register(StarModel)
admin.site.register(ImageModel)
admin.site.register(CommentModel)
admin.site.register(FollowNotificationModel)
admin.site.register(StarNotificationModel)
admin.site.register(RetweetNotificationModel)