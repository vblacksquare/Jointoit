from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from config import get_config


CONFIG = get_config()
User = get_user_model()


class Command(BaseCommand):
    help = "Create or update superuser"

    def handle(self, *args, **kwargs):

        name = CONFIG.admin.name
        email = CONFIG.admin.email
        password = CONFIG.admin.password

        user = User.objects.filter(name=name).first()

        if user:
            if [name, email] == [user.name, user.email] and check_password(password, user.password):
                self.stdout.write(self.style.SUCCESS("Superuser already up to date"))
                return

            user.name = name
            user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()

            self.stdout.write(self.style.WARNING("Superuser updated"))
        else:
            User.objects.create_superuser(
                name=name,
                email=email,
                password=password
            )

            self.stdout.write(self.style.SUCCESS("Superuser created"))
