from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import FollowNotificationModel, RetweetNotificationModel, StarNotificationModel, UserModel, TweetModel, RetweetModel, FollowModel, FollowedUserModel, StarModel, ImageModel, CommentModel

from urllib.parse import urlencode
import re

from .function import authentication


def signupview(request):
    if request.method == "GET":
        if request.GET.get("error"):
            error = request.GET.get("error")
        else:
            error = ""

        return render(request, "signup.html", {"error" : error, "authentication" : authentication(request)})

    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        username_set = UserModel.objects.all()
        username_duplicate = False

        for value in username_set:
            if username == value.username:
                username_duplicate = True
        
        if not username_duplicate:
            get_user_model().objects.create_user(username, "", password)
            return redirect("login")
        else:
            redirect_url = reverse("signup")
            parameters = urlencode({"error" : "サインアップに失敗しました"})
            url = f"{redirect_url}?{parameters}"
            return redirect(url)

def loginview(request):
    if request.method == "GET":
        if request.GET.get("error"):
            error = request.GET.get("error")
        else:
            error = ""

        return render(request, "login.html", {"error" : error, "authentication" : authentication(request)})
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("my_tweets")
        else:
            redirect_url = reverse("login")
            parameters = urlencode({"error" : "ログインに失敗しました"})
            url = f"{redirect_url}?{parameters}"
            return redirect(url)

def logoutview(request):
    logout(request)
    return redirect("login")

def tweetsview(request, user_id):
    if request.user.is_authenticated:
        if request.user.registration == 0:
            return redirect("profile_image_registration")
        elif request.user.registration == 1:
            return redirect("self_introduction_registration")

    user = get_user_model().objects.get(id=user_id)
    tweet_set = TweetModel.objects.filter(user=user_id)
    retweet_set = RetweetModel.objects.filter(user=user_id)
    tweet_list = []

    for tweet in tweet_set:
        tweet_list.append(tweet)
    
    if request.user.is_authenticated:
        if user_id == request.user.id:
            follow_set = FollowModel.objects.filter(follow_user=request.user.id)

            for follow in follow_set:

                followed_user = follow.followed_user.followed_user

                for tweet in followed_user.tweetmodel_set.all():
                    tweet_list.append(tweet)

    for retweet in retweet_set:
        tweet_duplicate = False

        for tweet in tweet_list:

            if retweet.tweet == tweet:
                tweet_duplicate = True

                if retweet.datetime >= tweet.datetime:
                    tweet_list.remove(tweet)
                    tweet_list.append(retweet)
        
        if tweet_duplicate:
            break

        tweet_list.append(retweet)    

    tweet_list.sort(key=lambda x:x.datetime.timestamp())
    tweet_list.reverse()

    follow_set = FollowModel.objects.filter(follow_user=user_id)
    follow_number = 0

    for follow in follow_set:
        follow_number += 1
    
    followed_user_set = FollowedUserModel.objects.filter(followed_user=user_id)
    followed_user_number = 0

    for follower in followed_user_set:
        followed_user_number += 1

    if request.user.is_authenticated:
        followed_user_set = FollowedUserModel.objects.filter(followed_user=user_id)
        follow_set = FollowModel.objects.filter(follow_user=request.user.id)
        follow_existence = False

        for follow in follow_set:
            for followed_user in followed_user_set:
                if follow.followed_user == followed_user:
                    followed_user = followed_user
                    follow_existence = True
    
    else:
        follow_existence = False
    
    redirect_token = 1

    if request.user.is_authenticated:
        login_user_id = request.user.id
    else:
        login_user_id = -1
    
    url = reverse("search", kwargs={"token" : "tweet"})

    return render(request, "tweets.html", {"user" : user, "login_user_id" : login_user_id, "tweet_list" : tweet_list, "follow_number" : follow_number, "followed_user_number" : followed_user_number, "redirect_token" : redirect_token, "follow_existence" : follow_existence, "url" : url, "authentication" : authentication(request), "keyword" : ""})

