import os

from django.core.management.base import BaseCommand, CommandError
from rem.models import *
from django.core.mail import EmailMessage
from django.core.mail import get_connection
import datetime

from rem.models import Utility, ToDo


def calcStart(x):
    if x <= datetime.date.today().day:
        month = (datetime.date.today().month + 1) % 13
        if month == 13:
            month += 1
            year = datetime.date.today().year + 1
        else:
            year = datetime.date.today().year
    if x >= datetime.date.today().day:
        month = datetime.date.today().month
        year = datetime.date.today().year

    return datetime.date(year, month, x)


class Command(BaseCommand):
    def handle(self,  *args, **options):
        for utility in Utility.objects.all():

            next_check_start_date = calcStart(utility.dict_start_day)
            if(utility.dict_start_day < utility.dict_end_day):
                next_check_end_date = datetime.date(next_check_start_date.year, next_check_start_date.month, utility.dict_end_day)
            else:
                m = (next_check_start_date.month + 1) % 13
                if m == 0:
                    m += 1
                    y = next_check_start_date.year + 1
                next_check_end_date = datetime.date(y, m, utility.dict_end_day)

            if (datetime.date.today() - next_check_start_date).days <= 5:
                task = ToDo()
                task.start_day = next_check_start_date
                task.end_day = next_check_end_date
                task.description = str(Utility.serial) + " sorozatszámú fogyasztásmérö óraállásának diktálása. Esedékes " + str(next_check_end_date) + " dátumig!"
                task.title = "Diktálás " + str(utility.serial)
                task.responsible = utility.util_responsible

                task.save()


                email = EmailMessage(
                task.title,
                task.description,
                User.objects.get(username="admin").email,
                {task.responsible.email},
                )

                email.send()