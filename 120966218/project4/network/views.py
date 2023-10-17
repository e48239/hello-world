import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html
# ^^ for future reference

def index(request):

    # Authenicated users can view their posts and add 
    if request.user.is_authenticated:
        return render(request, "network/index.html", {
            "type": "None"
        })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

@login_required
@csrf_exempt
def create(request):

    if request.method == "POST":
        post = Post()
        post.poster = request.user
        post.body = request.POST.get('body')
        # Save to database
        post.save()
        # Send them to the listing page
        return render(request, "network/index.html", {
            "post": post
        })
    else:   
        return render(request, "network/index.html")


@csrf_exempt
@login_required
def getFollowedPosts(request):

    # Get the profile of the user and list of all posts
    profile = get_object_or_404(Profile, user=request.user.id)
    allPosts = Post.objects.all()

    # Get the list of users they follow 
    follows = profile.follows.all()

    #Make an empty list 
    posts = []

    for post in allPosts:
        if post.poster in follows:
            posts.append(post)

    #Update True False attribute for each post based on current user
    for post in posts:
        list = post.liked.all()
        if request.user in list:
            post.liked_by_user = True
            post.save()
        else:
            post.liked_by_user = False
            post.save()

    # Return posts in reverse chronologial order
    posts.sort(key=lambda x: x.timestamp, reverse=True)

    #Add pagination 
    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "network/posts.html", {
        "posts": posts,
        "message": "Following",
        "type" : "following"
    })

@csrf_exempt
@login_required
def getAllPosts(request):

    # Get all the posts
    posts = Post.objects.all()

    #Update True False attribute for each post based on current user
    for post in posts:
        list = post.liked.all()
        if request.user in list:
            post.liked_by_user = True
            post.save()
        else:
            post.liked_by_user = False
            post.save()

    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()

    #Add pagination 
    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "network/posts.html", {
        "posts": posts,
        "message": "All Posts",
        "type" : "all"
    })

@csrf_exempt
@login_required
def getProfile(request, id):

    #Get the users profile
    profile = get_object_or_404(Profile, user=id)

    followerCount = len(profile.followers.all())
    followsCount = len(profile.follows.all())

    #Get their posts
    posts = Post.objects.filter(poster=id)
    posts = posts.order_by("-timestamp").all()

    # Does the user follow this profile
    if request.user in profile.followers.all():
        following = True
    else: 
        following = False

    #Add pagination 
    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "network/profile.html", {
        "profile": profile,
        "followers": followerCount,
        "follows": followsCount,
        "following": following,
        "posts": posts
    })

@csrf_exempt
@login_required
def Follow(request, id):

    #Update the users profile to include the new follower
    profile = Profile.objects.get(user=id)
    profile.followers.add(request.user)

    #Add the person to request.user profile
    follower = Profile.objects.get(user=request.user)
    add = User.objects.get(id=id)
    follower.follows.add(add)

    return HttpResponseRedirect(reverse("profile", args=(id,)))

@csrf_exempt
@login_required
def Unfollow(request, id):

    #Update the users profile to remove the new follower
    profile = Profile.objects.get(user=id)
    profile.followers.remove(request.user)

    # Remove that person from request.user profile
    userP = Profile.objects.get(user=request.user)
    remove = User.objects.get(id=id)
    userP.follows.remove(remove)

    return HttpResponseRedirect(reverse("profile", args=(id,)))

@csrf_exempt
@login_required
def Like(request, id, type):

    if request.method == "POST":
        # Get the post using the ID
        post = Post.objects.get(id=id)
        post.liked.add(request.user)

        # Get the likes and update count
        likes = len(post.liked.all())
        post.likes = likes
        post.save()

        #Add to users profile of liked posts
        profile = Profile.objects.get(user=request.user)
        profile.like.add(post)
        
        if type == "all":
            return HttpResponseRedirect(reverse("all"))
        elif type == "following":
            return HttpResponseRedirect(reverse("following"))

@csrf_exempt
@login_required
def Unlike(request, id, type):

    if request.method == "POST":
        # Get the post using the ID
        post = Post.objects.get(id=id)
        post.liked.remove(request.user)

        # Get the likes and update count
        likes = len(post.liked.all())
        post.likes = likes
        post.liked_by_user = False
        post.save()

        # remove from users profile of liked posts
        profile = Profile.objects.get(user=request.user)
        profile.like.remove(post)

        if type == "all":
            return HttpResponseRedirect(reverse("all"))
        elif type == "following":
            return HttpResponseRedirect(reverse("following"))

@csrf_exempt
@login_required
def Edit(request,id):
    
    #Get the post
    post = Post.objects.get(id=id)
    text = post.body

    return render(request, "network/edit.html", {
        "text": text,
        "post": post 
    })

@csrf_exempt
@login_required
def Save(request,id):
    
    #Get the post
    post = Post.objects.get(id=id)

    # Get the form data
    text = request.POST.get('body')
    post.body = text
    post.save()

    return render(request, "network/edit.html", {
        "text": text,
        "post": post,
        "message" : "Your post has been updated."
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

        # Also create a profile
            profile = Profile()
            profile.user = user
            profile.save()
            
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
