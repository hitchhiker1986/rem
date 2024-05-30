#!/bin/bash
source ../../bin/activate
/bin/systemctl start mariadb.service
python manage.py runserver

