import json
import smtplib

from celery import shared_task, current_app
from django.core.mail import send_mail
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from config import settings

from distribution.models import MailingEvent, Client, Log
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_email(mailing_event_id):
    """ Задача на рассылку"""

    mailing_event = MailingEvent.objects.get(id=mailing_event_id)

    if mailing_event.status == 'created':
        mailing_event.status = 'started'
        mailing_event.save(update_fields=['status'])

        clients = Client.objects.filter(owner=mailing_event.owner)

        for client in clients:
            try:
                send_mail(
                    subject=mailing_event.message.subject,
                    message=mailing_event.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False,
                )

                Log.objects.create(
                    message=mailing_event.message,
                    owner=mailing_event.owner,
                    status='success',
                    response='Email sent successfully',
                    client=client

                )
            except smtplib.SMTPException as e:

                Log.objects.create(
                    message=mailing_event.message,
                    owner=mailing_event.owner,
                    status='failed',
                    response=str(e),
                    client=client
                )

            except Exception as e:

                Log.objects.create(
                    message=mailing_event.message,
                    owner=mailing_event.owner,
                    status='failed',
                    response=str(e),
                    client=client
                )


@shared_task
def finalize_mailing_event(mailing_event_id):
    """Задача на изменение статуса при окончании рассылки"""
    mailing_event = MailingEvent.objects.get(id=mailing_event_id)
    if mailing_event.end_time <= timezone.now():
        mailing_event.status = 'completed'
        # mailing_event.is_active = False
        mailing_event.save(update_fields=['status'])


def schedule_email_task(mailing_event):
    """Планирование задачи рассылки и завершения рассылки"""
    start_time = mailing_event.start_time
    task_name = None
    one_off = None
    day_of_week = '*'
    day_of_month = None
    month_of_year = None
    should_send_immediately = False

    if start_time <= timezone.now() and mailing_event.is_active:
        should_send_immediately = True

    if mailing_event.frequency == 'once':
        day_of_month = start_time.day
        month_of_year = start_time.month
        task_name = f'Send Mailing Event {mailing_event.id} Emails'
        one_off = True

    elif mailing_event.frequency == 'daily':
        day_of_month = '*'
        month_of_year = '*'
        task_name = f'Send Mailing Event {mailing_event.id} Emails Daily'
        one_off = False

    elif mailing_event.frequency == 'weekly':
        day_of_week = start_time.strftime('%w')
        month_of_year = '*'
        task_name = f'Send Mailing Event {mailing_event.id} Emails Weekly'
        one_off = False

    elif mailing_event.frequency == 'monthly':
        day_of_month = start_time.day
        month_of_year = '*'
        task_name = f'Send Mailing Event {mailing_event.id} Emails Monthly'
        one_off = False

    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=start_time.minute,
        hour=start_time.hour,
        day_of_week=day_of_week,
        day_of_month=day_of_month,
        month_of_year=month_of_year,

    )

    task, created = PeriodicTask.objects.get_or_create(
        name=task_name,
        defaults={
            'crontab': schedule,
            'task': 'distribution.tasks.send_email',
            'args': json.dumps([mailing_event.id]),
            'one_off': one_off,
            'expires': mailing_event.end_time
        }
    )
    if not created:
        task.crontab = schedule
        task.args = json.dumps([mailing_event.id])
        task.one_off = one_off
        task.expires = mailing_event.end_time
        task.save(update_fields=['crontab', 'args', 'one_off', 'expires'])

    if should_send_immediately:
        send_email.delay(mailing_event.id)

    finalize_task = current_app.send_task('distribution.tasks.finalize_mailing_event', args=[mailing_event.id],
                                          eta=mailing_event.end_time)

    return task, finalize_task
