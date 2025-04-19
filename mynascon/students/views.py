from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Student

# Custom decorator to protect views
def student_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('student_id'):
            return redirect('students:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def signup_view(request):
    if request.session.get('student_id'):
        return redirect('students:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
        elif Student.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
        elif Student.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use')
        else:
            hashed_password = make_password(password1)
            student = Student.objects.create(username=username, email=email, password=hashed_password)
            request.session['student_id'] = student.id
            messages.success(request, 'Account created and logged in successfully!')
            return redirect('students:dashboard')

    return render(request, 'signup.html')


def login_view(request):
    if request.session.get('student_id'):
        return redirect('students:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(username=username)
            if check_password(password, student.password):
                request.session['student_id'] = student.id
                messages.success(request, f'Welcome back, {student.username}!')
                print('Login successful')
                return redirect('students:dashboard')
            else:
                print('Incorrect password')
                messages.error(request, 'Incorrect password')
        except Student.DoesNotExist:
            print('User does not exist')
            messages.error(request, 'User does not exist')

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return redirect('students:login')


@student_login_required
def dashboard_view(request):
    student_id = request.session.get('student_id')
    student = Student.objects.get(id=student_id)
    return render(request, 'dash.html', {'student': student})
