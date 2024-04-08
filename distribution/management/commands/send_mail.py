from distribution.tasks import send_email, finalize_mailing_event


def send_mailing_event(mailing_event_id):
    """Функция для отправки рассылки вручную"""

    send_email.delay(mailing_event_id)
    finalize_mailing_event.apply_async(args=[mailing_event_id])

    return
