import logging
from fastbill import FastbillWrapper
from django.conf import settings

logger = logging.getLogger(__name__)


def get_connection():
    """

    :return:
    """
    return FastbillWrapper(settings.FASTBILL_EMAIL, settings.FASTBILL_API_KEY)


def get_customer_by_id(customer_id):
    """

    :param customer_id:
    :return:
    """
    from .models import Customer
    from .exceptions import ConvertError

    try:
        result = get_connection().customer_get(filter={"CUSTOMER_ID": customer_id})
        created, customer = Customer.objects.update_or_create(result["CUSTOMERS"][0])
        if int(customer.customer_id) != int(customer_id):
            logger.warning("Fastbill returned the wrong customer id. Asked for %s but got %s" % (customer_id,
                                                                                                 customer.customer_id))
            return None
        return customer
    except (IndexError, ValueError, ConvertError) as e:
        logger.warning("Could not fetch customer with customer_id %s, error: %s" % (customer_id, e))
    return None


def get_subscription_by_id(subscription_id):
    """

    :param subscription_id:
    :return:
    """
    from .models import Subscription
    from .exceptions import ConvertError

    try:
        result = get_connection().subscription_get(filter={"SUBSCRIPTION_ID": subscription_id})
        created, sub = Subscription.objects.update_or_create(result["SUBSCRIPTIONS"][0])
        if int(sub.subscription_id) != int(subscription_id):
            logger.warning("Fastbill returned the wrong subscription id. Asked for %s but got %s" % (subscription_id,
                                                                                                 sub.subscription_id))
            return None
        return sub
    except (IndexError, ValueError, ConvertError) as e:
        logger.warning("Could not fetch subscription with subscription_id %s, error: %s" % (subscription_id, e))
    return None


def get_invoice_by_id(invoice_id):
    """

    :param invoice_id:
    :return:
    """
    from .models import Invoice
    from .exceptions import ConvertError

    try:
        result = get_connection().invoice_get(filter={"INVOICE_ID": invoice_id})
        created, invoice = Invoice.objects.update_or_create(result["INVOICES"][0])
        if int(invoice.invoice_id) != int(invoice_id):
            logger.warning("Fastbill returned the wrong invoice id. Asked for %s but got %s" % (invoice_id,
                                                                                                 invoice.invoice_id))
            return None
        return invoice
    except (IndexError, ValueError, ConvertError) as e:
        logger.warning("Could not fetch subscription with subscription_id %s, error: %s" % (invoice_id, e))
    return None


def get_article_by_number(article_number):
    """

    :param article_number:
    :return:
    """
    from .models import Article
    from .exceptions import ConvertError

    try:
        result = get_connection().article_get(filter={"ARTICLE_NUMBER": article_number})
        created, article = Article.objects.update_or_create(result["ARTICLES"][0])
        if int(article.article_number) != int(article_number):
            logger.warning("Fastbill returned the wrong article number. Asked for %s but got %s" % (article_number,
                                                                                                 article.article_number))
            return None
        return article
    except (IndexError, ValueError, ConvertError) as e:
        logger.warning("Could not fetch article with article_number %s, error: %s" % (article_number, e))
    return None


def get_articles():
    from .models import Article
    from .exceptions import ConvertError

    for api_item in get_connection().article_get():
        try:
            created, article = Article.objects.update_or_create(api_item)
        except ConvertError, e:
            logger.warning("Could not fetch article: %s" % e)

