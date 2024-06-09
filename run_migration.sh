#!/bin/bash
rm -f "db.sqlite3"

#run the migrations
python manage.py makemigrations
python manage.py migrate

#create the superuser
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin','guru@gmail.com','admin')"|python manage.py shell

#prepare the dummy data
python manage.py generate_dummy_data