def star_tweetsview(request, user_id):
    if request.user.is_authenticated:
        if request.user.registration == 0:
            return redirect("profile_image_registration")
        elif request.user.registration == 1:
            return redirect("self_introduction_registration")

    user = get_user_model().objects.get(id=user_id)
    star_set = StarModel.objects.filter(user=user_id)
    star_list = []

    for star in star_set:
        star_list.append(star)
    
    star_list.sort(key=lambda x:x.datetime.timestamp())
    star_list.reverse()

    follow_set = FollowModel.objects.filter(follow_user=user_id)
    follow_number = 0

    for follow in follow_set:
        follow_number += 1
    
    followed_user_set = FollowedUserModel.objects.filter(followed_user=user_id)
    followed_user_number = 0

    for follower in followed_user_set:
        followed_user_number += 1

    if request.user.is_authenticated:
        followed_user_set = FollowedUserModel.objects.filter(followed_user=user_id)
        follow_set = FollowModel.objects.filter(follow_user=request.user.id)
        follow_existence = False

        for follow in follow_set:
            for followed_user in followed_user_set:
                if follow.followed_user == followed_user:
                    followed_user = followed_user
                    follow_existence = True
    
    else:
        follow_existence = False
    
    redirect_token = 2

    if request.user.is_authenticated:
        login_user_id = request.user.id
    else:
        login_user_id = -1
    
    url = reverse("search", kwargs={"token" : "tweet"})

    return render(request, "stars.html", {"user" : user, "login_user_id" : login_user_id, "star_list" : star_list, "follow_number" : follow_number, "followed_user_number" : followed_user_number, "redirect_token" : redirect_token, "follow_existence" : follow_existence, "url" : url, "authentication" : authentication(request)})


def my_tweetsview(request):
    if request.user.is_authenticated:
        return redirect("tweets", user_id=request.user.id)
    else:
        return redirect("login")

def detailview(request, tweet_id):
    if request.user.is_authenticated:
        if request.user.registration == 0:
            return redirect("profile_image_registration")
        elif request.user.registration == 1:
            return redirect("self_introduction_registration")

    tweet = TweetModel.objects.get(id=tweet_id)
    star_set = StarModel.objects.filter(tweet=tweet_id)
    star_number = 0

    for star in star_set:
        star_number += 1
    
    retweet_set = RetweetModel.objects.filter(tweet=tweet_id)
    retweet_number = 0

    for retweet in retweet_set:
        retweet_number += 1
    
    comment_set = CommentModel.objects.filter(tweet=tweet_id)
    comment_list = []
    
    for comment in comment_set:
        comment_list.append(comment)
    
    comment_list.sort(key=lambda x:x.datetime.timestamp())
    comment_list.reverse()
    
    comment_number = len(comment_list)

    if request.user.is_authenticated:
        star_set = StarModel.objects.filter(tweet=tweet_id).filter(user=request.user.id)
        star = None

        for value in star_set:
            star = value
            
        if star is None:
            star_existence = False
        else:
            star_existence = True
        
        retweet_set = RetweetModel.objects.filter(tweet=tweet_id).filter(user=request.user.id)
        retweet = None

        for value in retweet_set:
            retweet = value
        
        if retweet is None:
            retweet_existence = False
        else:
            retweet_existence = True
    
    else:
        star_existence = False
        retweet_existence = False

    star_image = ImageModel.objects.get(image_name="star")
    retweet_image = ImageModel.objects.get(image_name="retweet")
    comment_image = ImageModel.objects.get(image_name="comment")

    comment_url = reverse("comment", kwargs={"tweet_id" : tweet_id})

    # comment_urlにはきちんと値が格納されている

    open = 0

    if request.GET.get("open"):
        open = int(request.GET.get("open"))
    
    # openにはきちんと値が格納されている

    return render(request, "detail.html", {"tweet" : tweet, "comment_list" : comment_list, "comment_number" : comment_number, "star_number" : star_number, "retweet_number" : retweet_number,"star_existence" : star_existence, "retweet_existence" : retweet_existence, "star_image" : star_image, "retweet_image" : retweet_image, "comment_image" : comment_image, "comment_url" : comment_url, "open" : open, "authentication" : authentication(request)})

