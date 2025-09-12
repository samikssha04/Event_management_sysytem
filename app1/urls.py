from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("admin_portal/", views.admin_portal_view, name="admin_portal"),
    path('logout/', views.logout_view, name='logout'),
    path("student-dashboard/", views.student_dashboard_view, name="student_dashboard"),
]

