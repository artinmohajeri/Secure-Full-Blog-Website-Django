from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import SignUpForm, SignInForm,ProfilePicForm, BioForm, BlogForm
from .models import CustomUser, Blog

class HomePage(TemplateView):
    template_name = "home.html"

def signup_page(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        username = request.POST["username"]
        confirm_password = request.POST.get('confirm_password')
        if form.is_valid():
            password = form.cleaned_data["password"]
            if len(password) >= 7 or len(confirm_password)>=7:
                if password == confirm_password:  #check if the username already exists
                    user = form.save(commit=False)
                    user.save()
                    user = authenticate(username=username, password=password)
                    messages.success(request, "Your account was created successfully!")
                    login(request, user)
                    return redirect('/profile/'+username)
                else:
                    messages.warning(request, 'Your password doesnt match!')
            else:
                messages.warning(request, 'password should containt at least 7 letters!')
        else:
            if CustomUser.objects.filter(username=username).exists():
                messages.warning(request, 'The username already exists!')
            else:
                messages.warning(request, 'Form submission failed. Please try again.')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, "user":request.user})


def signin_page(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            print(form.is_valid)
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect('/profile/'+username)
            else:
                messages.warning(request, "The user does not exist or the password is incorrect")
        else:
            messages.warning(request, "Invalid form data. Please check the input.")
            print("*****************************")
            print(form.is_valid)
    else:
        form = SignInForm()
    return render(request, 'signin.html', {"form": form, "user":request.user})


def blog_page(request,username, id):
    blog = Blog.objects.get(id=id)
    return render(request, 'blog.html', {'blog':blog})

def blogs_page(request):
    blogs = Blog.objects.all()
    return render(request, 'blogs.html', {'blogs':blogs})

def followings_blogs_page(request):
    blogs = Blog.objects.all()
    followed_users = request.user.followings.all()
    show_only_my_followings_blogs = True
    return render(request, 'blogs.html', {'blogs':blogs, 'followed_users':followed_users, 'show_only_my_followings_blogs':show_only_my_followings_blogs})

@login_required
def profile_page(request, username):
    bioform = BioForm()
    blogform = BlogForm()
    user = get_object_or_404(CustomUser,username=username)
    if request.method == "POST":
        if "addpic" in request.POST:
            form = ProfilePicForm(request.POST, request.FILES)
            if form.is_valid():
                pic = form.cleaned_data["pic"]
                request.user.pic = pic
                request.user.save()
                messages.success(request, "Your profile picture changed successfuly")
                return redirect('/profile/'+username)
        elif "addbio" in request.POST:
            bioform = BioForm(request.POST)
            if bioform.is_valid():
                bio = bioform.cleaned_data["bio"]
                request.user.bio = bio
                request.user.save()
                messages.success(request, "Your bio changed successfuly")
                return redirect('/profile/'+username)
        elif "addblog" in request.POST:
            blogform = BlogForm(request.POST, request.FILES)
            if blogform.is_valid():
                blog = blogform.save(commit=False)
                blog.author = request.user
                print(blog.pic)
                blog.save()
                messages.success(request, "Your blog was posted successfuly")
                return redirect('/profile/'+username)
    else:
        form = ProfilePicForm()
    return render(request, 'profile.html', {"user":user, "form":form, "bioform":bioform, "blogform":blogform})

def delete_bio(request):
    request.user.bio = ""
    request.user.save()
    messages.success(request, "Your bio was deleted successfuly")
    return redirect('/profile/'+request.user.username)

def delete_account(request):
    request.user.delete()
    messages.success(request, "Your account was deleted successfuly")
    return redirect('/')

@login_required
def logout_func(request):
    logout(request)
    messages.success(request, "Logged out successfuly!")
    return redirect(to=reverse('signin_page'))

@login_required
def follow(request, username):
    user = get_object_or_404(CustomUser, username=username)
    user.followers.add(request.user)
    request.user.followings.add(user)
@login_required
def unfollow(request, username):
    user = get_object_or_404(CustomUser, username=username)
    user.followers.remove(request.user)
    request.user.followings.remove(user)

@login_required
def like(request, id):
    blog = get_object_or_404(Blog, id=id)
    blog.likes.add(request.user)
    return redirect(request.META['HTTP_REFERER'])

@login_required
def dislike(request, id):
    blog = get_object_or_404(Blog, id=id)
    blog.likes.remove(request.user)
    return redirect(request.META['HTTP_REFERER'])

def users(request):
    all_users = CustomUser.objects.all()
    return render(request, 'users.html', {"users":all_users})

class ContactPage(TemplateView):
    template_name = "contact.html"