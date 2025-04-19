from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
        elif Student.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
        else:
            student = Student.objects.create(username=username, email=email, password=password1)
            request.session['student_id'] = student.id
            return redirect('students:dashboard')
    return render(request, 'signup.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('Received:', username, password)

        try:
            student = Student.objects.get(username=username, password=password)
            request.session['student_id'] = student.id
            print('✅ Valid credentials')
            return redirect('students:dashboard')
        except Student.DoesNotExist:
            print('❌ Invalid credentials')
            messages.error(request, 'Invalid username or password')
    else:
        print('Rendering login page')

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('students:login')


def dashboard_view(request):
    student_id = request.session.get('student_id')
    if student_id:
        student = Student.objects.get(id=student_id)
        return render(request, 'dash.html', {'student': student})
    else:
        return redirect('students:login')
