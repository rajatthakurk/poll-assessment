# poll-assessment

install requirements.txt

install redis on your system

open two terminals

run "python manage.py runserver" on terminal 1

run "celery -A Poll_Project.celery worker --pool=solo -l info" on terminal 2
