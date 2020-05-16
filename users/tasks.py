import logging
from typing import List
from conf.celery import app
from django.core.mail import send_mail


logger = logging.getLogger(__name__)


@app.task()
def send_email(subject: str, message: str, html_message: str, from_email: str,
               to: List):
    """
    Send email
    :return:
    """
    logger.info(f'Sent email "{subject}" to "{to}"')
    send_mail(
        subject=subject,
        message=message,
        html_message=html_message,
        from_email=from_email,
        recipient_list=to
    )
