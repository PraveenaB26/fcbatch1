from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task, Address
from geopy.geocoders import Nominatim  # Optional for geolocation or use Google Maps API

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, email=email, password=password1)
        
        # Handle address geolocation (optional)
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(address)
        if location:
            Address.objects.create(
                user=user,
                address=address,
                latitude=location.latitude,
                longitude=location.longitude
            )
        messages.success(request, 'Registration successful.')
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials')
        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist')

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('login')

@login_required
def dashboard_view(request):
    tasks = Task.objects.filter(created_by=request.user)
    return render(request, 'dashboard.html', {'tasks': tasks})

@login_required
def add_task_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date_time = request.POST.get('date_time')
        assigned_to_id = request.POST.get('assigned_to')
        assigned_to = User.objects.get(id=assigned_to_id)

        task = Task.objects.create(
            name=name,
            date_time=date_time,
            assigned_to=assigned_to,
            created_by=request.user
        )
        messages.success(request, 'Task added successfully.')
        return redirect('dashboard')

    users = User.objects.exclude(id=request.user.id)  # Exclude the current user
    return render(request, 'add_task.html', {'users': users})

