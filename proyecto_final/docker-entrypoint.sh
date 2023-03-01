#!/bin/bash

echo "Flush manage.py command"

while ! python manage.py flush --no-input 2>&1; do
    echo "Flush django manage command"
    sleep 3
done

echo "Migrate the Database at startup of project"

while ! python manage.py migrate 2>&1; do
    echo "Migration is in progress status"
    sleep 3
done

echo "Django docker is fully configured successfully"

exec "$@"