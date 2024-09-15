from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from datetime import datetime
from .models import Subscription

logger = logging.getLogger(__name__)

def deactivate_expired_subscriptions():
    today = datetime.now().date()
    subscriptions = Subscription.objects.filter(end_date__lt=today, status='active')

    for subscription in subscriptions:
        subscription.status = 'inactive'
        subscription.save()

    logger.info('Successfully updated subscription statuses')

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        deactivate_expired_subscriptions,
        trigger=CronTrigger(day="*", hour=0, minute=0),  # Runs every day at midnight
        id='deactivate_expired_subscriptions',
        replace_existing=True
    )

    scheduler.start()
    logger.info("Scheduler started successfully")

# Ensure the
