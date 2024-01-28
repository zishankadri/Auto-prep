from .utils import send_email

def send_verification_email(email, auth_token, domain_name):
    subject = "Verify your email for < site name >"
    message = f'''
            Verify your email for < Site Name > by clicking :- 
            {domain_name}/accounts/verify_email/{auth_token}/
            '''
    send_email(subject=subject, message=message, email=email)



# def send_verification_email(email, auth_token):
#     email_from = settings.EMAIL_HOST_USER

#     subject = "Verify your email address"
#     message = f"Verify your email for Algostockz by clicking :- {domain_name}/accounts/verify/{auth_token}/"
#     recipient_list = [email, ]
    
#     send_mail(subject, message, email_from, recipient_list, fail_silently = False)

# def changing_email_verificatin(email, auth_token):
#     email_from = settings.EMAIL_HOST_USER

#     subject = "Verify your email address"
#     message = f"Verify your email for Algostockz by clicking :- {domain_name}/accounts/change_email_final/{auth_token}/"
#     recipient_list = [email, ]
    
#     send_mail(subject, message, email_from, recipient_list, fail_silently = False)


# def send_change_password_email(email, auth_token):
#     email_from = settings.EMAIL_HOST_USER

#     subject = "Change Password"
#     message = f"Change password for Algostockz by clicking :- {domain_name}/accounts/change_password/{auth_token}/"
#     recipient_list = [email, ]
    
#     send_mail(subject, message, email_from, recipient_list, fail_silently = False)


# def send_change_email_email(email, auth_token):
#     email_from = settings.EMAIL_HOST_USER

#     subject = "Change Email"
#     message = f"Change Email for Algostockz by clicking :- {domain_name}/accounts/change_email/{auth_token}/"
#     recipient_list = [email, ]
    
#     send_mail(subject, message, email_from, recipient_list, fail_silently = False)

