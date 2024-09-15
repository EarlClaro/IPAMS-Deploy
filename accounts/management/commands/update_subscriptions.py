# from django.core.management.base import BaseCommand
# from accounts.models import User

# class Command(BaseCommand):
#     help = 'Update subscription status for users with role_id >= 3'

#     def handle(self, *args, **kwargs):
#         users = User.objects.filter(role_id__gte=3)
#         for user in users:
#             if user.is_subscribed != True or user.subscription_status != 'admin privilege':
#                 user.is_subscribed = True
#                 user.subscription_status = 'admin privilege'
#                 user.save()

#         self.stdout.write(self.style.SUCCESS('Successfully updated subscription status for users with role_id >= 3'))