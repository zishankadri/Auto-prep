from django.conf import settings
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.utils import timezone


from django.shortcuts import get_object_or_404
from accounts.models import UserAccount
from django.dispatch import receiver
from accounts.utils import send_email

from customadmin.models import GeneralData


# @receiver(valid_ipn_received)
def show_me_the_money(sender, **kwargs):
    general_data = GeneralData.get_or_create()
    MONTHLY_PRICE = general_data.monthly_price
    YEARLY_PRICE = general_data.yearly_price
 
    ipn_obj = sender

    # user.subscription_status = "outside"
    # user.save()

    if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL: return  # Invalid payment
    if ipn_obj.mc_currency != 'USD':
        user = UserAccount.objects.get(id=ipn_obj.custom)
        user.subscriber_id = ipn_obj.subscr_id
        user.subscription_status = "Currency mismatch"

        return  # Invalid payment

    # Subscription creation
    if ipn_obj.txn_type == 'subscr_signup':
        user = UserAccount.objects.get(id=ipn_obj.custom)
        user.subscriber_id = ipn_obj.subscr_id

        if not valid_creation(ipn_obj, user, MONTHLY_PRICE, YEARLY_PRICE):
            user.subscription_status = "INVALID"
            user.save()
            return
            
        # Successful Transaction give the users what they want.
        user.is_paid_member = True
        user.subscription_status = "ACTIVE"
        # user.subsciption_period = ipn_obj.period3  # "1 M" or "1 Y"
        user.save()

        # Send Thank You email to user
        subject = f"Access Granted to {settings.SITE_NAME} Subscription!"
        message = f'''
                We are delighted to inform you that your payment for the {settings.SITE_NAME} subscription has been successfully processed. Your account is now active, and you can start using our service immediately.

                {settings.DEFAUL_DOMAIN}/classes/
                '''
        send_email(subject=subject, message=message, email=user.email)

    # Successful payment for recurring subscription
    elif ipn_obj.txn_type == "subscr_payment":
        user.subscription_status = "subscr_payment"

        # user = UserAccount.objects.get(subscriber_id=ipn_obj.subscr_id)
        user = UserAccount.objects.get(id=ipn_obj.custome)

        if not ipn_obj.payment_status == ST_PP_COMPLETED:
            return 

        user.is_paid_member = True
        # user.last_payment_date = timezone.localdate()
        
        user.save()

    # Subscription cancellation
    elif ipn_obj.txn_type == 'subscr_cancel':
        user = UserAccount.objects.get(subscriber_id=ipn_obj.subscr_id)
        user.subscription_status = "CANCELED"
        
    elif ipn_obj.txn_type == 'subscr_eot':
        user = UserAccount.objects.get(subscriber_id=ipn_obj.subscr_id)
        user.is_paid_member = False
        user.subscription_status = "ENDED"
        user.save()

valid_ipn_received.connect(show_me_the_money)

def valid_creation(ipn_obj, MONTHLY_PRICE, YEARLY_PRICE):
    if ipn_obj.recurring != "1": return False 

    if ipn_obj.period3 == "1 M":
        # Trial period duration check
        if ipn_obj.period1 != "1 M":
            return False
        # Trial period price check
        if ipn_obj.amount1 != MONTHLY_PRICE:
            return False
        # Regular subscription price check
        if ipn_obj.amount3 != MONTHLY_PRICE:
            return False 
        
    elif ipn_obj.period3 == "1 Y":
        # Trial period duration check
        if ipn_obj.period1 != "1 Y":
            return False
        # Trial period price check
        if ipn_obj.amount1 != YEARLY_PRICE:
            return False 
        # Regular subscription price check
        if ipn_obj.amount3 != YEARLY_PRICE:
            return False 
   
    return True


# def valid_transaction(ipn_obj, user):
#     user = UserAccount.objects.get(subscriber_id=ipn_obj.subscr_id)

#     if not ipn_obj.payment_status == ST_PP_COMPLETED:
#         return False
    
#     if user.subscription_status == "INVALID":
#         return False

#     return True



# Subscription Creation
# def handle_subscription_creation(ipn_obj):
# def handle_successful_payment(ipn_obj):
# def handle_subscription_cancellation(ipn_obj):
