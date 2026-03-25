from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import *
from django.core.mail import send_mail

@receiver(post_save,sender=User)
def send_mail_for_user(sender,instance,created,**kwargs):
    if created:
         send_mail('registration',
            'Thanks for registartion,your registration is Successfull',
            'pothireddy2002@gmail.com',
            [instance.email],
            fail_silently=False
            )
