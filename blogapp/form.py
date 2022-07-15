from django import forms
from django.contrib.auth.forms import UserCreationForm,User
from blogapp.models import UserProfile,Blog,Comments
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2"
        ]
class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())

class CreateUserForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=('user',)
        widgets= {
            "date_of_birth" : forms.DateInput(attrs={"type":"date","class":"form-control"}),
            "bio":forms.TextInput(attrs={"class":"form-control"})

        }

class ResetPasswordForm(forms.Form):
    old_password=forms.CharField(widget=forms.PasswordInput())
    new_password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField()

class BlogForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields=[
            "image",
            "title",
            "description"

        ]
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control"}),
            "image":forms.FileInput(attrs={"class":"form-control"})
        }

class ProfilepicUpdateForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=[
            "profile_pic"
        ]
        widgets={
            "profile_pic":forms.FileInput(attrs={"class":"form-control"})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model= Comments
        fields=["comment"]
        widgets={
            "comment":forms.TextInput(attrs={"class":"form-control"})
        }
