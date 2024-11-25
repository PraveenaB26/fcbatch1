from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import BlogPost

# User Registration View
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Simple validation (optional, additional to form)
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')
        
        # Create user if validations pass
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('all_blogs')  # Redirect to blogs page after registration
    
    return render(request, 'register.html')

# User Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('all_blogs')
        
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# User Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# View for Creating a Blog Post
@login_required
def create_blog_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        BlogPost.objects.create(title=title, content=content, author=request.user)
        return redirect('all_blogs')
    return render(request, 'create_blog.html')

# View for Displaying All Blog Posts
def all_blogs_view(request):
    blogs = BlogPost.objects.all()
    return render(request, 'all_blogs.html', {'blogs': blogs})

@login_required
def edit_blog_view(request, blog_id):
    blog_post = get_object_or_404(BlogPost, id=blog_id, author=request.user)
    
    if request.method == 'POST':
        blog_post.title = request.POST.get('title')
        blog_post.content = request.POST.get('content')
        blog_post.save()
        return redirect('all_blogs')  # Redirect to the all blogs page after editing
    
    return render(request, 'edit_blog.html', {'blog_post': blog_post})

