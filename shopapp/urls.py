from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'shopapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('<int:pk>/profile/', views.profile, name='profile'),
    path('<int:pk>/update_user/', views.edit_profile, name='update_user'),
    path('<int:pk>/delete_user/', views.delete_profile, name='delete_user'),

]