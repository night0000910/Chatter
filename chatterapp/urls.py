from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import signupview, loginview, tweetsview, star_tweetsview, my_tweetsview, detailview, starview, retweetview, commentview, open_formview, followview, tweetview, logoutview, followingview, followerview, profile_image_registraionview, self_introduction_registrationview, profileview, notificationview, searchview, star_userview, retweet_userview


urlpatterns = [
    path("signup/", signupview, name="signup"),
    path("login/", loginview, name="login"),
    path("logout/", logoutview, name="logout"),
    path("tweets/<int:user_id>/", tweetsview, name="tweets"),
    path("star_tweets/<int:user_id>/", star_tweetsview, name="star_tweets"),
    path("my_tweets/", my_tweetsview, name="my_tweets"),
    path("detail/<int:tweet_id>/", detailview, name="detail"),
    path("star/<int:tweet_id>/", starview, name="star"),
    path("retweet/<int:tweet_id>/", retweetview, name="retweet"),
    path("comment/<int:tweet_id>/", commentview, name="comment"),
    path("openform/<int:tweet_id>/<int:open>/", open_formview, name="open_form"),
    path("follow/<int:user_id>/<int:redirect_token>/", followview, name="follow"),
    path("tweet/", tweetview, name="tweet"),
    path("following/<int:user_id>/", followingview, name="following"),
    path("follower/<int:user_id>/", followerview, name="follower"),
    path("profile_image_registration/", profile_image_registraionview, name="profile_image_registration"),
    path("self_introduction_registration/", self_introduction_registrationview, name="self_introduction_registration"),
    path("profile/", profileview, name="profile"),
    path("notification/", notificationview, name="notification"),
    path("search/<str:token>/", searchview, name="search"),
    path("star_user/<int:tweet_id>/", star_userview, name="star_user"),
    path("retweet_user/<int:tweet_id>/", retweet_userview, name="retweet_user"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)