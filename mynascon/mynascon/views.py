from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pusher
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Account created. Please log in.")
        return redirect('login')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# @login_required(login_url='login')
def home(request):
    return render(request, 'index.html')

pusher_client = pusher.Pusher(
  app_id='1977792',
  key='04413b42c5876c94141b',
  secret='0a299870c1aeb3b5a5c2',
  cluster='mt1',
  ssl=True
)

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        pusher_client.trigger('my-channel', 'my-event', {'message': message})
        return JsonResponse({'status': 'Message sent'})
    
def chat_view(request):
    return render(request, 'chat.html')