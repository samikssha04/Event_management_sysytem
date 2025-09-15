from django.contrib import admin
from .models import Event, Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "event", "registered_at")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "time", "location", "enrolled_count", "max_participants")
    list_filter = ("date", "location")
    search_fields = ("title", "description")