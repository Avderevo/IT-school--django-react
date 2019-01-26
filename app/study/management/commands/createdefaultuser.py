from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create default super user'

    def handle(self, *args, **options):
        self.create_user()

    def create_user(self):
        try:
            get_user_model().objects.get(username='admin')
            message = '[{0}] Default django user already exists.'.format(__name__)
            self.stdout.write(self.style.SUCCESS(message))
        except get_user_model().DoesNotExist:
            user = get_user_model().objects.create(
                username='admin',
                email='admin@ITS.com',
                is_superuser=True,
                is_staff=True
            )
            user.set_password('admin')
            user.save()
            message = '[{0}] Default django user successfully created.'.format(__name__)
            self.stdout.write(self.style.SUCCESS(message))