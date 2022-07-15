from django.urls.conf import path
from blogapp import views

urlpatterns=[
    path("accounts/signup",views.SigninView.as_view(),name="signup"),
    path("accounts/signin",views.LoginView.as_view(),name="signin"),
    path("home",views.IndexView.as_view(),name="home"),
    path("accounts/signout",views.signout,name="signout"),
    path("user/profile/add",views.CreateUserProfileView.as_view(),name="add-profile"),
    path("user/profiles",views.ViewProfileView.as_view(),name="viewprofile"),
    path("user/profiles/changepassword",views.ResetPasswordView.as_view(),name="change-pwd"),
    path("user/profiles/update/<int:user_id>",views.ProfileupdateView.as_view(),name="update-profile"),
    path("user/profiles/profilepic-update/<int:user_id>",views.ProfilepicUpdateView.as_view(),name="pic-update"),
    path("post/comment/<int:post_id>",views.add_comment,name="add-comment"),
    path("post/like/add/<int:post_id>",views.add_like,name="add-like"),
]