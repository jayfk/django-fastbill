management commands

python manage.py fastbill --update-articles


signals

put this in your models.py

from django_fastbill.signals import customer_signal, subscription_signal, payment_signal
from django.dispatch import receiver


@receiver(customer_signal)
def customer_signal_receiver(sender, customer, event_type, raw_data, **kwargs):
    print "#" * 50
    print "sender", sender
    print "event_type", event_type
    print "customer", customer
    print "data", raw_data
    print "#" * 50


@receiver(subscription_signal)
def subscription_signal_receiver(sender, customer, subscription, event_type, raw_data, **kwargs):
    print "#" * 50
    print "sender", sender
    print "event_type", event_type
    print "customer", customer
    print "subscription", subscription
    print "data", raw_data
    print "#" * 50

@receiver(payment_signal)
def payment_signal_receiver(sender, customer, subscription, invoice, event_type, raw_data, **kwargs):
    print "#" * 50
    print "sender", sender
    print "event_type", event_type
    print "customer", customer
    print "subscription", subscription
    print "invoice", invoice
    print "data", raw_data
    print "#" * 50