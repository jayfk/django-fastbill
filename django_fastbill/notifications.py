from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import base64
from .helper import get_customer_by_id, get_subscription_by_id, get_invoice_by_id
from .models import Customer
from .signals import customer_signal, subscription_signal, payment_signal

import logging
from django.dispatch import Signal

NOTIFICATIONS = [
    "customer.created",
    "customer.changed",
    "customer.deleted",
    "subscription.created",
    "subscription.changed",
    "subscription.canceled",
    "subscription.closed",
    "subscription.reactivate",
    "payment.created",
    "payment.failed",
    "payment.chargeback",
    "payment.refunded",
]

logger = logging.getLogger(__name__)

@csrf_exempt
def notification_view(request):
    # authorize using basic authentication
    logger.info("Fastbill notification received")
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == "basic":
                uname, passwd = base64.b64decode(auth[1]).split(':')
                if uname == settings.FASTBILL_NOTIFICATION_USERNAME and \
                passwd == settings.FASTBILL_NOTIFICATION_PASSWORD:
                    # notification is authorized, load json
                    data = json.loads(request.body)
                    if data["type"] in NOTIFICATIONS:
                        # call the function
                        if "payment" in data["type"]:
                            payment_signal.send(
                                sender=__name__,
                                customer=get_customer_by_id(data["customer"]["customer_id"]),
                                subscription=get_subscription_by_id(data["subscription"]["subscription_id"]),
                                invoice=get_invoice_by_id(data["payment"]["invoice_id"]),
                                event_type=data["type"],
                                raw_data=data
                            )
                        elif "subscription" in data["type"]:
                            subscription_signal.send(
                                sender=__name__,
                                customer=get_customer_by_id(data["customer"]["customer_id"]),
                                subscription=get_subscription_by_id(data["subscription"]["subscription_id"]),
                                event_type=data["type"],
                                raw_data=data
                            )
                        elif "customer" in data["type"]:
                            customer = get_customer_by_id(data["customer"]["customer_id"])

                            # delete the customer if we have a delete signal
                            if customer is not None and "delete" in data["type"]:
                                customer.delete()
                                customer = None

                            customer_signal.send(
                                sender=__name__,
                                customer=customer,
                                event_type=data["type"],
                                raw_data=data
                            )

                    else:
                        logging.warning("Unrecognized notification received: %s" % data["type"])
                        return HttpResponse(status=401)

                    logger.info("Fastbill Notification processed")
                    return HttpResponse("ok")

    logger.info("Could not process Fastbill Notifcation. Unknown Error.")
    return HttpResponse(status=401)
