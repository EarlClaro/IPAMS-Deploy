# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import User

# @receiver(post_save, sender=User)
# def update_subscription_status(sender, instance, **kwargs):
#     # Avoid recursion in signals by checking if changes are needed
#     if instance.role_id >= 3:
#         if instance.is_subscribed != True or instance.subscription_status != "admin privilege":
#             instance.is_subscribed = True
#             instance.subscription_status = "admin privilege"
#             instance.save()
#     else:
#         if instance.is_subscribed != False or instance.subscription_status != "unpaid":
#             instance.is_subscribed = False
#             instance.subscription_status = "unpaid"
#             instance.save()