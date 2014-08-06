from django.db import models
from .managers import FastBillApiManager
from django.contrib.auth.models import User
import logging
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class FastBillBase(models.Model):
    """

    """
    created_at = models.DateTimeField(auto_now=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    objects = FastBillApiManager()

    class Meta:
        abstract = True

    def get_customer(self, api_update_relations, customer_id):
        """
        """
        from .helper import get_customer_by_id
        if api_update_relations:
            return get_customer_by_id(customer_id)
        else:
            try:
                return Customer.objects.get(customer_id=customer_id)
            except Customer.DoesNotExist:
                return get_customer_by_id(customer_id)

    def get_user(self, customer_ext_uid):
        """
        """
        if customer_ext_uid in [0, "0"]:
            return None

        else:
            try:
                return User.objects.get(pk=customer_ext_uid)
            except User.DoesNotExist:
                logger.warning("User with pk %s does not exist. Customer object without relation created" %
                               customer_ext_uid)
                return None

    def get_subscription(self, api_update_relations, subscription_id):
        """
        """
        from .helper import get_subscription_by_id
        if api_update_relations:
            return get_subscription_by_id(subscription_id)
        else:
            try:
                return Subscription.objects.get(subscription_id=subscription_id)
            except Subscription.DoesNotExist:
                return get_subscription_by_id(subscription_id)

    def get_article(self, api_update_relations, article_number):
        """
        """
        from .helper import get_article_by_number
        if api_update_relations:
            return get_article_by_number(article_number)
        else:
            try:
                return Article.objects.get(article_number=article_number)
            except Article.DoesNotExist:
                return get_article_by_number(article_number)


class Article(FastBillBase):
    """

    """
    subscription_cancellation = models.CharField(max_length=50)
    article_number = models.IntegerField(primary_key=True)
    description = models.TextField()
    tags = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    unit_price = models.FloatField()
    is_addon = models.BooleanField()
    subscription_trial = models.CharField(max_length=50)
    subscription_interval = models.CharField(max_length=50)
    checkout_url = models.URLField(max_length=300)
    setup_fee = models.FloatField()
    subscription_duration_follow = models.CharField(max_length=50)
    return_url_success = models.URLField(max_length=300)
    vat_percent = models.FloatField()
    allow_multiple = models.BooleanField()
    return_url_cancel = models.URLField(max_length=300)
    subscription_number_events = models.IntegerField()
    currency_code = models.CharField(max_length=3)
    subscription_duration = models.CharField(max_length=50)

    def __unicode__(self):
        return u"Article, Number: %s Title %s" % (self.article_number, self.title)


class Customer(FastBillBase):
    """
    Crippled Customer Model. We only save needed data
    """

    customer_number = models.IntegerField()
    customer_ext_uid = models.IntegerField(null=True)
    customer_id = models.IntegerField(primary_key=True)

    dashboard_url = models.URLField(max_length=500)
    changedata_url = models.URLField(max_length=500)

    user = models.OneToOneField(User, null=True, related_name="fastbill_customer")

    def save(self, *args, **kwargs):
        """
        """
        if self.user is None:
            self.user = self.get_user(self.customer_ext_uid)

        super(Customer, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"Customer, ID: %s User: %s" % (self.customer_id, self.user)


class Subscription(FastBillBase):
    """

    """
    status = models.CharField(max_length=20)

    x_attributes = models.TextField()
    invoice_title = models.CharField(max_length=300)
    cancellation_date = models.DateTimeField(null=True)
    expiration_date = models.DateTimeField()
    last_event = models.DateTimeField()
    start = models.DateTimeField()
    subscription_ext_uid = models.IntegerField(null=True)
    next_event = models.DateTimeField()
    article_number = models.IntegerField()
    subscription_id = models.IntegerField(primary_key=True)
    customer_id = models.IntegerField()
    quantity = models.IntegerField()

    fastbill_customer = models.ForeignKey(Customer, null=True, related_name="subscriptions")
    fastbill_article = models.ForeignKey(Article, null=True, related_name="subscriptions")

    @property
    def customer(self):
        """
        """
        return self.fastbill_customer

    @property
    def article(self):
        """
        """
        return self.fastbill_article

    def save(self, api_update_relations=False, *args,  **kwargs):
        """
        """
        super(Subscription, self).save(*args, **kwargs)

        old_cust, old_article = self.fastbill_customer, self.fastbill_article
        if self.fastbill_customer is None or api_update_relations:
            self.fastbill_customer = self.get_customer(api_update_relations, self.customer_id)
        if self.fastbill_article is None or api_update_relations:
            self.fastbill_article = self.get_article(api_update_relations, self.article_number)

        if old_cust != self.fastbill_customer or old_article != self.fastbill_article:
            # resave if something changed
            super(Subscription, self).save(*args, **kwargs)

    def __unicode__(self):
        return "Subscription, ID: %s customer %s" % (self.subscription_id, self.customer)


class Invoice(FastBillBase):
    """

    """
    cash_discount_percent = models.FloatField()
    affiliate = models.CharField(max_length=10)
    payment_type = models.CharField(max_length=2)
    introtext = models.TextField()
    due_date = models.DateTimeField()
    subscription_invoice_counter = models.IntegerField()
    is_canceled = models.BooleanField()
    paypal_url = models.URLField(max_length=500)
    cash_discount_days = models.IntegerField()
    invoice_date = models.DateTimeField()
    paid_date = models.DateTimeField(null=True)
    country_code = models.CharField(max_length=2)
    customer_id = models.IntegerField()
    currency_code = models.CharField(max_length=3)
    invoice_id = models.IntegerField(primary_key=True)
    sub_total = models.FloatField()
    days_for_payment = models.IntegerField()
    document_url = models.URLField(max_length=500)
    invoice_number = models.CharField(max_length=300)
    total = models.FloatField()
    customer_number = models.IntegerField()
    invoice_title = models.CharField(max_length=300)
    delivery_date = models.CharField(max_length=300)
    subscription_id = models.IntegerField()
    type = models.CharField(max_length=30)
    vat_total = models.FloatField()
    template_id = models.IntegerField()

    fastbill_customer = models.ForeignKey(Customer, null=True, related_name="invoices")
    fastbill_subscription = models.ForeignKey(Subscription, null=True, related_name="invoices")

    def get_payment_type(self):
        if self.payment_type == "1":
            return _("money transfer")
        elif self.payment_type == "2":
            return _("direct debit")
        elif self.payment_type == "3":
            return _("bar")
        elif self.payment_type == "4":
            return _("pay pal")
        elif self.payment_type == "5":
            return _("cash in advance")
        elif self.payment_type == "6":
            return _("credit card")
        return _("other")

    @property
    def customer(self):
        """

        :return:
        """
        return self.fastbill_customer

    @property
    def subscription(self):
        """

        :return:
        """
        return self.fastbill_subscription

    def save(self, api_update_relations=False, *args, **kwargs):
        """

        :param api_update_relations:
        :param args:
        :param kwargs:
        :return:
        """
        super(Invoice, self).save(*args, **kwargs)

        old_cust, old_sub = self.fastbill_customer, self.fastbill_subscription

        if self.fastbill_customer is None or api_update_relations:
            self.fastbill_customer = self.get_customer(api_update_relations, self.customer_id)

        if self.fastbill_subscription is None or api_update_relations:
            self.fastbill_subscription = self.get_subscription(api_update_relations, self.subscription_id)

        if old_cust != self.fastbill_customer or old_sub != self.fastbill_subscription:
            # resave if something changed
            super(Invoice, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"Invoice, ID:%s Number: %s" % (self.invoice_id, self.invoice_number)