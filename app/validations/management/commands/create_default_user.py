from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create default user"

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="defaultuser").exists():
            User.objects.create_user("defaultuser", password="defaultpassword")
            self.stdout.write(self.style.SUCCESS(
                "Default user has been created."))
        else:
            self.stdout.write(self.style.SUCCESS(
                "Default user already exists."))
