#!/bin/bash

# Reset database and migrations
python manage.py reset_db --yes

# Create migrations and apply them
python manage.py makemigrations
python manage.py migrate

# Collect static files
yes yes | python manage.py collectstatic

# Populate game data
python manage.py populate_gamedata
