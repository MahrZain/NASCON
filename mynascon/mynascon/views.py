from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from urllib.parse import urlencode
from students.models import Student
from teacher.models import Course, CourseVideo

def signup_view(request):
    if request.session.get('student_id'):
        return redirect('student_home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if Student.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        if Student.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('signup')

        Student.objects.create(username=username, email=email, password=password1)
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'signup.html')

def login_view(request):
    if request.session.get('student_id'):
        return redirect('student_home')  # or 'student_home_browse' if you prefer

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(username=username, password=password)
            request.session['student_id'] = student.id

            # ✅ Redirect with ?page=browse
            base_url = reverse('student_home')
            query_string = urlencode({'page': 'browse'})
            return redirect(f"{base_url}?{query_string}")

        except Student.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')


def home(request):
    return render(request, 'index.html')


def teacherHome(request):
    return render(request, 'teacher/home.html')




    student = Student.objects.get(id=student_id)
    return render(request, 'student/dash.html', {'student': student})

def dashboard_view(request):
    student_id = request.session.get('student_id')
    student = Student.objects.get(id=student_id)
    page = request.GET.get('page', 'welcome')  # default is welcome
    return render(request, 'dash.html', {'student': student, 'page': page})


def studentHome(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    student = Course.objects.get(id=student_id)
    page = request.GET.get('page', 'welcome')
    return render(request, 'student/dash.html', {'student': student, 'page': page})