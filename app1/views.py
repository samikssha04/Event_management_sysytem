from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def admin_portal_view(request):
    return render(request, 'admin_portal.html')
