import os

from django.core.management.base import BaseCommand, CommandError
from rem.models import *
from django.core.mail import EmailMessage
from django.core.mail import get_connection
import datetime

from rem.models import Apartment

class Command(BaseCommand):


    def add_arguments(self, parser):
        parser.add_argument('apartment_id', type=int)

    def handle(self,  *args, **options):
        if options['apartment_id'] > 0:
            try:
                apartment = Apartment.objects.get(id=options['apartment_id'])
            except Apartment.DoesNotExist:
                raise CommandError('Apartment does not exist')

            if apartment.next_check < 3 and apartment.check_status:
                apartment.next_check += 1

            if apartment.next_check == 6 and apartment.check_status:
                apartment.next_check *= 2

            if not apartment.check_status:
                apartment.next_check = 1

            t = ToDo()
            t.start_day = datetime.date.today() + datetime.timedelta(days=+apartment.next_check*30)
            t.end_day = t.start_day + datetime.timedelta(days=+5)
            t.task_responsible = User.objects.get(username="admin")
            t.title = "Állapotfelmérés - " + str(apartment)
            t.description = "A(z) " + apartment.city + " " + apartment.address + " következö ellenörzése."
            t.save()

            email = EmailMessage(
                t.title,
                t.description,
                User.objects.get(username="admin").email,
                {t.responsible.email},
            )

            email.send()


        else:
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


# use_date = datetime.datetime.now()
# print(use_date)
# 2024-02-13 14:28:16.987258
# use_date = use_date + datetime.timedelta(days=-15)
