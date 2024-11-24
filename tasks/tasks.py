from celery import shared_task
from django.core.mail import send_mail
from .models import Email

@shared_task(bind=True, max_retries=3)
def send_email_task(self, email_id):
    try:
        email = Email.objects.get(id=email_id)
        send_mail(
            email.subject,
            email.body,
            'from@example.com',
            [email.recipient],
            fail_silently=False,
        )
        email.sent = True
        email.save()
    except Exception as e:
        self.retry(exc=e, countdown=60)  # Retry after 1 minute

