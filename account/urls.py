from django.urls import path
from . import views
urlpatterns = [
    path('' , views.profile , name='profile'),
    path('editprofile' , views.editProfile , name='editprofile'),
    path('login' , views.userLogin , name='login'),
    path('register' , views.register , name='register'),
    path('reset-pass' , views.resetPass , name='resetPass'),
    # path('forgot-pass' , views.forgotPass , name='forgotPass'),
    path('logout' , views.userLogout , name='logout'),
]