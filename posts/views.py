from django.shortcuts import render, redirect
from .models import Posts
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User, auth
from django.db.models import Q

def redirect_if_authenticated(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You are loged in no need to do it again!")
            return redirect("/")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def redirect_if_not_authenticated(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You need to login first!")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def redirect_if_not_superuser(view_func):
  def _wrapped_view(request, *args, **kwargs):
    if not request.user.is_superuser:
      return redirect("/")
    return view_func(request, *args, **kwargs)
  return _wrapped_view

# Create your views here.

# @redirect_if_not_authenticated
def index(request):
    search_query = request.GET.get('q', '')
    posts = Posts.objects.all()

    if search_query and request.user.is_authenticated:
        posts = posts.filter(Q(title__icontains=search_query))
        if not posts:
          return render(request, "index.html", {"post_not_found": True})
        
    paginator = Paginator(posts, 3)
    page = request.GET.get("page")
    all_posts = paginator.get_page(page)
    return render(request, "index.html", {"posts": all_posts, "search_query": search_query})

@redirect_if_not_authenticated
def post(request, pk):
  post = Posts.objects.get(id=pk)
  return render(request, "post.html", {"post": post})

@redirect_if_not_superuser
def create_blog(request):
  if request.method == "POST":
    title = request.POST["title"]
    description = request.POST["description"]

    if not title and not description:
      messages.error(request, "Please fill out the required fields correctly!")
      return redirect("create_blog")
    if not title:
      messages.error(request, "Please fill out the title field correctly!")
      return redirect("create_blog")
    if not description:
      messages.error(request, "Please fill out the description field correctly!")
      return redirect("create_blog")

    new_post = Posts()
    new_post.title = title
    new_post.body = description
    new_post.save()
    messages.success(request, "New blog created successfully!")
    return redirect("/")
  else:
    return render(request, "create_blog.html")


@redirect_if_authenticated
def register(request):
  if request.method == "POST":
    email = request.POST["email"]
    username = request.POST["username"]
    password = request.POST["password"]

    if not email and not username and not password:
      messages.error(request, "Please fill out the required fields correctly!")
      return redirect("register")
    elif not email:
      messages.error(request, "Please fill out the email field correctly!")
      return redirect("register")
    elif not password:
      messages.error(request, "Please fill out the password field correctly!")
      return redirect("register")

    existing_username = User.objects.filter(username=username).exists()
    existing_email = User.objects.filter(email=email).exists()

    if existing_email:
      messages.error(request, "Email Already Exists")
      return redirect("register")
    elif existing_username:
      messages.error(request, "Username Already Exists")
      return redirect("register")
    else:
      user = User.objects.create_user(email=email, username=username, password=password)
      user.save()
      messages.success(request, "Confirm your account by logging in")
      return redirect("login")
  
  return render(request, "register.html")


@redirect_if_authenticated
def login(request):
  if request.method == "POST":
    username = request.POST["username"]
    password = request.POST["password"]
    user = auth.authenticate(username=username, password=password)

    if not username and not password:
      messages.error(request, "Please fill out the required fields correctly!")
      return redirect("login")
    elif not username:
      messages.error(request, "Please fill out the username field correctly!")
      return redirect("login")
    elif not password:
      messages.error(request, "Please fill out the password field correctly!")
      return redirect("login")

    if user is not None:
      auth.login(request, user)
      messages.success(request, f"Welcome {user.username}")
      return redirect("/")
    else:
      messages.error(request, "Credentials Invalid")
      return redirect("login")
    
  return render(request, "login.html")
  

def logout(request):
  auth.logout(request)
  messages.success(request, "You loged out successfully!")
  return redirect("login")