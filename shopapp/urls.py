from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'shopapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('update_user/', views.edit_profile, name='update_user'),
    path('delete_user/', views.delete_profile, name='delete_user'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('comment/edit/<int:pk>/', views.edit_comment, name='edit_comment'),
    path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'),


]
