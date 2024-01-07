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

class BlogPage(TemplateView):
    template_name = "blog.html"

class BlogsPage(TemplateView):
    template_name = "blogs.html"

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
                return redirect('/profile/'+username)
        elif "addbio" in request.POST:
            bioform = BioForm(request.POST)
            if bioform.is_valid():
                bio = bioform.cleaned_data["bio"]
                request.user.bio = bio
                request.user.save()
                return redirect('/profile/'+username)
        elif "addblog" in request.POST:
            blogform = BlogForm(request.POST)
            if blogform.is_valid():
                blog = blogform.save(commit=False)
                blog.author = request.user
                blog.save()
                return redirect('/profile/'+username)
    else:
        form = ProfilePicForm()
    return render(request, 'profile.html', {"user":user, "form":form, "bioform":bioform, "blogform":blogform})

def delete_bio(request):
    request.user.bio = ""
    request.user.save()
    return redirect('/profile/'+request.user.username)

def delete_account(request):
    request.user.delete()
    return redirect('/')


def logout_func(request):
    logout(request)
    messages.success(request, "Logged out successfuly!")
    return redirect(to=reverse('signin_page'))


class UsersPage(TemplateView):
    template_name = "users.html"

def users(request):
    all_users = CustomUser.objects.all()
    return render(request, 'users.html', {"users":all_users})

class ContactPage(TemplateView):
    template_name = "contact.html"