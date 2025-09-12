from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Event, Enrollment

def home_view(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")  # match your form field
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("login")

        user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            login(request, user)

            # check role safely
            if hasattr(user, "profile") and user.profile.role == "admin":
                return redirect("admin_portal")
            else:
                return redirect("student_dashboard")

        else:
            messages.error(request, "Invalid email or password")
            return redirect("login")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("name")  # matches signup.html
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role", "student")  # default to student
        student_id = request.POST.get("student_id")

        # check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('signup')

        # create user
        user = User.objects.create_user(username=username, email=email, password=password)

        # create profile with role & student_id
        Profile.objects.create(user=user, role=role, student_id=student_id)

        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'signup.html')


@login_required
def admin_portal_view(request):
    return render(request, 'admin_portal.html')


@login_required
def student_dashboard_view(request):
    user = request.user
    enrollments = Enrollment.objects.filter(student=user)
    registered_events = [enrollment.event for enrollment in enrollments]

    from datetime import date
    upcoming_events = Event.objects.filter(date__gte=date.today()).exclude(id__in=[e.id for e in registered_events])[:3]

    context = {
        "user": user,
        "registered_events": registered_events,
        "upcoming_events": upcoming_events,
    }
    return render(request, "student_dashboard.html", context)