def starview(request, tweet_id):
    if request.user.is_authenticated:
        if request.user.registration == 0:
            return redirect("profile_image_registration")
        elif request.user.registration == 1:
            return redirect("self_introduction_registration")

    if request.user.is_authenticated:
        tweet = TweetModel.objects.get(id=tweet_id)
        star_set = StarModel.objects.filter(tweet=tweet_id).filter(user=request.user.id)
        star = None

        for value in star_set:
            star = value
        
        if star is None:
            star = StarModel.objects.create(user=request.user, tweet=tweet)
            
            # 通知
            StarNotificationModel.objects.create(user=tweet.user, star=star)
        else:
            star.delete()
        
        return redirect("detail", tweet_id=tweet_id)

    else:
        return redirect("login")

def retweetview(request, tweet_id):
    if request.user.is_authenticated:
        if request.user.registration == 0:
            return redirect("profile_image_registration")
        elif request.user.registration == 1:
            return redirect("self_introduction_registration")

    if request.user.is_authenticated:
        tweet = TweetModel.objects.get(id=tweet_id)
        retweet_set = RetweetModel.objects.filter(tweet=tweet_id).filter(user=request.user.id)
        retweet = None

        for value in retweet_set:
            retweet = value
        
        if retweet is None:
            retweet = RetweetModel.objects.create(user=request.user, tweet=tweet)

            # 通知
            RetweetNotificationModel.objects.create(user=tweet.user, retweet=retweet)
        else:
            retweet.delete()
        
        return redirect("detail", tweet_id=tweet_id)

    else:
        return redirect("login")

def commentview(request, tweet_id):
    if request.user.is_authenticated:
        if request.user.registration == 0:
            return redirect("profile_image_registration")
        elif request.user.registration == 1:
            return redirect("self_introduction_registration")

    if request.user.is_authenticated:
        tweet = TweetModel.objects.get(id=tweet_id)
        content = request.POST["comment"]
        CommentModel.objects.create(content=content, user=request.user, tweet=tweet)
        return redirect("detail", tweet_id=tweet_id)
    else:
        return redirect("login")

def open_formview(request, tweet_id, open):
    if request.user.is_authenticated:
        if request.user.registration == 0:
            return redirect("profile_image_registration")
        elif request.user.registration == 1:
            return redirect("self_introduction_registration")

    if request.user.is_authenticated:
        if open == 0:
            open += 1
        elif open == 1:
            open -= 1
        
        redirect_url = reverse("detail", kwargs={"tweet_id" : tweet_id})
        parameters = urlencode({"open" : open})
        url = f"{redirect_url}?{parameters}"
        return redirect(url)
    else:
        return redirect("login")

def followview(request, user_id, redirect_token): # user_idは、フォローされたユーザーのidを表す
    if request.user.is_authenticated:
        if request.user.registration == 0:
            return redirect("profile_image_registration")
        elif request.user.registration == 1:
            return redirect("self_introduction_registration")

    if request.user.is_authenticated:
        followed_user_set = FollowedUserModel.objects.filter(followed_user=user_id)
        follow_set = FollowModel.objects.filter(follow_user=request.user.id)
        existence = False

        for follow in follow_set:
            for followed_user in followed_user_set:
                if follow.followed_user == followed_user:
                    followed_user = followed_user
                    existence = True
                    print(followed_user)

        if existence:
            followed_user.delete()
        else:
            follow_user = request.user
            followed_user = UserModel.objects.get(id=user_id)
            followed_user = FollowedUserModel.objects.create(followed_user=followed_user)
            follow = FollowModel.objects.create(follow_user=follow_user, followed_user=followed_user)

            # 通知
            FollowNotificationModel.objects.create(user=follow.followed_user.followed_user, follow=follow)
        
        if redirect_token == 1:
            return redirect("tweets", user_id=user_id)
        elif redirect_token == 2:
            return redirect("star_tweets", user_id=user_id)

        
    else:
        return redirect("login")

def tweetview(request):
    if request.user.is_authenticated:
        if request.user.registration == 0:
            return redirect("profile_image_registration")
        elif request.user.registration == 1:
            return redirect("self_introduction_registration")

    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "tweet.html", {"login_user" : request.user, "authentication" : authentication(request)})
        elif request.method == "POST":
            content = request.POST["content"]
            TweetModel.objects.create(user=request.user, content=content)
            return redirect("my_tweets")
    else:
        return redirect("login")

