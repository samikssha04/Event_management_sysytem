from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Event, Enrollment, Registration
from .forms import EventForm
from datetime import date
from app1.models import CustomUser
from app1.forms import SignupForm
from django.contrib.auth import get_user_model


# ---------------- HOME ----------------
def home_view(request):
    return render(request, 'home.html')


# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.email}!")
            return redirect('student_dashboard')  # your dashboard
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'login.html')

# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------- SIGNUP -------------
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')  # replace with your login URL name
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})



# ---------------- STUDENT DASHBOARD ----------------
@login_required
def student_dashboard_view(request):
    user = request.user
    events = Event.objects.all()
    enrollments = Enrollment.objects.filter(student=user)
    registered_events = [enrollment.event for enrollment in enrollments]

    upcoming_events = Event.objects.filter(date__gte=date.today()).exclude(id__in=[e.id for e in registered_events])[:3]

    context = {
        "user": user,
        "registered_events": registered_events,
        "upcoming_events": upcoming_events,
    }
    return render(request, "student_dashboard.html", context)


# ---------------- EVENT DETAIL ----------------
def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, "event_detail.html", {"event": event})


# ---------------- EVENT LIST ----------------
@login_required
def events_list_view(request):
    events = Event.objects.all()
    registered_event_ids = Enrollment.objects.filter(student=request.user).values_list('event_id', flat=True)

    if request.method == "POST":
        event_id = int(request.POST.get("event_id"))
        event = Event.objects.get(id=event_id)

        if event_id in registered_event_ids:
            messages.warning(request, "You have already registered for this event.")
        elif event.enrolled_count >= event.max_participants:
            messages.error(request, "Event is full.")
        else:
            Enrollment.objects.create(student=request.user, event=event)
            event.enrolled_count += 1
            event.save()
            messages.success(request, "Registered successfully!")
            return redirect("events_list")

    context = {
        "events": events,
        "registered_event_ids": registered_event_ids,
    }
    return render(request, "event_list.html", context)


# ---------------- ENROLL EVENT ----------------
@login_required
def enroll_event_view(request, event_id):
    """Register current student for an event"""
    event = get_object_or_404(Event, id=event_id)

    # prevent duplicate enrollment
    if not Enrollment.objects.filter(student=request.user, event=event).exists():
        Enrollment.objects.create(student=request.user, event=event)
        event.enrolled_count += 1
        event.save()

    return redirect("events_list")


# ---------------- REGISTER EVENT (for student dashboard quick register) ----------------
def register_event(request, event_id):
    if not request.user.is_authenticated:   # student must be logged in
        return redirect("login")

    event = get_object_or_404(Event, id=event_id)

    # Check if already registered
    existing = Registration.objects.filter(student=request.user, event=event)
    if not existing.exists():
        Registration.objects.create(student=request.user, event=event)

    return redirect("student_dashboard")
