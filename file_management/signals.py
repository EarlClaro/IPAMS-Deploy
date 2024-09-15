# yourapp/signals.py

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import LoginEvent
from django.utils import timezone
@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    # Create a LoginEvent instance for the logged-in user
    LoginEvent.objects.create(user=user)

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    # Update the log_out_time when a user logs out
    login_event = LoginEvent.objects.filter(user=user, log_out_time__isnull=True).first()
    if login_event:
        login_event.log_out_time = timezone.now()
        login_event.save()