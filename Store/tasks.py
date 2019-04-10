from __future__ import absolute_import, unicode_literals

from celery import shared_task

from django.core.mail import send_mail


@shared_task
def send_confirmation_order_mail(destination, subject, body):
    send_mail(
        subject,
        body,
        "onufryklaczynski@gmail.com",
        recipient_list=[destination],
    )
    return f'Email to {destination} of subject: {subject} sent.'