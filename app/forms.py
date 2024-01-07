from django import forms
from .models import CustomUser, Blog
from django.contrib.auth.forms import AuthenticationForm


class SignUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super(SignUpForm, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs.update({'class': 'form-control','_type':'text', 'id': 'uname', 'placeholder': 'Enter username', 'maxlength':'30', 'name':'username'})
            self.fields['password'].widget.attrs.update({'class': 'form-control','_type':'password', 'id': 'pwd', 'placeholder': 'Enter password','name':"password", 'maxlength':'128'})
            self.fields['fname'].widget.attrs.update({'class': 'form-control','_type':'text', 'id': 'fname', 'placeholder': 'First Name', 'maxlength':'20'})
            self.fields['lname'].widget.attrs.update({'class': 'form-control','_type':'text', 'id': 'lname', 'placeholder': 'Last Name', 'maxlength':'20'})
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'fname', 'lname']


class SignInForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','_type':'text', 'id': 'uname', 'placeholder': 'Enter username', 'maxlength':'30', 'name':'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','_type':'password', 'id': 'pwd', 'placeholder': 'Enter password','name':"password", 'maxlength':'128'}))
    # def __init__(self, *args, **kwargs):
    #     super(SignInForm, self).__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs.update({'class': 'form-control','_type':'text', 'id': 'uname', 'placeholder': 'Enter username', 'maxlength':'30', 'name':'username'})
    #     self.fields['password'].widget.attrs.update({'class': 'form-control','_type':'password', 'id': 'pwd', 'placeholder': 'Enter password','name':"password", 'maxlength':'128'})
    # class Meta:
    #         model = CustomUser
    #         fields = ['username', 'password']

class ProfilePicForm(forms.Form):
    pic = forms.FileField(widget=forms.FileInput(attrs={'_type':'file', 'id': 'profile-input', 'name':'pic'}))

class BioForm(forms.Form):
    bio = forms.CharField(widget=forms.Textarea(attrs={'id': 'bio-txt', 'name':"blog-text", 'cols':'30', 'rows':'5' , 'class':'form-control'}))

class BlogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super(BlogForm, self).__init__(*args, **kwargs)
            self.fields['pic'].widget.attrs.update({'class': 'form-control','_type':'file', 'id':'blog-img', 'name':'blogimg'})
            self.fields['title'].widget.attrs.update({'class': 'form-control','_type':'text', 'id': 'blog-title','name':"blog-title", 'maxlength':'50'})
            self.fields['body'].widget.attrs.update({'class': 'form-control', 'id': 'blog-txt','name':'blog-text','cols':'30', 'rows':'5'})
    class Meta:
        model = Blog
        fields = ['pic', 'title', 'body']