from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,FormView,TemplateView,UpdateView
from blogapp.form import UserRegistrationForm,LoginForm,CreateUserForm,ResetPasswordForm,BlogForm,ProfilepicUpdateForm,CommentForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from blogapp.models import UserProfile,Blog,Comments
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,"you must login")
            return redirect("sign-in")
    return wrapper

class SigninView(CreateView):
    form_class = UserRegistrationForm
    template_name = "registration.html"
    model = User
    success_url = reverse_lazy("signin")
    # def get(self,request,*args,**kwargs):
    #     form=self.reg_form()
    #     return render(request,self.reg_tem,{"form":form})
    #
    # def post(self,request,*args,**kwargs):
    #     form=self.reg_form(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request,"account created successfully")
    #         return render(request,self.reg_tem,{"form":form})
    #     else:
    #         messages.error(request,"account creation failed")
    #         return render(request,self.reg_tem,{"form":form})

class LoginView(FormView):
    template_name="login.html"
    form_class = LoginForm
    model = User
    # def get(self,request,*args,**kwargs):
    #     return render(request,self.log_tem)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
        if user:
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"incorrect username or password")
            return render(request,self.template_name,{"form":form})

@method_decorator(signin_required,name="dispatch")
class IndexView(CreateView):
    template_name = "home.html"
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author=self.request.user
        self.object = form.save()
        messages.success(self.request,"Post has been added successfully")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        blogs=Blog.objects.all().order_by("-posted_date")
        context["blogs"]=blogs
        comment_form=CommentForm()
        context["comment_form"]=comment_form
        return context



@signin_required
def signout(request,*args,**kwargs):
    logout(request)
    return redirect("signin")

@method_decorator(signin_required,name="dispatch")
class CreateUserProfileView(CreateView):
    template_name = "add.html"
    form_class = CreateUserForm
    model = UserProfile
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"profile has been created")
        self.object=form.save()
        return  super().form_valid(form)

@method_decorator(signin_required,name="dispatch")
class ViewProfileView(TemplateView):
    template_name = "viewprofile.html"

@method_decorator(signin_required,name="dispatch")
class ResetPasswordView(FormView):
    form_class = ResetPasswordForm
    template_name = "resetpwd.html"

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            oldpassword=form.cleaned_data.get("old_password")
            new_password=form.cleaned_data.get("new_password")
            confirm_password=form.cleaned_data.get("confirm_password")
            user=authenticate(request,username=request.user.username,password=oldpassword)
            if new_password!=confirm_password:
                messages.error(request,"both passwords are not matching")
                return  render(request,self.template_name,{"form":form})
            elif user:
                user.set_password(confirm_password)
                user.save()
                messages.success(request,"password updated successfully")
                return redirect("signin")
            else:
                messages.error(request,"incorrect old password")
                return render(request,self.template_name,{"form":form})

@method_decorator(signin_required,name="dispatch")
class ProfileupdateView(UpdateView):
    model = UserProfile
    form_class = CreateUserForm
    template_name = "profile-update.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"

    def form_valid(self, form):
        messages.success(self.request,"profile has been updated")
        self.object = form.save()
        return super().form_valid(form)

@method_decorator(signin_required,name="dispatch")
class ProfilepicUpdateView(UpdateView):
    model = UserProfile
    form_class = ProfilepicUpdateForm
    template_name = "profilepic-update.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"


def add_comment(request,*args,**kwargs):
    if request.method=="POST":
        blog_id=kwargs.get("post_id")
        blog=Blog.objects.get(id=blog_id)
        user=request.user
        comment=request.POST.get("comment")
        Comments.objects.create(blog=blog,user=user,comment=comment)
        messages.success(request,"you are commented to this post")
        return redirect("home")

def add_like(request,*args,**kwargs):
    blog_id=kwargs.get("post_id")
    blog=Blog.objects.get(id=blog_id)
    blog.liked_by.add(request.user)
    blog.save()
    return redirect("home")