def followingview(request, user_id): # フォローしているユーザーを表示するためのビュー
    if request.user.is_authenticated:
        if request.user.registration == 0:
            return redirect("profile_image_registration")
        elif request.user.registration == 1:
            return redirect("self_introduction_registration")

    user = UserModel.objects.get(id=user_id)
    follow_set = FollowModel.objects.filter(follow_user=user_id)
    follow_list = []

    for follow in follow_set:
        follow_list.append(follow)
    
    follow_list.sort(key=lambda x:x.datetime.timestamp())
    follow_list.reverse()

    url = reverse("search", kwargs={"token" : "tweet"})

    return render(request, "following.html", {"user" : user, "follow_list" : follow_list, "url" : url, "authentication" : authentication(request)})

def followerview(request, user_id): # フォロワーを表示するためのビュー
    if request.user.is_authenticated:
        if request.user.registration == 0:
            return redirect("profile_image_registration")
        elif request.user.registration == 1:
            return redirect("self_introduction_registration")

    user = UserModel.objects.get(id=user_id)
    followed_user_set = FollowedUserModel.objects.filter(followed_user=user_id)
    follow_list = []

    
    for followed_user in followed_user_set:
        follow_set = FollowModel.objects.filter(followed_user=followed_user)

        for follow in follow_set:
            follow_list.append(follow)
    
    follow_list.sort(key=lambda x:x.datetime.timestamp())
    follow_list.reverse()

    url = reverse("search", kwargs={"token" : "tweet"})

    return render(request, "follower.html", {"user" : user, "follow_list" : follow_list, "url" : url, "authentication" : authentication(request)})

def profile_image_registraionview(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "profile_image_registration.html", {"user" : request.user, "authentication" : authentication(request)})
        elif request.method == "POST":
            if request.FILES:
                profile_image = request.FILES["profile_image"]
                user = get_user_model().objects.get(id=request.user.id)
                user.profile_image = profile_image
                user.save()
                return redirect("profile_image_registration")
            else:
                return redirect("profile_image_registration")
    else:
        return redirect("login")

def self_introduction_registrationview(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            user = get_user_model().objects.get(id=request.user.id)
            user.registration = 1
            user.save()
            return render(request, "self_introduction_registration.html", {"authentication" : authentication(request)})
        elif request.method == "POST":
            if request.POST["self_introduction"]:
                self_introduction = request.POST["self_introduction"]
            else:
                self_introduction = ""
            
            user = get_user_model().objects.get(id=request.user.id)
            user.self_introduction = self_introduction
            user.registration = 2
            user.save()

            return redirect("my_tweets")
    else:
        return redirect("login")

def profileview(request):
    if request.user.is_authenticated:
        if request.user.registration == 0:
            return redirect("profile_image_registration")
        elif request.user.registration == 1:
            return redirect("self_introduction_registration")
    
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "profile.html", {"user" : request.user, "authentication" : authentication(request)})
        elif request.method == "POST":

            if request.POST["token"] == "profile_image":
                user = request.user
                if request.FILES:
                    profile_image = request.FILES["profile_image"]
                    user.profile_image = profile_image
                    user.save()
                
                return redirect("profile")

            elif request.POST["token"] == "self_introduction":
                
                if request.POST["self_introduction"]:
                    self_introduction = request.POST["self_introduction"]
                else:
                    self_introduction = ""
                
                user = request.user
                user.self_introduction = self_introduction
                user.save()
                return redirect("profile")
                   
    else:
        return redirect("login")

def notificationview(request):
    if request.user.is_authenticated:
        if request.user.registration == 0:
            return redirect("profile_image_registration")
        elif request.user.registration == 1:
            return redirect("self_introduction_registration")
    
    if request.user.is_authenticated:
        user = request.user
        star_notification_set = StarNotificationModel.objects.filter(user=user)
        retweet_notification_set = RetweetNotificationModel.objects.filter(user=user)
        follow_notification_set = FollowNotificationModel.objects.filter(user=user)
        notification_list = []

        for notification in star_notification_set:
            notification_list.append(notification)
        
        for notification in retweet_notification_set:
            notification_list.append(notification)
        
        for notification in follow_notification_set:
            notification_list.append(notification)

        notification_list.sort(key=lambda x:x.datetime.timestamp())
        notification_list.reverse()

        url = reverse("search", kwargs={"token" : "tweet"})

        return render(request, "notification.html", {"user" : user, "notification_list" : notification_list, "url" : url, "authentication" : authentication(request)})

    else:
        return redirect("login")
    
