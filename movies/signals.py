from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.dispatch import receiver
from django.conf import settings

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens. When a token is created, an e-mail is sent to the
    user.
    """
    # URL v e-mailu musí odkazovat na frontendovou aplikaci
    # Frontend bude mít stránku /reset-password, která přijme token jako parametr
    # Pro lokální vývoj předpokládáme, že frontend běží na portu 3000
    reset_url = f"http://localhost:3000/?page=reset-password&token={reset_password_token.key}"

    email_plaintext_message = (
        f"Hello {reset_password_token.user.username},\n\n"
        f"You requested a password reset for your CineSmart account.\n"
        f"Please go to the following link to reset your password:\n\n"
        f"{reset_url}\n\n"
        f"If you did not request this, please ignore this email.\n"
    )

    send_mail(
        # title:
        "Password Reset for CineSmart",
        # message:
        email_plaintext_message,
        # from:
        settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else "noreply@cinesmart.com",
        # to:
        [reset_password_token.user.email]
    )

