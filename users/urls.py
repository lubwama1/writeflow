
from django.urls import path
from . import views


app_name = 'users' 
urlpatterns = [
     path('login/', views.user_login, name='account_login'),
     path('signup/', views.user_register, name='account_signup'),
     path('profile/<str:username>/', views.user_profile, name='profile'),
     path('account/', views.user_account, name='account'),
     path('logout/', views.user_logout, name='account_logout'),

     path('confirm-email/<key>/', views.UserConfirmEmailView.as_view(), name='account_confirm_email'),
     path('author_profile/<int:pk>/', views.author_profile, name='author_profile'),
]
