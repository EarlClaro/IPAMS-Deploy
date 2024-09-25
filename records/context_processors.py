from datetime import datetime, timedelta
from .models import Subscription

def subscription_status(request):
    if request.user.is_authenticated:
        subscription = request.user.get_subscription()
        show_modal = subscription.is_near_end() and subscription.plan_id_id in [2, 3] if subscription else False
        if subscription:
            # Use locked_plan_name to show the subscribed plan, not the updated one
            plan_name = subscription.locked_plan_name if subscription.locked_plan_name else 'Free'
        else:
            plan_name = 'Free'
        return {'show_modal': show_modal, 'subscription_plan_name': plan_name}
    return {'show_modal': False, 'subscription_plan_name': 'Free'}
