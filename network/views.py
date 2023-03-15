import json
import time
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Follow


def index(request):

    # Get all the post
    all_posts = Post.objects.all().order_by("-date")

    # Pagination
    paginator = Paginator(all_posts, 10)
    page_num = request.GET.get("page")
    page_posts = paginator.get_page(page_num)
    
    return render(request, "network/index.html", {
        "page_posts": page_posts,
    })

def likepost(request, post_id):
    # Get the post to be liked or removed from liked
    post = Post.objects.get(pk=post_id)

    if request.user.is_authenticated:
        # Get logged in user
        user = request.user
        if post.likers.filter(id=user.id).exists():
            post.likers.remove(user)
            print("Unliked")
            return HttpResponseRedirect(reverse("index"))
        else:
            post.likers.add(user)
            print("liked")
            return HttpResponseRedirect(reverse("index"))


def following(request):
    # Get the persons the user is following
    user = request.user
    f = user.followings.all()
    followings = [e.following.all()[0] for e in f]
    all_posts = Post.objects.all().order_by("-date")

    # Get the posts of the user's followings
    followingPosts = []
    for post in all_posts:
        for person in followings:
            if person.username == post.poster.username:
                followingPosts.append(post)
    
    # Pagination
    paginator = Paginator(followingPosts, 10)
    page_num = request.GET.get("page")
    page_posts = paginator.get_page(page_num)

    return render(request, "network/following.html", {
        "page_posts": page_posts,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Check if authentication successful
        if username == None or email == None:
            return render(request, "network/register.html", {
                "message": "Invalid username and/or password."
            })

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def addPost(request):

    # writing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get contents of post
    data = request.POST["tweet"]

    # Create a new post for the user.
    user = request.user
    post = Post(
        poster = user,
        post = data,
    )
    post.save()

    return HttpResponseRedirect(reverse("index"))

def profile(request, profile_id):
    # Get profile viewed
    profile = User.objects.get(pk=profile_id)

    # Get the logged in user
    user = request.user

    # Profile posts
    profile_posts = Post.objects.filter(poster=profile).order_by("-date")

    # Persons the profile is following
    followings = [e for e in Follow.objects.filter(user=profile)]

    # Profile's followers
    followers = profile.followers.all()

    userfollowing = False
    for follower in followers:
        if follower.user.username == user.username:
            userfollowing = True
    print(f"{userfollowing}")
    # Pagination
    paginator = Paginator(profile_posts, 10)
    page_num = request.GET.get("page")
    page_posts = paginator.get_page(page_num)
    return render(request, "network/profile.html", {
        "page_posts": page_posts,
        "profile": profile,
        "num_posts": len(page_posts),
        "followings": followings,
        "followers": followers,
        "userfollowing": userfollowing
    })

@login_required
def follow(request, profile_id):
    # Get profile to be followed
    profile = User.objects.get(pk=profile_id)

    # User who is following
    user = request.user

    # Add profile to user's following list
    f = Follow(user=user)
    f.save()
    f.following.add(profile)
    return HttpResponseRedirect(reverse('profile', kwargs={'profile_id': profile.id}))

def unfollow(request, profile_id):
    # Get profile to be unfollowed
    profile = User.objects.get(pk=profile_id)

    # User who wants to unfollow
    user = request.user

    # Get the followers of the profile viewed
    followers = profile.followers.all()

    for follower in followers:
        if follower.user.username == user.username:
            follower.delete()
            return HttpResponseRedirect(reverse('profile', kwargs={'profile_id': profile.id}))

@csrf_exempt
@login_required
def editpost(request, post_id):
    print(post_id)

    # Editing an old post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "Post request required."}, status=400)
    
    # Get content of post
    editedPost = json.loads(request.body).get("post", "")

    # Get the post to be edited
    oldPost = Post.objects.get(pk=post_id)
    oldPost.post = editedPost
    oldPost.save()

    # Delete the previous post
    return JsonResponse(oldPost.serialize())