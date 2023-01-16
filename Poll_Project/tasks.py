from celery import shared_task
import datetime
from django.utils import timezone
from Poll_App.models import Poll


@shared_task(bind=True)
def delete_ex_poll(self):
    d = timezone.now() - datetime.timedelta(hours=24)
    ex_poll = Poll.objects.filter(timestamp__lt=d)
    ex_poll.delete()