def searchview(request, token):
    if request.user.is_authenticated:
        if request.user.registration == 0:
            return redirect("profile_image_registration")
        elif request.user.registration == 1:
            return redirect("self_introduction_registration")
    
    if request.POST["keyword"]:
        keyword = request.POST["keyword"]
    else:
        keyword = ""

    url = reverse("search", kwargs={"token" : "tweet"})

    user_url = reverse("search", kwargs={"token" : "user"})

    # user_urlにはきちんと値が格納されている

    if keyword.startswith("#"): # ハッシュタグかどうかを判定
        if token == "tweet":
            f_pattern = re.compile(fr"{keyword}[\n\t\s]")
            s_pattern = re.compile(fr"{keyword}$")
            tweet_set = TweetModel.objects.all()
            tweet_list = []

            for tweet in tweet_set:
                if f_pattern.search(tweet.content):
                    tweet_list.append(tweet)
                elif s_pattern.search(tweet.content):
                    tweet_list.append(tweet)
            
            tweet_list.sort(key=lambda x:x.datetime.timestamp())
            tweet_list.reverse()
            print(tweet_list)

            return render(request, "search.html", {"keyword" : keyword, "tweet_list" : tweet_list, "url" : url, "token" : token, "user_url" : user_url, "authentication" : authentication(request)})

        elif token == "user":
            user_list = []
            return render(request, "search.html", {"keyword" : keyword, "user_list" : user_list, "url" : url, "token" : token, "user_url" : user_url, "authentication" : authentication(request)})

    else:

        if token == "tweet": # ツイートの検索か、ユーザーの検索かを判別
            tweet_set = TweetModel.objects.all()
            user_set = UserModel.objects.all()
            tweet_list = []
            user_list = []
            
            for user in user_set:
                if keyword in user.username:
                    user_list.append(user)

            for tweet in tweet_set:
                if keyword in tweet.content:
                    tweet_list.append(tweet)
                else:

                    for user in user_list:
                        if user.id == tweet.user.id:
                            tweet_list.append(tweet)
                
            tweet_list.sort(key=lambda x:x.datetime.timestamp())
            tweet_list.reverse()

            return render(request, "search.html", {"keyword" : keyword, "tweet_list" : tweet_list, "url" : url, "token" : token, "user_url" : user_url, "authentication" : authentication(request)})

        elif token == "user":
            user_set = UserModel.objects.all()
            user_list = []

            for user in user_set:
                if keyword in user.username:
                    user_list.append(user)
            
            return render(request, "search.html", {"keyword" : keyword, "user_list" : user_list, "url" : url, "token" : token, "user_url" : user_url, "authentication" : authentication(request)})

def star_userview(request, tweet_id): # スターをつけたユーザーを表示するためのビュー
    if request.user.is_authenticated:
        if request.user.registration == 0:
            return redirect("profile_image_registration")
        elif request.user.registration == 1:
            return redirect("self_introduction_registration")

    star_set = StarModel.objects.filter(tweet=tweet_id)
    star_user_list = []

    for star in star_set:
        star_user_list.append(star.user)
    
    return render(request, "star_user.html", {"star_user_list" : star_user_list, "authentication" : authentication(request), "tweet_id" : tweet_id})

def retweet_userview(request, tweet_id): # リツイートしたユーザーを表示するためのビュー
    if request.user.is_authenticated:
        if request.user.registration == 0:
            return redirect("profile_image_registration")
        elif request.user.registration == 1:
            return redirect("self_introduction_registration")
    
    retweet_set = RetweetModel.objects.filter(tweet=tweet_id)
    retweet_user_list = []

    for retweet in retweet_set:
        retweet_user_list.append(retweet.user)
    
    return render(request, "retweet_user.html", {"retweet_user_list" : retweet_user_list, "authentication" : authentication(request), "tweet_id" : tweet_id})


