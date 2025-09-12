from django.contrib import admin
from .models import Event, Enrollment

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "location", "category", "max_participants", "enrolled_count")

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "event", "registered_at")
