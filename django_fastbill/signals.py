from django.dispatch import Signal

customer_signal = Signal(providing_args=["customer", "data"])
subscription_signal = Signal(providing_args=["customer", "subscription", "data"])
payment_signal = Signal(providing_args=["customer", "subscription", "invoice", "data"])