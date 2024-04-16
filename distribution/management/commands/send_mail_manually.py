from django.core.management import BaseCommand

from distribution.tasks import send_email, finalize_mailing_event


class Command(BaseCommand):
    help = 'Manually send a mailing event'

    def add_arguments(self, parser):
        parser.add_argument('mailing_event_id', type=int, help='ID of the mailing event to send')

    def handle(self, *args, **options):
        mailing_event_id = options['mailing_event_id']
        send_mailing_event(mailing_event_id)
        self.stdout.write(self.style.SUCCESS(f'Mailing event {mailing_event_id} sent successfully.'))


def send_mailing_event(mailing_event_id):
    """Функция для отправки рассылки вручную"""

    send_email.delay(mailing_event_id)
    finalize_mailing_event.apply_async(args=[mailing_event_id])

    return
