from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import FollowNotificationModel, RetweetNotificationModel, StarNotificationModel, UserModel, TweetModel, RetweetModel, FollowModel, FollowedUserModel, StarModel, ImageModel, CommentModel

from urllib.parse import urlencode
import re

def authentication(request):
    if request.user.is_authenticated:
        authentication = True
    else:
        authentication = False
    
    return authentication
