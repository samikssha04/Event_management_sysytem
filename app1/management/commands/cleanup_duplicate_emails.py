from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Remove duplicate emails from User table, keeping only the first account"

    def handle(self, *args, **kwargs):
        seen = set()
        duplicates = []

        for user in User.objects.all().order_by("id"):
            if user.email in seen:
                duplicates.append(user)
            else:
                seen.add(user.email)

        if not duplicates:
            self.stdout.write(self.style.SUCCESS("✅ No duplicate emails found."))
            return

        for dup in duplicates:
            self.stdout.write(f"Deleting duplicate: {dup.username} ({dup.email})")
            dup.delete()

        self.stdout.write(self.style.SUCCESS("✨ Cleanup complete!"))
