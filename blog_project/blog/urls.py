from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register_view'),  # Define the URL pattern
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_blog_view, name='create_blog'),
    path('blogs/', views.all_blogs_view, name='all_blogs'),
    path('edit_blog/<int:blog_id>/', views.edit_blog_view, name='edit_blog'), 
]
