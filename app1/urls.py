from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path('logout/', views.logout_view, name='logout'),
    path("student_dashboard/", views.student_dashboard_view, name="student_dashboard"),
    path("events/", views.events_list_view, name="events_list"),
    path("events/enroll/<int:event_id>/", views.enroll_event_view, name="enroll_event"),
    path("event/<int:event_id>/", views.event_detail, name="event_detail"),

]



