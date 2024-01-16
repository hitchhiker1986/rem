from django.core.management.base import BaseCommand, CommandError
from rem.models import *
from django.core.mail import EmailMessage

class Command(BaseCommand):
    def handle(self,  *args, **options):

        t = ToDo()
        t.start_day = 10
        t.end_day = 15
        t.description = "This is a new test task"
        t.title = "Test Task #5"
        t.responsible = User.objects.get(username="laszlo")
        t.save()
        print(t.responsible.email)
        print(User.objects.get(username="admin").email)
        email = EmailMessage(
            t.title,
            t.description,
            User.objects.get(username="admin").email,
            {t.responsible.email},
        )

        email.send()
