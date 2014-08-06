# -*- coding: utf-8 -*-
from django.test import TestCase, TransactionTestCase
from .models import Article, Customer, Subscription, Invoice
from .exceptions import ConvertError
from mock import Mock, patch
from datetime import datetime
from pytz import tzinfo, timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.conf import settings
import json


class FastbillTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="foo", pk=1)
        print "@" * 40
        for user in User.objects.all():
            print user.pk
        print "@" * 40


class UpdateOrCreateTestCase(FastbillTestCase):
    def test_article(self):
        api_items = [
            {u'SUBSCRIPTION_CANCELLATION': 0, u'ARTICLE_NUMBER': u'1', u'DESCRIPTION': u'', u'TAGS': u'',
             u'TITLE': u'Test', u'TRANSLATIONS': [], u'UNIT_PRICE': u'10.0000', u'IS_ADDON': u'0',
             u'SUBSCRIPTION_TRIAL': 0, u'SUBSCRIPTION_INTERVAL': u'1 month',
             u'CHECKOUT_URL': u'https://automatic.fastbill.com/purchase/4751862ae058864485a7722930137c9f/1',
             u'SETUP_FEE': u'0.0000', u'SUBSCRIPTION_DURATION_FOLLOW': 0, u'RETURN_URL_SUCCESS': u'',
             u'VAT_PERCENT': u'19.00', u'ALLOW_MULTIPLE': u'0', u'RETURN_URL_CANCEL': u'',
             u'SUBSCRIPTION_NUMBER_EVENTS': u'0', u'CURRENCY_CODE': u'EUR', u'SUBSCRIPTION_DURATION': 0},
            {u'SUBSCRIPTION_CANCELLATION': 0, u'ARTICLE_NUMBER': u'2', u'DESCRIPTION': u'', u'TAGS': u'',
             u'TITLE': u'Testprodukt 2', u'TRANSLATIONS': [], u'UNIT_PRICE': u'20.0000', u'IS_ADDON': u'0',
             u'SUBSCRIPTION_TRIAL': 0, u'SUBSCRIPTION_INTERVAL': u'1 month',
             u'CHECKOUT_URL': u'https://automatic.fastbill.com/purchase/4751862ae058864485a7722930137c9f/2',
             u'SETUP_FEE': u'0.0000', u'SUBSCRIPTION_DURATION_FOLLOW': 0, u'RETURN_URL_SUCCESS': u'',
             u'VAT_PERCENT': u'19.00', u'ALLOW_MULTIPLE': u'0', u'RETURN_URL_CANCEL': u'',
             u'SUBSCRIPTION_NUMBER_EVENTS': u'0', u'CURRENCY_CODE': u'EUR', u'SUBSCRIPTION_DURATION': 0}
        ]

        # create and check
        created, article = Article.objects.update_or_create(api_items[0])

        self.assertEqual(created, True)
        self.assertEqual(article.subscription_cancellation, 0)
        self.assertEqual(article.title, "Test")
        self.assertEqual(article.article_number, 1)
        self.assertEqual(article.description, '')
        self.assertEqual(article.tags, '')
        self.assertEqual(article.unit_price, 10.000)

        self.assertEqual(article.is_addon, False)
        self.assertEqual(article.subscription_trial, 0)
        self.assertEqual(article.subscription_interval, "1 month")
        self.assertEqual(article.checkout_url,
                         "https://automatic.fastbill.com/purchase/4751862ae058864485a7722930137c9f/1")
        self.assertEqual(article.setup_fee, 0.000)
        self.assertEqual(article.subscription_duration_follow, 0)
        self.assertEqual(article.return_url_success, "")
        self.assertEqual(article.vat_percent, 19.00)
        self.assertEqual(article.allow_multiple, False)
        self.assertEqual(article.return_url_cancel, "")
        self.assertEqual(article.subscription_number_events, 0)
        self.assertEqual(article.currency_code, "EUR")
        self.assertEqual(article.subscription_duration, 0)

        # call again
        created, article = Article.objects.update_or_create(api_items[0])
        self.assertEqual(created, False)

        # check that we have the item in db now
        article = Article.objects.get(article_number=1)

    def test_customer(self):
        api_items = [
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Bjarne', u'LAST_NAME': u'Riis', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'13,00', u'ZIPCODE': u'5467890',
             u'BANK_ACCOUNT_MANDATE_REFERENCE': u'', u'AFFILIATE': u'', u'PAYMENT_TYPE': u'4', u'LANGUAGE_CODE': u'de',
             u'EMAIL': u'foo@bar.com', u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'',
             u'TAGS': u'', u'PHONE': u'', u'CUSTOMER_TYPE': u'consumer',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/d2045f88905d7e7d206eef3b0d869829',
             u'COUNTRY_CODE': u'DE', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'', u'CUSTOMER_ID': u'692708',
             u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'PAYPAL_BILLINGAGREEMENTID': u'',
             u'X_ATTRIBUTES': u'', u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'd2045f88905d7e7d206eef3b0d869829',
             u'BANK_BIC': u'', u'CREATED': u'2014-07-21 12:20:22', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-21 12:20:22',
             u'SALUTATION': u'mr', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'Example City',
             u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/d2045f88905d7e7d206eef3b0d869829',
             u'CUSTOMER_NUMBER': u'1', u'VAT_ID': u'', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Foostrasse 12',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''},
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Steffen', u'LAST_NAME': u'Simon', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'0,00', u'ZIPCODE': u'5467890',
             u'BANK_ACCOUNT_MANDATE_REFERENCE': u'', u'AFFILIATE': u'', u'PAYMENT_TYPE': u'4', u'LANGUAGE_CODE': u'de',
             u'EMAIL': u'foo@bar.com', u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'',
             u'TAGS': u'', u'PHONE': u'', u'CUSTOMER_TYPE': u'consumer',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/283fd3d8bcc205564f2b970ea978aa3c',
             u'COUNTRY_CODE': u'DE', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'', u'CUSTOMER_ID': u'692738',
             u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'PAYPAL_BILLINGAGREEMENTID': u'',
             u'X_ATTRIBUTES': u'', u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'283fd3d8bcc205564f2b970ea978aa3c',
             u'BANK_BIC': u'', u'CREATED': u'2014-07-21 12:40:32', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-21 12:40:32',
             u'SALUTATION': u'mr', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'Example City',
             u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/283fd3d8bcc205564f2b970ea978aa3c',
             u'CUSTOMER_NUMBER': u'2', u'VAT_ID': u'', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Foostrasse 12',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''},
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Johnny', u'LAST_NAME': u'Giraffaloe', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'0,00', u'ZIPCODE': u'5467890',
             u'BANK_ACCOUNT_MANDATE_REFERENCE': u'', u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'LANGUAGE_CODE': u'de',
             u'EMAIL': u'foo@bar.com', u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'', u'TAGS': u'',
             u'PHONE': u'', u'CUSTOMER_TYPE': u'business',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/40b6307fb087009dda6a192b2f6e379d',
             u'COUNTRY_CODE': u'DE', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'Johnne',
             u'CUSTOMER_ID': u'693080', u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'X_ATTRIBUTES': u'',
             u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'40b6307fb087009dda6a192b2f6e379d', u'BANK_BIC': u'',
             u'CREATED': u'2014-07-21 17:09:56', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-21 17:09:56',
             u'SALUTATION': u'mr', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'Example City',
             u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/40b6307fb087009dda6a192b2f6e379d',
             u'CUSTOMER_NUMBER': u'3', u'VAT_ID': u'', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Foostrasse 12',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''},
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Foo', u'LAST_NAME': u'Bar', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'0,00', u'ZIPCODE': u'Bar', u'BANK_ACCOUNT_MANDATE_REFERENCE': u'',
             u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'LANGUAGE_CODE': u'de', u'EMAIL': u'foo@bar.com',
             u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'', u'TAGS': u'', u'PHONE': u'',
             u'CUSTOMER_TYPE': u'business',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/2f956a511f76b65f7da9bb89b03dfbc7',
             u'COUNTRY_CODE': u'DE', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'Oliver',
             u'CUSTOMER_ID': u'693096', u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'X_ATTRIBUTES': u'',
             u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'2f956a511f76b65f7da9bb89b03dfbc7', u'BANK_BIC': u'',
             u'CREATED': u'2014-07-21 17:18:07', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-21 17:18:07',
             u'SALUTATION': u'', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'Foooofo', u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/2f956a511f76b65f7da9bb89b03dfbc7',
             u'CUSTOMER_NUMBER': u'4', u'VAT_ID': u'', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Foo',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''},
        ]

        from django.core.exceptions import ObjectDoesNotExist

        created, customer = Customer.objects.update_or_create(api_items[0])
        self.assertEqual(created, True)
        self.assertEqual(customer.customer_ext_uid, 1)
        self.assertEqual(customer.customer_number, 1)
        self.assertEqual(customer.customer_id, 692708)
        self.assertEqual(customer.user.pk, customer.customer_ext_uid)

        self.assertEqual(
            customer.dashboard_url,
            "https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/d2045f88905d7e7d206eef3b0d869829"
        )

        self.assertEqual(
            customer.changedata_url,
            "https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/d2045f88905d7e7d206eef3b0d869829"
        )

        customer.user.delete()

        with self.assertRaises(ObjectDoesNotExist):
            Customer.objects.get(customer_number=1)

        created, customer = Customer.objects.update_or_create(api_items[1])
        self.assertEqual(created, True)
        self.assertEqual(customer.customer_ext_uid, 1)
        self.assertEqual(customer.customer_number, 2)
        self.assertEqual(customer.customer_id, 692738)
        self.assertEqual(customer.user, None)

    @patch("fastbill.FastbillWrapper._request")
    def test_subscription(self, mocked_call):
        api_items = [
            {u'STATUS': u'active', u'X_ATTRIBUTES': u'', u'INVOICE_TITLE': u'',
             u'HASH': u'5b69eec0ec71a95f976e9cd7c784d8d9', u'CANCELLATION_DATE': u'2014-08-21 00:00:00',
             u'EXPIRATION_DATE': u'2014-08-21 00:00:00', u'LAST_EVENT': u'2014-07-21 12:40:32',
             u'START': u'2014-07-21 12:40:32', u'SUBSCRIPTION_EXT_UID': u'1', u'NEXT_EVENT': u'2014-08-01 00:00:00',
             u'ARTICLE_NUMBER': u'1', u'SUBSCRIPTION_ID': 312414, u'CUSTOMER_ID': 692738, u'ADDONS': [],
             u'QUANTITY': u'1'},
            {u'STATUS': u'active', u'X_ATTRIBUTES': u'', u'INVOICE_TITLE': u'',
             u'HASH': u'0d124afc9c8758be0076bd5921c77346', u'CANCELLATION_DATE': u'0000-00-00 00:00:00',
             u'EXPIRATION_DATE': u'2014-08-21 12:20:22', u'LAST_EVENT': u'2014-07-21 12:20:22',
             u'START': u'2014-07-21 12:20:22', u'SUBSCRIPTION_EXT_UID': u'1', u'NEXT_EVENT': u'2014-08-21 12:20:22',
             u'ARTICLE_NUMBER': u'1', u'SUBSCRIPTION_ID': 312392, u'CUSTOMER_ID': 692708, u'ADDONS': [],
             u'QUANTITY': u'1'},
            {u'STATUS': u'active', u'X_ATTRIBUTES': u'', u'INVOICE_TITLE': u'',
             u'HASH': u'0c86d1059605ea425f5bd6e1362d1063', u'CANCELLATION_DATE': u'0000-00-00 00:00:00',
             u'EXPIRATION_DATE': u'2014-08-21 17:09:56', u'LAST_EVENT': u'2014-07-21 17:09:56',
             u'START': u'2014-07-21 17:09:56', u'SUBSCRIPTION_EXT_UID': u'1', u'NEXT_EVENT': u'2014-08-21 17:09:56',
             u'ARTICLE_NUMBER': u'2', u'SUBSCRIPTION_ID': 312714, u'CUSTOMER_ID': 693080, u'ADDONS': [],
             u'QUANTITY': u'1'},
            {u'STATUS': u'active', u'X_ATTRIBUTES': u'', u'INVOICE_TITLE': u'',
             u'HASH': u'32a0045463b22e72f82e60718ad673ca', u'CANCELLATION_DATE': u'0000-00-00 00:00:00',
             u'EXPIRATION_DATE': u'2014-08-21 17:18:07', u'LAST_EVENT': u'2014-07-21 17:18:07',
             u'START': u'2014-07-21 17:18:07', u'SUBSCRIPTION_EXT_UID': u'1', u'NEXT_EVENT': u'2014-08-21 17:18:07',
             u'ARTICLE_NUMBER': u'2', u'SUBSCRIPTION_ID': 312728, u'CUSTOMER_ID': 693096, u'ADDONS': [],
             u'QUANTITY': u'1'},
        ]

        customer_call = {u'CUSTOMERS': [
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Johnny', u'LAST_NAME': u'Giraffaloe', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'0,00', u'ZIPCODE': u'5467890',
             u'BANK_ACCOUNT_MANDATE_REFERENCE': u'', u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'LANGUAGE_CODE': u'de',
             u'EMAIL': u'foo@bar.com', u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'', u'TAGS': u'',
             u'PHONE': u'', u'CUSTOMER_TYPE': u'business',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/40b6307fb087009dda6a192b2f6e379d',
             u'COUNTRY_CODE': u'DE', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'Johnne',
             u'CUSTOMER_ID': u'692738', u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'X_ATTRIBUTES': u'',
             u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'40b6307fb087009dda6a192b2f6e379d', u'BANK_BIC': u'',
             u'CREATED': u'2014-07-21 17:09:56', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-21 17:09:56',
             u'SALUTATION': u'mr', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'Example City',
             u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/40b6307fb087009dda6a192b2f6e379d',
             u'CUSTOMER_NUMBER': u'3', u'VAT_ID': u'', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Foostrasse 12',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''}]}

        article_call = {u'ARTICLES': [
            {u'SUBSCRIPTION_CANCELLATION': 0, u'ARTICLE_NUMBER': u'1', u'DESCRIPTION': u'', u'TAGS': u'',
             u'TITLE': u'Test', u'TRANSLATIONS': [], u'UNIT_PRICE': u'10.0000', u'IS_ADDON': u'0',
             u'SUBSCRIPTION_TRIAL': 0, u'SUBSCRIPTION_INTERVAL': u'1 month',
             u'CHECKOUT_URL': u'https://automatic.fastbill.com/purchase/4751862ae058864485a7722930137c9f/1',
             u'SETUP_FEE': u'0.0000', u'SUBSCRIPTION_DURATION_FOLLOW': 0, u'RETURN_URL_SUCCESS': u'',
             u'VAT_PERCENT': u'19.00', u'ALLOW_MULTIPLE': u'0', u'RETURN_URL_CANCEL': u'',
             u'SUBSCRIPTION_NUMBER_EVENTS': u'0', u'CURRENCY_CODE': u'EUR', u'SUBSCRIPTION_DURATION': 0}]}

        mocked_call.side_effect = [
            customer_call,
            article_call
        ]

        created, sub = Subscription.objects.update_or_create(api_items[0])
        self.assertEqual(created, True)
        self.assertEqual(sub.status, "active")
        self.assertEqual(sub.x_attributes, "")
        self.assertEqual(sub.invoice_title, "")
        self.assertEqual(sub.cancellation_date, datetime(2014, 8, 21, tzinfo=timezone("UTC")))
        self.assertEqual(sub.expiration_date, datetime(2014, 8, 21, tzinfo=timezone("UTC")))
        self.assertEqual(sub.last_event, datetime(2014, 7, 21, 12, 40, 32, tzinfo=timezone("UTC")))
        self.assertEqual(sub.start, datetime(2014, 7, 21, 12, 40, 32, tzinfo=timezone("UTC")))
        self.assertEqual(sub.subscription_ext_uid, 1)
        self.assertEqual(sub.next_event, datetime(2014, 8, 1, 0, 0, 0, tzinfo=timezone("UTC")))
        self.assertEqual(sub.article_number, 1)
        self.assertEqual(sub.subscription_id, 312414)
        self.assertEqual(sub.customer_id, 692738)
        self.assertEqual(sub.quantity, 1)

        customer = Customer.objects.get(customer_id=692738)

        self.assertEqual(sub.fastbill_customer, customer)

    @patch("fastbill.FastbillWrapper._request")
    def test_invoice(self, mocked_call):
        api_items = [
            {u'BANK_NAME': [], u'FIRST_NAME': u'Bjarne', u'LAST_NAME': u'Riis', u'BANK_CODE': [],
             u'ZIPCODE': u'5467890', u'CASH_DISCOUNT_PERCENT': u'0.00', u'PAYMENT_INFO': u'', u'AFFILIATE': u'',
             u'PAYMENT_TYPE': u'4', u'INTROTEXT': u'', u'COMMENT': u'', u'DUE_DATE': u'2014-07-21',
             u'SUBSCRIPTION_INVOICE_COUNTER': u'1', u'IS_CANCELED': u'0',
             u'PAYPAL_URL': u'https://automatic.fastbill.com/paypal/5cb2E4yT5AZ9VX_SgxDgKZVJ46mrNhlF-8B4uVwuusDFqVlbZElyavqUVUh26mz',
             u'CASH_DISCOUNT_DAYS': u'0', u'INVOICE_DATE': u'2014-07-21', u'PAID_DATE': u'0000-00-00 00:00:00',
             u'COUNTRY_CODE': u'DE', u'ITEMS': [
                {u'ARTICLE_NUMBER': u'1', u'DESCRIPTION': u'Test<br>', u'UNIT_PRICE': u'10.00000000',
                 u'COMPLETE_GROSS': 11.9, u'SORT_ORDER': 1, u'INVOICE_ITEM_ID': u'1018228', u'VAT_PERCENT': u'19.00',
                 u'VAT_VALUE': 1.9, u'COMPLETE_NET': 10, u'QUANTITY': u'1.00'}], u'ORGANIZATION': u'',
             u'CUSTOMER_ID': u'692708', u'BANK_ACCOUNT_NUMBER': [], u'CURRENCY_CODE': u'EUR', u'BANK_BIC': [],
             u'BANK_IBAN': [], u'INVOICE_ID': u'505388', u'SUB_TOTAL': 10, u'DAYS_FOR_PAYMENT': 0,
             u'VAT_ITEMS': [{u'VAT_PERCENT': u'19.00', u'VAT_VALUE': 1.9, u'COMPLETE_NET': 10}],
             u'DOCUMENT_URL': u'https://automatic.fastbill.com/download/5cb2E4yT5AZ9VX_SgxDgKZVJ46mrNhlF-8B4uVwuusDFqVlbZElyavqUVUh26mz',
             u'ADDRESS_2': u'', u'INVOICE_NUMBER': u'pm100', u'SALUTATION': u'mr', u'CUSTOMER_COSTCENTER_ID': u'0',
             u'CITY': u'Dortmund', u'TOTAL': 11.9, u'INVOICE_TITLE': u'', u'CUSTOMER_NUMBER': u'1', u'VAT_ID': u'',
             u'DELIVERY_DATE': u'21.07.2014 - 20.08.2014', u'ADDRESS': u'Foostrasse 12', u'BANK_ACCOUNT_OWNER': [],
             u'SUBSCRIPTION_ID': u'312392', u'TYPE': u'outgoing', u'TEMPLATE_ID': u'1', u'VAT_TOTAL': 1.9},
            {u'BANK_NAME': [], u'FIRST_NAME': u'Steffen', u'LAST_NAME': u'Simon', u'BANK_CODE': [],
             u'ZIPCODE': u'5467890', u'CASH_DISCOUNT_PERCENT': u'0.00',
             u'PAYMENT_INFO': u'22.07.2014 11,90 \u20ac (Kreditkarte) ', u'AFFILIATE': u'', u'PAYMENT_TYPE': u'4',
             u'INTROTEXT': u'', u'COMMENT': u'', u'DUE_DATE': u'2014-07-21', u'SUBSCRIPTION_INVOICE_COUNTER': u'1',
             u'IS_CANCELED': u'0',
             u'PAYPAL_URL': u'https://automatic.fastbill.com/paypal/vgPH0_9tviFC_i55d8DkEPk5o5PyPF-mPFZNBF9kL_jt4bKzfu4vSxXLJaFIYr',
             u'CASH_DISCOUNT_DAYS': u'0', u'INVOICE_DATE': u'2014-07-21', u'PAID_DATE': u'2014-07-22 00:00:00',
             u'COUNTRY_CODE': u'DE', u'ITEMS': [
                {u'ARTICLE_NUMBER': u'1', u'DESCRIPTION': u'Test<br>', u'UNIT_PRICE': u'10.00000000',
                 u'COMPLETE_GROSS': 11.9, u'SORT_ORDER': 1, u'INVOICE_ITEM_ID': u'1018236', u'VAT_PERCENT': u'19.00',
                 u'VAT_VALUE': 1.9, u'COMPLETE_NET': 10, u'QUANTITY': u'1.00'}], u'ORGANIZATION': u'',
             u'CUSTOMER_ID': u'692738', u'BANK_ACCOUNT_NUMBER': [], u'CURRENCY_CODE': u'EUR', u'BANK_BIC': [],
             u'BANK_IBAN': [], u'INVOICE_ID': u'505394', u'SUB_TOTAL': 10, u'DAYS_FOR_PAYMENT': 0,
             u'VAT_ITEMS': [{u'VAT_PERCENT': u'19.00', u'VAT_VALUE': 1.9, u'COMPLETE_NET': 10}],
             u'DOCUMENT_URL': u'https://automatic.fastbill.com/download/vgPH0_9tviFC_i55d8DkEPk5o5PyPF-mPFZNBF9kL_jt4bKzfu4vSxXLJaFIYr',
             u'ADDRESS_2': u'', u'INVOICE_NUMBER': u'pm101', u'SALUTATION': u'mr', u'CUSTOMER_COSTCENTER_ID': u'0',
             u'CITY': u'Dortmund', u'TOTAL': 11.9, u'INVOICE_TITLE': u'', u'CUSTOMER_NUMBER': u'2', u'VAT_ID': u'',
             u'DELIVERY_DATE': u'21.07.2014 - 20.08.2014', u'ADDRESS': u'Foostrasse 12', u'BANK_ACCOUNT_OWNER': [],
             u'SUBSCRIPTION_ID': u'312414', u'TYPE': u'outgoing', u'TEMPLATE_ID': u'1', u'VAT_TOTAL': 1.9},
            {u'BANK_NAME': [], u'FIRST_NAME': u'Johnny', u'LAST_NAME': u'Giraffaloe', u'BANK_CODE': [],
             u'ZIPCODE': u'5467890', u'CASH_DISCOUNT_PERCENT': u'0.00', u'PAYMENT_INFO': u'', u'AFFILIATE': u'',
             u'PAYMENT_TYPE': u'1', u'INTROTEXT': u'', u'COMMENT': u'', u'DUE_DATE': u'2014-07-21',
             u'SUBSCRIPTION_INVOICE_COUNTER': u'1', u'IS_CANCELED': u'0',
             u'PAYPAL_URL': u'https://automatic.fastbill.com/paypal/xkTvRqSxJzURhyMVGAB3QkSpP44KoPsYz_GDpZ0yLIDt6PCQD2goII4ACnPu_B',
             u'CASH_DISCOUNT_DAYS': u'0', u'INVOICE_DATE': u'2014-07-21', u'PAID_DATE': u'0000-00-00 00:00:00',
             u'COUNTRY_CODE': u'DE', u'ITEMS': [
                {u'ARTICLE_NUMBER': u'2', u'DESCRIPTION': u'Testprodukt 2<br>', u'UNIT_PRICE': u'20.00000000',
                 u'COMPLETE_GROSS': 23.8, u'SORT_ORDER': 1, u'INVOICE_ITEM_ID': u'1018334', u'VAT_PERCENT': u'19.00',
                 u'VAT_VALUE': 3.8, u'COMPLETE_NET': 20, u'QUANTITY': u'1.00'}], u'ORGANIZATION': u'Johnne',
             u'CUSTOMER_ID': u'693080', u'BANK_ACCOUNT_NUMBER': [], u'CURRENCY_CODE': u'EUR', u'BANK_BIC': [],
             u'BANK_IBAN': [], u'INVOICE_ID': u'505464', u'SUB_TOTAL': 20, u'DAYS_FOR_PAYMENT': 0,
             u'VAT_ITEMS': [{u'VAT_PERCENT': u'19.00', u'VAT_VALUE': 3.8, u'COMPLETE_NET': 20}],
             u'DOCUMENT_URL': u'https://automatic.fastbill.com/download/xkTvRqSxJzURhyMVGAB3QkSpP44KoPsYz_GDpZ0yLIDt6PCQD2goII4ACnPu_B',
             u'ADDRESS_2': u'', u'INVOICE_NUMBER': u'pm102', u'SALUTATION': u'mr', u'CUSTOMER_COSTCENTER_ID': u'0',
             u'CITY': u'Dortmund', u'TOTAL': 23.8, u'INVOICE_TITLE': u'', u'CUSTOMER_NUMBER': u'3', u'VAT_ID': u'',
             u'DELIVERY_DATE': u'21.07.2014 - 20.08.2014', u'ADDRESS': u'Foostrasse 12', u'BANK_ACCOUNT_OWNER': [],
             u'SUBSCRIPTION_ID': u'312714', u'TYPE': u'outgoing', u'TEMPLATE_ID': u'1', u'VAT_TOTAL': 3.8},
            {u'BANK_NAME': [], u'FIRST_NAME': u'Foo', u'LAST_NAME': u'Bar', u'BANK_CODE': [], u'ZIPCODE': u'Bar',
             u'CASH_DISCOUNT_PERCENT': u'0.00', u'PAYMENT_INFO': u'22.07.2014 23,80 \u20ac () ', u'AFFILIATE': u'',
             u'PAYMENT_TYPE': u'1', u'INTROTEXT': u'', u'COMMENT': u'', u'DUE_DATE': u'2014-07-21',
             u'SUBSCRIPTION_INVOICE_COUNTER': u'1', u'IS_CANCELED': u'0',
             u'PAYPAL_URL': u'https://automatic.fastbill.com/paypal/jSMWYTREo--zLC796pD3Th5DHIXzmCXIVkeu3wyftwR5yM1s14jHZcLhkiUJlsR7',
             u'CASH_DISCOUNT_DAYS': u'0', u'INVOICE_DATE': u'2014-07-21', u'PAID_DATE': u'2014-07-22 00:00:00',
             u'COUNTRY_CODE': u'DE', u'ITEMS': [
                {u'ARTICLE_NUMBER': u'2', u'DESCRIPTION': u'Testprodukt 2<br>', u'UNIT_PRICE': u'20.00000000',
                 u'COMPLETE_GROSS': 23.8, u'SORT_ORDER': 1, u'INVOICE_ITEM_ID': u'1018340', u'VAT_PERCENT': u'19.00',
                 u'VAT_VALUE': 3.8, u'COMPLETE_NET': 20, u'QUANTITY': u'1.00'}], u'ORGANIZATION': u'Oliver',
             u'CUSTOMER_ID': u'693096', u'BANK_ACCOUNT_NUMBER': [], u'CURRENCY_CODE': u'EUR', u'BANK_BIC': [],
             u'BANK_IBAN': [], u'INVOICE_ID': u'505468', u'SUB_TOTAL': 20, u'DAYS_FOR_PAYMENT': 0,
             u'VAT_ITEMS': [{u'VAT_PERCENT': u'19.00', u'VAT_VALUE': 3.8, u'COMPLETE_NET': 20}],
             u'DOCUMENT_URL': u'https://automatic.fastbill.com/download/jSMWYTREo--zLC796pD3Th5DHIXzmCXIVkeu3wyftwR5yM1s14jHZcLhkiUJlsR7',
             u'ADDRESS_2': u'', u'INVOICE_NUMBER': u'pm103', u'SALUTATION': u'', u'CUSTOMER_COSTCENTER_ID': u'0',
             u'CITY': u'Foooofo', u'TOTAL': 23.8, u'INVOICE_TITLE': u'', u'CUSTOMER_NUMBER': u'4', u'VAT_ID': u'',
             u'DELIVERY_DATE': u'21.07.2014 - 20.08.2014', u'ADDRESS': u'Foo', u'BANK_ACCOUNT_OWNER': [],
             u'SUBSCRIPTION_ID': u'312728', u'TYPE': u'outgoing', u'TEMPLATE_ID': u'1', u'VAT_TOTAL': 3.8},
        ]

        customer_call = {u'CUSTOMERS': [
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Johnny', u'LAST_NAME': u'Giraffaloe', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'0,00', u'ZIPCODE': u'5467890',
             u'BANK_ACCOUNT_MANDATE_REFERENCE': u'', u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'LANGUAGE_CODE': u'de',
             u'EMAIL': u'foo@bar.com', u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'', u'TAGS': u'',
             u'PHONE': u'', u'CUSTOMER_TYPE': u'business',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/40b6307fb087009dda6a192b2f6e379d',
             u'COUNTRY_CODE': u'DE', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'Johnne',
             u'CUSTOMER_ID': u'692708', u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'X_ATTRIBUTES': u'',
             u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'40b6307fb087009dda6a192b2f6e379d', u'BANK_BIC': u'',
             u'CREATED': u'2014-07-21 17:09:56', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-21 17:09:56',
             u'SALUTATION': u'mr', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'Example City',
             u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/40b6307fb087009dda6a192b2f6e379d',
             u'CUSTOMER_NUMBER': u'1', u'VAT_ID': u'', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Foostrasse 12',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''}]}

        subscription_call = {u'SUBSCRIPTIONS': [{u'STATUS': u'active', u'X_ATTRIBUTES': u'', u'INVOICE_TITLE': u'',
                                                 u'HASH': u'0d124afc9c8758be0076bd5921c77346',
                                                 u'CANCELLATION_DATE': u'0000-00-00 00:00:00',
                                                 u'EXPIRATION_DATE': u'2014-08-21 12:20:22',
                                                 u'LAST_EVENT': u'2014-07-21 12:20:22',
                                                 u'START': u'2014-07-21 12:20:22', u'SUBSCRIPTION_EXT_UID': u'1',
                                                 u'NEXT_EVENT': u'2014-08-21 12:20:22', u'ARTICLE_NUMBER': u'1',
                                                 u'SUBSCRIPTION_ID': 312392, u'CUSTOMER_ID': 692708, u'ADDONS': [],
                                                 u'QUANTITY': u'1'}]}

        article_call = {u'ARTICLES': [
            {u'SUBSCRIPTION_CANCELLATION': 0, u'ARTICLE_NUMBER': u'1', u'DESCRIPTION': u'', u'TAGS': u'',
             u'TITLE': u'Test', u'TRANSLATIONS': [], u'UNIT_PRICE': u'10.0000', u'IS_ADDON': u'0',
             u'SUBSCRIPTION_TRIAL': 0, u'SUBSCRIPTION_INTERVAL': u'1 month',
             u'CHECKOUT_URL': u'https://automatic.fastbill.com/purchase/4751862ae058864485a7722930137c9f/1',
             u'SETUP_FEE': u'0.0000', u'SUBSCRIPTION_DURATION_FOLLOW': 0, u'RETURN_URL_SUCCESS': u'',
             u'VAT_PERCENT': u'19.00', u'ALLOW_MULTIPLE': u'0', u'RETURN_URL_CANCEL': u'',
             u'SUBSCRIPTION_NUMBER_EVENTS': u'0', u'CURRENCY_CODE': u'EUR', u'SUBSCRIPTION_DURATION': 0}]}

        mocked_call.side_effect = [
            customer_call,
            subscription_call,
            article_call,
        ]

        created, sub = Invoice.objects.update_or_create(api_items[0])

        self.assertEqual(created, True)


class ConvertErrorTestCase(FastbillTestCase):
    def test_article_identifier(self):
        api_items = [
            # note the broken ARTICLE_NUMBER
            {u'SUBSCRIPTION_CANCELLATION': 0, u'ARTICLE_NUMBER######': u'1', u'DESCRIPTION': u'', u'TAGS': u'',
             u'TITLE': u'Test', u'TRANSLATIONS': [], u'UNIT_PRICE': u'10.0000', u'IS_ADDON': u'0',
             u'SUBSCRIPTION_TRIAL': 0, u'SUBSCRIPTION_INTERVAL': u'1 month',
             u'CHECKOUT_URL': u'https://automatic.fastbill.com/purchase/4751862ae058864485a7722930137c9f/1',
             u'SETUP_FEE': u'0.0000', u'SUBSCRIPTION_DURATION_FOLLOW': 0, u'RETURN_URL_SUCCESS': u'',
             u'VAT_PERCENT': u'19.00', u'ALLOW_MULTIPLE': u'0', u'RETURN_URL_CANCEL': u'',
             u'SUBSCRIPTION_NUMBER_EVENTS': u'0', u'CURRENCY_CODE': u'EUR', u'SUBSCRIPTION_DURATION': 0},
            {u'SUBSCRIPTION_CANCELLATION': 0, u'ARTICLE_NUMBER': u'2', u'DESCRIPTION': u'', u'TAGS': u'',
             u'TITLE': u'Testprodukt 2', u'TRANSLATIONS': [], u'UNIT_PRICE': u'20.0000', u'IS_ADDON': u'0',
             u'SUBSCRIPTION_TRIAL': 0, u'SUBSCRIPTION_INTERVAL': u'1 month',
             u'CHECKOUT_URL': u'https://automatic.fastbill.com/purchase/4751862ae058864485a7722930137c9f/2',
             u'SETUP_FEE': u'0.0000', u'SUBSCRIPTION_DURATION_FOLLOW': 0, u'RETURN_URL_SUCCESS': u'',
             u'VAT_PERCENT': u'19.00', u'ALLOW_MULTIPLE': u'0', u'RETURN_URL_CANCEL': u'',
             u'SUBSCRIPTION_NUMBER_EVENTS': u'0', u'CURRENCY_CODE': u'EUR', u'SUBSCRIPTION_DURATION': 0}
        ]

        with self.assertRaises(ConvertError):
            Article.objects.update_or_create(api_items[0])


class HelperTestCase(FastbillTestCase):
    @patch("fastbill.FastbillWrapper._request")
    def test_get_article_by_number(self, mocked_call):
        mocked_call.return_value = {u'ARTICLES': [
            {u'SUBSCRIPTION_CANCELLATION': 0, u'ARTICLE_NUMBER': u'1', u'DESCRIPTION': u'', u'TAGS': u'',
             u'TITLE': u'Test', u'TRANSLATIONS': [], u'UNIT_PRICE': u'10.0000', u'IS_ADDON': u'0',
             u'SUBSCRIPTION_TRIAL': 0, u'SUBSCRIPTION_INTERVAL': u'1 month',
             u'CHECKOUT_URL': u'https://automatic.fastbill.com/purchase/4751862ae058864485a7722930137c9f/1',
             u'SETUP_FEE': u'0.0000', u'SUBSCRIPTION_DURATION_FOLLOW': 0, u'RETURN_URL_SUCCESS': u'',
             u'VAT_PERCENT': u'19.00', u'ALLOW_MULTIPLE': u'0', u'RETURN_URL_CANCEL': u'',
             u'SUBSCRIPTION_NUMBER_EVENTS': u'0', u'CURRENCY_CODE': u'EUR', u'SUBSCRIPTION_DURATION': 0}]}

        from .helper import get_article_by_number

        article = get_article_by_number(1)
        self.assertEqual(article.article_number, 1)

        article = get_article_by_number(2)
        self.assertEqual(article, None)

    @patch("fastbill.FastbillWrapper._request")
    def test_get_subscription_by_id(self, mocked_call):
        sub_call = {u'SUBSCRIPTIONS': [{u'STATUS': u'active', u'X_ATTRIBUTES': u'', u'INVOICE_TITLE': u'',
                                        u'HASH': u'0d124afc9c8758be0076bd5921c77346',
                                        u'CANCELLATION_DATE': u'0000-00-00 00:00:00',
                                        u'EXPIRATION_DATE': u'2014-08-21 12:20:22',
                                        u'LAST_EVENT': u'2014-07-21 12:20:22',
                                        u'START': u'2014-07-21 12:20:22', u'SUBSCRIPTION_EXT_UID': u'1',
                                        u'NEXT_EVENT': u'2014-08-21 12:20:22', u'ARTICLE_NUMBER': u'1',
                                        u'SUBSCRIPTION_ID': 312392, u'CUSTOMER_ID': 692708, u'ADDONS': [],
                                        u'QUANTITY': u'1'}]}

        customer_call = {u'CUSTOMERS': [
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Johnny', u'LAST_NAME': u'Giraffaloe', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'0,00', u'ZIPCODE': u'5467890',
             u'BANK_ACCOUNT_MANDATE_REFERENCE': u'', u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'LANGUAGE_CODE': u'de',
             u'EMAIL': u'foo@bar.com', u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'', u'TAGS': u'',
             u'PHONE': u'', u'CUSTOMER_TYPE': u'business',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/40b6307fb087009dda6a192b2f6e379d',
             u'COUNTRY_CODE': u'DE', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'Johnne',
             u'CUSTOMER_ID': u'692708', u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'X_ATTRIBUTES': u'',
             u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'40b6307fb087009dda6a192b2f6e379d', u'BANK_BIC': u'',
             u'CREATED': u'2014-07-21 17:09:56', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-21 17:09:56',
             u'SALUTATION': u'mr', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'Example City',
             u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/40b6307fb087009dda6a192b2f6e379d',
             u'CUSTOMER_NUMBER': u'1', u'VAT_ID': u'', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Foostrasse 12',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''}]}

        article_call = {u'ARTICLES': [
            {u'SUBSCRIPTION_CANCELLATION': 0, u'ARTICLE_NUMBER': u'1', u'DESCRIPTION': u'', u'TAGS': u'',
             u'TITLE': u'Test', u'TRANSLATIONS': [], u'UNIT_PRICE': u'10.0000', u'IS_ADDON': u'0',
             u'SUBSCRIPTION_TRIAL': 0, u'SUBSCRIPTION_INTERVAL': u'1 month',
             u'CHECKOUT_URL': u'https://automatic.fastbill.com/purchase/4751862ae058864485a7722930137c9f/1',
             u'SETUP_FEE': u'0.0000', u'SUBSCRIPTION_DURATION_FOLLOW': 0, u'RETURN_URL_SUCCESS': u'',
             u'VAT_PERCENT': u'19.00', u'ALLOW_MULTIPLE': u'0', u'RETURN_URL_CANCEL': u'',
             u'SUBSCRIPTION_NUMBER_EVENTS': u'0', u'CURRENCY_CODE': u'EUR', u'SUBSCRIPTION_DURATION': 0}]}

        mocked_call.side_effect = [
            sub_call,
            customer_call,
            article_call,

            # add another sub_call, we are calling it twice
            sub_call,
            customer_call,
            article_call,
        ]

        from .helper import get_subscription_by_id

        sub = get_subscription_by_id(312392)
        self.assertEqual(sub.subscription_id, 312392)

        # sub = get_subscription_by_id(1)
        # self.assertEqual(sub, None)


class NotificationTestCase(FastbillTestCase):
    def setUp(self):
        super(NotificationTestCase, self).setUp()
        import base64

        credentials = "%s:%s" % (settings.FASTBILL_NOTIFICATION_USERNAME, settings.FASTBILL_NOTIFICATION_PASSWORD)
        self.auth_string = "Basic %s" % base64.b64encode(credentials)

    @patch("fastbill.FastbillWrapper._request")
    def test_customer_created(self, api_call):
        customer_created = {u'customer': {u'x_attributes': [], u'city': u'oli', u'customer_id': u'697230',
                                          u'hash': u'c7f08e2fa58ecc497ae94bbf8d12b6d6', u'country_code': u'DK',
                                          u'firstname': u'Oli', u'companyname': u'Oli', u'lastname': u'ol',
                                          u'title': u'', u'zipcode': u'oli', u'customer_number': u'9', u'telefax': u'',
                                          u'telephone': u'', u'address_2': u'', u'address': u'Oli',
                                          u'salutation': u'Herr',
                                          u'payment_data_url': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
                                          u'customer_ext_uid': 1, u'email': u'oli@oli.de',
                                          u'dashboard_url': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6'},
                            u'type': u'customer.created', u'id': 366428}

        customer_call = {"CUSTOMERS": [
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Oli', u'LAST_NAME': u'ol', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'0,00', u'ZIPCODE': u'oli', u'BANK_ACCOUNT_MANDATE_REFERENCE': u'',
             u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'LANGUAGE_CODE': u'de', u'EMAIL': u'oli@oli.de',
             u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'', u'TAGS': u'', u'PHONE': u'',
             u'CUSTOMER_TYPE': u'business',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
             u'COUNTRY_CODE': u'DK', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'Oli', u'CUSTOMER_ID': u'697230',
             u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'X_ATTRIBUTES': u'',
             u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'c7f08e2fa58ecc497ae94bbf8d12b6d6', u'BANK_BIC': u'',
             u'CREATED': u'2014-07-24 15:06:07', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-24 15:06:07',
             u'SALUTATION': u'mr', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'oli', u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
             u'CUSTOMER_NUMBER': u'9', u'VAT_ID': u'oli', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Oli',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''}]}
        api_call.return_value = customer_call
        response = self.client.post(reverse("django-fastbill-notification"), json.dumps(customer_created),
                                    content_type="application/json", HTTP_AUTHORIZATION=self.auth_string)

        customer = Customer.objects.get(customer_id=customer_created["customer"]["customer_id"])
        self.assertEqual(customer.customer_id, int(customer_created["customer"]["customer_id"]))
        self.assertEqual(customer.dashboard_url, customer_created["customer"]["dashboard_url"])
        self.assertEqual(response.status_code, 200)

    @patch("fastbill.FastbillWrapper._request")
    def test_customer_changed(self, api_call):
        customer_changed = {u'customer': {u'x_attributes': [], u'city': u'Brandebnurgh', u'customer_id': u'697230',
                                          u'hash': u'2a01e7a1e717fd2ebf84e980d4888048', u'country_code': u'DE',
                                          u'firstname': u'Kalli', u'companyname': u'Kallio', u'lastname': u'Kalle',
                                          u'title': u'', u'zipcode': u'33445', u'customer_number': u'8',
                                          u'telefax': u'', u'telephone': u'', u'address_2': u'',
                                          u'address': u'Kallstr. 22', u'salutation': u'Herr',
                                          u'payment_data_url': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/2a01e7a1e717fd2ebf84e980d4888048',
                                          u'customer_ext_uid': u'1', u'email': u'kalli@kalle.de',
                                          u'dashboard_url': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/2a01e7a1e717fd2ebf84e980d4888048'},
                            u'type': u'customer.changed', u'id': 366426}

        customer_call = {"CUSTOMERS": [
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Oli', u'LAST_NAME': u'ol', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'0,00', u'ZIPCODE': u'oli', u'BANK_ACCOUNT_MANDATE_REFERENCE': u'',
             u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'LANGUAGE_CODE': u'de', u'EMAIL': u'oli@oli.de',
             u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'', u'TAGS': u'', u'PHONE': u'',
             u'CUSTOMER_TYPE': u'business',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/2a01e7a1e717fd2ebf84e980d4888048',
             u'COUNTRY_CODE': u'DK', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'Oli', u'CUSTOMER_ID': u'697230',
             u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'X_ATTRIBUTES': u'',
             u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'c7f08e2fa58ecc497ae94bbf8d12b6d6', u'BANK_BIC': u'',
             u'CREATED': u'2014-07-24 15:06:07', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-24 15:06:07',
             u'SALUTATION': u'mr', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'oli', u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
             u'CUSTOMER_NUMBER': u'9', u'VAT_ID': u'oli', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Oli',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''}]}
        api_call.return_value = customer_call
        response = self.client.post(reverse("django-fastbill-notification"), json.dumps(customer_changed),
                                    content_type="application/json", HTTP_AUTHORIZATION=self.auth_string)

        customer = Customer.objects.get(customer_id=customer_changed["customer"]["customer_id"])
        self.assertEqual(customer.customer_id, int(customer_changed["customer"]["customer_id"]))
        self.assertEqual(customer.dashboard_url, customer_changed["customer"]["dashboard_url"])
        self.assertEqual(response.status_code, 200)

    @patch("fastbill.FastbillWrapper._request")
    def test_customer_deleted(self, api_call):
        customer_deleted = {u'customer': {u'x_attributes': [], u'city': u'Brandebnurgh', u'customer_id': u'697230',
                                          u'hash': u'2a01e7a1e717fd2ebf84e980d4888048', u'country_code': u'DE',
                                          u'firstname': u'Kalli', u'companyname': u'Kallio', u'lastname': u'Kalle',
                                          u'title': u'', u'zipcode': u'33445', u'customer_number': u'8',
                                          u'telefax': u'', u'telephone': u'', u'address_2': u'',
                                          u'address': u'Kallstr. 22', u'salutation': u'Herr',
                                          u'payment_data_url': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/2a01e7a1e717fd2ebf84e980d4888048',
                                          u'customer_ext_uid': u'1', u'email': u'kalli@kalle.de',
                                          u'dashboard_url': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/2a01e7a1e717fd2ebf84e980d4888048'},
                            u'type': u'customer.deleted', u'id': 366426}

        customer_call = {"CUSTOMERS": [
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Oli', u'LAST_NAME': u'ol', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'0,00', u'ZIPCODE': u'oli', u'BANK_ACCOUNT_MANDATE_REFERENCE': u'',
             u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'LANGUAGE_CODE': u'de', u'EMAIL': u'oli@oli.de',
             u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'', u'TAGS': u'', u'PHONE': u'',
             u'CUSTOMER_TYPE': u'business',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/2a01e7a1e717fd2ebf84e980d4888048',
             u'COUNTRY_CODE': u'DK', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'Oli', u'CUSTOMER_ID': u'697230',
             u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'X_ATTRIBUTES': u'',
             u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'c7f08e2fa58ecc497ae94bbf8d12b6d6', u'BANK_BIC': u'',
             u'CREATED': u'2014-07-24 15:06:07', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-24 15:06:07',
             u'SALUTATION': u'mr', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'oli', u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
             u'CUSTOMER_NUMBER': u'9', u'VAT_ID': u'oli', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Oli',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''}]}
        api_call.return_value = customer_call
        response = self.client.post(reverse("django-fastbill-notification"), json.dumps(customer_deleted),
                                    content_type="application/json", HTTP_AUTHORIZATION=self.auth_string)

        customer = Customer.objects.get(customer_id=customer_deleted["customer"]["customer_id"])
        self.assertEqual(customer.customer_id, int(customer_deleted["customer"]["customer_id"]))
        self.assertEqual(customer.dashboard_url, customer_deleted["customer"]["dashboard_url"])
        self.assertEqual(response.status_code, 200)

    @patch("fastbill.FastbillWrapper._request")
    def test_subscription_created(self, api_call):
        subscription_created = {
            u'customer': {u'city': u'oli', u'customer_id': u'697230', u'hash': u'c7f08e2fa58ecc497ae94bbf8d12b6d6',
                          u'country_code': u'DK', u'firstname': u'Oli', u'companyname': u'Oli', u'lastname': u'ol',
                          u'title': u'', u'zipcode': u'oli', u'customer_number': u'9', u'telefax': u'',
                          u'telephone': u'',
                          u'address_2': u'', u'address': u'Oli', u'salutation': u'Herr',
                          u'payment_data_url': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
                          u'customer_ext_uid': 1, u'email': u'oli@oli.de',
                          u'dashboard_url': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6'},
            u'created': u'2014-07-24 15:06:10', u'type': u'subscription.created', u'id': 772558,
            u'subscription': {u'status': u'active', u'hash': u'af39223ed8581bf7473c5d7ba504e552', u'article_code': u'2',
                              u'last_event': u'2014-07-24 15:06:08', u'expiration_date': u'2014-08-24 15:06:08',
                              u'cancellation_date': u'0000-00-00 00:00:00', u'subscription_ext_uid': u'1',
                              u'next_event': u'2014-08-24 15:06:08', u'subscription_id': 315458,
                              u'start_date': u'2014-07-24 15:06:08', u'coupons': [], u'quantity': u'1'}}

        customer_call = {"CUSTOMERS": [
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Oli', u'LAST_NAME': u'ol', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'0,00', u'ZIPCODE': u'oli', u'BANK_ACCOUNT_MANDATE_REFERENCE': u'',
             u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'LANGUAGE_CODE': u'de', u'EMAIL': u'oli@oli.de',
             u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'', u'TAGS': u'', u'PHONE': u'',
             u'CUSTOMER_TYPE': u'business',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/2a01e7a1e717fd2ebf84e980d4888048',
             u'COUNTRY_CODE': u'DK', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'Oli', u'CUSTOMER_ID': u'697230',
             u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'X_ATTRIBUTES': u'',
             u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'c7f08e2fa58ecc497ae94bbf8d12b6d6', u'BANK_BIC': u'',
             u'CREATED': u'2014-07-24 15:06:07', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-24 15:06:07',
             u'SALUTATION': u'mr', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'oli', u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
             u'CUSTOMER_NUMBER': u'9', u'VAT_ID': u'oli', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Oli',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''}]}

        subscription_call = {u'SUBSCRIPTIONS': [{u'STATUS': u'active', u'X_ATTRIBUTES': u'', u'INVOICE_TITLE': u'',
                                                 u'HASH': u'0d124afc9c8758be0076bd5921c77346',
                                                 u'CANCELLATION_DATE': u'0000-00-00 00:00:00',
                                                 u'EXPIRATION_DATE': u'2014-08-21 12:20:22',
                                                 u'LAST_EVENT': u'2014-07-21 12:20:22',
                                                 u'START': u'2014-07-21 12:20:22', u'SUBSCRIPTION_EXT_UID': u'1',
                                                 u'NEXT_EVENT': u'2014-08-21 12:20:22', u'ARTICLE_NUMBER': u'1',
                                                 u'SUBSCRIPTION_ID': 315458, u'CUSTOMER_ID': 697230, u'ADDONS': [],
                                                 u'QUANTITY': u'1'}]}

        article_call = {u'ARTICLES': [
            {u'SUBSCRIPTION_CANCELLATION': 0, u'ARTICLE_NUMBER': u'1', u'DESCRIPTION': u'', u'TAGS': u'',
             u'TITLE': u'Test', u'TRANSLATIONS': [], u'UNIT_PRICE': u'10.0000', u'IS_ADDON': u'0',
             u'SUBSCRIPTION_TRIAL': 0, u'SUBSCRIPTION_INTERVAL': u'1 month',
             u'CHECKOUT_URL': u'https://automatic.fastbill.com/purchase/4751862ae058864485a7722930137c9f/1',
             u'SETUP_FEE': u'0.0000', u'SUBSCRIPTION_DURATION_FOLLOW': 0, u'RETURN_URL_SUCCESS': u'',
             u'VAT_PERCENT': u'19.00', u'ALLOW_MULTIPLE': u'0', u'RETURN_URL_CANCEL': u'',
             u'SUBSCRIPTION_NUMBER_EVENTS': u'0', u'CURRENCY_CODE': u'EUR', u'SUBSCRIPTION_DURATION': 0}]}

        api_call.side_effect = [
            customer_call,
            subscription_call,
            article_call
        ]

        response = self.client.post(reverse("django-fastbill-notification"), json.dumps(subscription_created),
                                    content_type="application/json", HTTP_AUTHORIZATION=self.auth_string)
        self.assertEqual(response.status_code, 200)

        Customer.objects.get(customer_id=subscription_created["customer"]["customer_id"])
        Subscription.objects.get(subscription_id=subscription_created["subscription"]["subscription_id"])
        # Article.objects.get(article_id=)

    @patch("fastbill.FastbillWrapper._request")
    def test_subscription_changed(self, api_call):
        subscription_changed = {
            u'customer': {u'city': u'oli', u'customer_id': u'697230', u'hash': u'c7f08e2fa58ecc497ae94bbf8d12b6d6',
                          u'country_code': u'DK', u'firstname': u'Oli', u'companyname': u'Oli', u'lastname': u'ol',
                          u'title': u'', u'zipcode': u'oli', u'customer_number': u'9', u'telefax': u'',
                          u'telephone': u'',
                          u'address_2': u'', u'address': u'Oli', u'salutation': u'Herr',
                          u'payment_data_url': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
                          u'customer_ext_uid': 1, u'email': u'oli@oli.de',
                          u'dashboard_url': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6'},
            u'created': u'2014-07-24 15:25:14', u'type': u'subscription.changed', u'id': 772594,
            u'subscription': {u'status': u'active', u'hash': u'af39223ed8581bf7473c5d7ba504e552', u'article_code': u'2',
                              u'last_event': u'2014-07-24 15:06:08', u'expiration_date': u'2014-08-24 00:00:00',
                              u'cancellation_date': u'2014-08-24 00:00:00', u'subscription_ext_uid': u'1',
                              u'next_event': u'2014-08-24 15:06:08', u'subscription_id': 315458,
                              u'start_date': u'2014-07-24 15:06:08', u'coupons': [], u'quantity': 1}}

        customer_call = {"CUSTOMERS": [
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Oli', u'LAST_NAME': u'ol', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'0,00', u'ZIPCODE': u'oli', u'BANK_ACCOUNT_MANDATE_REFERENCE': u'',
             u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'LANGUAGE_CODE': u'de', u'EMAIL': u'oli@oli.de',
             u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'', u'TAGS': u'', u'PHONE': u'',
             u'CUSTOMER_TYPE': u'business',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/2a01e7a1e717fd2ebf84e980d4888048',
             u'COUNTRY_CODE': u'DK', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'Oli', u'CUSTOMER_ID': u'697230',
             u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'X_ATTRIBUTES': u'',
             u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'c7f08e2fa58ecc497ae94bbf8d12b6d6', u'BANK_BIC': u'',
             u'CREATED': u'2014-07-24 15:06:07', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-24 15:06:07',
             u'SALUTATION': u'mr', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'oli', u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
             u'CUSTOMER_NUMBER': u'9', u'VAT_ID': u'oli', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Oli',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''}]}

        subscription_call = {u'SUBSCRIPTIONS': [{u'STATUS': u'active', u'X_ATTRIBUTES': u'', u'INVOICE_TITLE': u'',
                                                 u'HASH': u'0d124afc9c8758be0076bd5921c77346',
                                                 u'CANCELLATION_DATE': u'0000-00-00 00:00:00',
                                                 u'EXPIRATION_DATE': u'2014-08-21 12:20:22',
                                                 u'LAST_EVENT': u'2014-07-21 12:20:22',
                                                 u'START': u'2014-07-21 12:20:22', u'SUBSCRIPTION_EXT_UID': u'1',
                                                 u'NEXT_EVENT': u'2014-08-21 12:20:22', u'ARTICLE_NUMBER': u'1',
                                                 u'SUBSCRIPTION_ID': 315458, u'CUSTOMER_ID': 697230, u'ADDONS': [],
                                                 u'QUANTITY': u'1'}]}

        article_call = {u'ARTICLES': [
            {u'SUBSCRIPTION_CANCELLATION': 0, u'ARTICLE_NUMBER': u'1', u'DESCRIPTION': u'', u'TAGS': u'',
             u'TITLE': u'Test', u'TRANSLATIONS': [], u'UNIT_PRICE': u'10.0000', u'IS_ADDON': u'0',
             u'SUBSCRIPTION_TRIAL': 0, u'SUBSCRIPTION_INTERVAL': u'1 month',
             u'CHECKOUT_URL': u'https://automatic.fastbill.com/purchase/4751862ae058864485a7722930137c9f/1',
             u'SETUP_FEE': u'0.0000', u'SUBSCRIPTION_DURATION_FOLLOW': 0, u'RETURN_URL_SUCCESS': u'',
             u'VAT_PERCENT': u'19.00', u'ALLOW_MULTIPLE': u'0', u'RETURN_URL_CANCEL': u'',
             u'SUBSCRIPTION_NUMBER_EVENTS': u'0', u'CURRENCY_CODE': u'EUR', u'SUBSCRIPTION_DURATION': 0}]}

        api_call.side_effect = [
            customer_call,
            subscription_call,
            article_call
        ]

        response = self.client.post(reverse("django-fastbill-notification"), json.dumps(subscription_changed),
                                    content_type="application/json", HTTP_AUTHORIZATION=self.auth_string)
        self.assertEqual(response.status_code, 200)

        Customer.objects.get(customer_id=subscription_changed["customer"]["customer_id"])
        Subscription.objects.get(subscription_id=subscription_changed["subscription"]["subscription_id"])

    @patch("fastbill.FastbillWrapper._request")
    def test_subscription_canceled(self, api_call):
        subscription_canceled = {
            u'customer': {u'city': u'oli', u'customer_id': u'697230', u'hash': u'c7f08e2fa58ecc497ae94bbf8d12b6d6',
                          u'country_code': u'DK', u'firstname': u'Oli', u'companyname': u'Oli', u'lastname': u'ol',
                          u'title': u'', u'zipcode': u'oli', u'customer_number': u'9', u'telefax': u'',
                          u'telephone': u'',
                          u'address_2': u'', u'address': u'Oli', u'salutation': u'Herr',
                          u'payment_data_url': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
                          u'customer_ext_uid': 1, u'email': u'oli@oli.de',
                          u'dashboard_url': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6'},
            u'created': u'2014-07-24 15:25:14', u'type': u'subscription.canceled', u'id': 772594,
            u'subscription': {u'status': u'active', u'hash': u'af39223ed8581bf7473c5d7ba504e552', u'article_code': u'2',
                              u'last_event': u'2014-07-24 15:06:08', u'expiration_date': u'2014-08-24 00:00:00',
                              u'cancellation_date': u'2014-08-24 00:00:00', u'subscription_ext_uid': u'1',
                              u'next_event': u'2014-08-24 15:06:08', u'subscription_id': 315458,
                              u'start_date': u'2014-07-24 15:06:08', u'coupons': [], u'quantity': 1}}

        customer_call = {"CUSTOMERS": [
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Oli', u'LAST_NAME': u'ol', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'0,00', u'ZIPCODE': u'oli', u'BANK_ACCOUNT_MANDATE_REFERENCE': u'',
             u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'LANGUAGE_CODE': u'de', u'EMAIL': u'oli@oli.de',
             u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'', u'TAGS': u'', u'PHONE': u'',
             u'CUSTOMER_TYPE': u'business',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/2a01e7a1e717fd2ebf84e980d4888048',
             u'COUNTRY_CODE': u'DK', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'Oli', u'CUSTOMER_ID': u'697230',
             u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'X_ATTRIBUTES': u'',
             u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'c7f08e2fa58ecc497ae94bbf8d12b6d6', u'BANK_BIC': u'',
             u'CREATED': u'2014-07-24 15:06:07', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-24 15:06:07',
             u'SALUTATION': u'mr', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'oli', u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
             u'CUSTOMER_NUMBER': u'9', u'VAT_ID': u'oli', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Oli',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''}]}

        subscription_call = {u'SUBSCRIPTIONS': [{u'STATUS': u'active', u'X_ATTRIBUTES': u'', u'INVOICE_TITLE': u'',
                                                 u'HASH': u'0d124afc9c8758be0076bd5921c77346',
                                                 u'CANCELLATION_DATE': u'0000-00-00 00:00:00',
                                                 u'EXPIRATION_DATE': u'2014-08-21 12:20:22',
                                                 u'LAST_EVENT': u'2014-07-21 12:20:22',
                                                 u'START': u'2014-07-21 12:20:22', u'SUBSCRIPTION_EXT_UID': u'1',
                                                 u'NEXT_EVENT': u'2014-08-21 12:20:22', u'ARTICLE_NUMBER': u'1',
                                                 u'SUBSCRIPTION_ID': 315458, u'CUSTOMER_ID': 697230, u'ADDONS': [],
                                                 u'QUANTITY': u'1'}]}

        article_call = {u'ARTICLES': [
            {u'SUBSCRIPTION_CANCELLATION': 0, u'ARTICLE_NUMBER': u'1', u'DESCRIPTION': u'', u'TAGS': u'',
             u'TITLE': u'Test', u'TRANSLATIONS': [], u'UNIT_PRICE': u'10.0000', u'IS_ADDON': u'0',
             u'SUBSCRIPTION_TRIAL': 0, u'SUBSCRIPTION_INTERVAL': u'1 month',
             u'CHECKOUT_URL': u'https://automatic.fastbill.com/purchase/4751862ae058864485a7722930137c9f/1',
             u'SETUP_FEE': u'0.0000', u'SUBSCRIPTION_DURATION_FOLLOW': 0, u'RETURN_URL_SUCCESS': u'',
             u'VAT_PERCENT': u'19.00', u'ALLOW_MULTIPLE': u'0', u'RETURN_URL_CANCEL': u'',
             u'SUBSCRIPTION_NUMBER_EVENTS': u'0', u'CURRENCY_CODE': u'EUR', u'SUBSCRIPTION_DURATION': 0}]}

        api_call.side_effect = [
            customer_call,
            subscription_call,
            article_call
        ]

        response = self.client.post(reverse("django-fastbill-notification"), json.dumps(subscription_canceled),
                                    content_type="application/json", HTTP_AUTHORIZATION=self.auth_string)
        self.assertEqual(response.status_code, 200)

        Customer.objects.get(customer_id=subscription_canceled["customer"]["customer_id"])
        Subscription.objects.get(subscription_id=subscription_canceled["subscription"]["subscription_id"])

    @patch("fastbill.FastbillWrapper._request")
    def test_subscription_closed(self, api_call):
        subscription_closed = {
            u'customer': {u'city': u'oli', u'customer_id': u'697230', u'hash': u'c7f08e2fa58ecc497ae94bbf8d12b6d6',
                          u'country_code': u'DK', u'firstname': u'Oli', u'companyname': u'Oli', u'lastname': u'ol',
                          u'title': u'', u'zipcode': u'oli', u'customer_number': u'9', u'telefax': u'',
                          u'telephone': u'',
                          u'address_2': u'', u'address': u'Oli', u'salutation': u'Herr',
                          u'payment_data_url': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
                          u'customer_ext_uid': 1, u'email': u'oli@oli.de',
                          u'dashboard_url': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6'},
            u'created': u'2014-07-24 15:25:14', u'type': u'subscription.closed', u'id': 772594,
            u'subscription': {u'status': u'active', u'hash': u'af39223ed8581bf7473c5d7ba504e552', u'article_code': u'2',
                              u'last_event': u'2014-07-24 15:06:08', u'expiration_date': u'2014-08-24 00:00:00',
                              u'cancellation_date': u'2014-08-24 00:00:00', u'subscription_ext_uid': u'1',
                              u'next_event': u'2014-08-24 15:06:08', u'subscription_id': 315458,
                              u'start_date': u'2014-07-24 15:06:08', u'coupons': [], u'quantity': 1}}

        customer_call = {"CUSTOMERS": [
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Oli', u'LAST_NAME': u'ol', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'0,00', u'ZIPCODE': u'oli', u'BANK_ACCOUNT_MANDATE_REFERENCE': u'',
             u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'LANGUAGE_CODE': u'de', u'EMAIL': u'oli@oli.de',
             u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'', u'TAGS': u'', u'PHONE': u'',
             u'CUSTOMER_TYPE': u'business',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/2a01e7a1e717fd2ebf84e980d4888048',
             u'COUNTRY_CODE': u'DK', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'Oli', u'CUSTOMER_ID': u'697230',
             u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'X_ATTRIBUTES': u'',
             u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'c7f08e2fa58ecc497ae94bbf8d12b6d6', u'BANK_BIC': u'',
             u'CREATED': u'2014-07-24 15:06:07', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-24 15:06:07',
             u'SALUTATION': u'mr', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'oli', u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
             u'CUSTOMER_NUMBER': u'9', u'VAT_ID': u'oli', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Oli',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''}]}

        subscription_call = {u'SUBSCRIPTIONS': [{u'STATUS': u'active', u'X_ATTRIBUTES': u'', u'INVOICE_TITLE': u'',
                                                 u'HASH': u'0d124afc9c8758be0076bd5921c77346',
                                                 u'CANCELLATION_DATE': u'0000-00-00 00:00:00',
                                                 u'EXPIRATION_DATE': u'2014-08-21 12:20:22',
                                                 u'LAST_EVENT': u'2014-07-21 12:20:22',
                                                 u'START': u'2014-07-21 12:20:22', u'SUBSCRIPTION_EXT_UID': u'1',
                                                 u'NEXT_EVENT': u'2014-08-21 12:20:22', u'ARTICLE_NUMBER': u'1',
                                                 u'SUBSCRIPTION_ID': 315458, u'CUSTOMER_ID': 697230, u'ADDONS': [],
                                                 u'QUANTITY': u'1'}]}

        article_call = {u'ARTICLES': [
            {u'SUBSCRIPTION_CANCELLATION': 0, u'ARTICLE_NUMBER': u'1', u'DESCRIPTION': u'', u'TAGS': u'',
             u'TITLE': u'Test', u'TRANSLATIONS': [], u'UNIT_PRICE': u'10.0000', u'IS_ADDON': u'0',
             u'SUBSCRIPTION_TRIAL': 0, u'SUBSCRIPTION_INTERVAL': u'1 month',
             u'CHECKOUT_URL': u'https://automatic.fastbill.com/purchase/4751862ae058864485a7722930137c9f/1',
             u'SETUP_FEE': u'0.0000', u'SUBSCRIPTION_DURATION_FOLLOW': 0, u'RETURN_URL_SUCCESS': u'',
             u'VAT_PERCENT': u'19.00', u'ALLOW_MULTIPLE': u'0', u'RETURN_URL_CANCEL': u'',
             u'SUBSCRIPTION_NUMBER_EVENTS': u'0', u'CURRENCY_CODE': u'EUR', u'SUBSCRIPTION_DURATION': 0}]}

        api_call.side_effect = [
            customer_call,
            subscription_call,
            article_call
        ]

        response = self.client.post(reverse("django-fastbill-notification"), json.dumps(subscription_closed),
                                    content_type="application/json", HTTP_AUTHORIZATION=self.auth_string)
        self.assertEqual(response.status_code, 200)

        Customer.objects.get(customer_id=subscription_closed["customer"]["customer_id"])
        Subscription.objects.get(subscription_id=subscription_closed["subscription"]["subscription_id"])

    @patch("fastbill.FastbillWrapper._request")
    def test_subscription_reactivate(self, api_call):
        subscription_reactivate = {
            u'customer': {u'city': u'oli', u'customer_id': u'697230', u'hash': u'c7f08e2fa58ecc497ae94bbf8d12b6d6',
                          u'country_code': u'DK', u'firstname': u'Oli', u'companyname': u'Oli', u'lastname': u'ol',
                          u'title': u'', u'zipcode': u'oli', u'customer_number': u'9', u'telefax': u'',
                          u'telephone': u'',
                          u'address_2': u'', u'address': u'Oli', u'salutation': u'Herr',
                          u'payment_data_url': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
                          u'customer_ext_uid': 1, u'email': u'oli@oli.de',
                          u'dashboard_url': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6'},
            u'created': u'2014-07-24 15:31:12', u'type': u'subscription.reactivate', u'id': 772600,
            u'subscription': {u'status': u'active', u'hash': u'af39223ed8581bf7473c5d7ba504e552', u'article_code': u'2',
                              u'last_event': u'2014-07-24 15:06:08', u'expiration_date': u'2014-08-24 15:06:08',
                              u'cancellation_date': u'0000-00-00 00:00:00', u'subscription_ext_uid': u'1',
                              u'next_event': u'2014-08-24 15:06:08', u'subscription_id': 315458,
                              u'start_date': u'2014-07-24 15:06:08', u'coupons': [], u'quantity': u'1'}}

        customer_call = {"CUSTOMERS": [
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Oli', u'LAST_NAME': u'ol', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'0,00', u'ZIPCODE': u'oli', u'BANK_ACCOUNT_MANDATE_REFERENCE': u'',
             u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'LANGUAGE_CODE': u'de', u'EMAIL': u'oli@oli.de',
             u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'', u'TAGS': u'', u'PHONE': u'',
             u'CUSTOMER_TYPE': u'business',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/2a01e7a1e717fd2ebf84e980d4888048',
             u'COUNTRY_CODE': u'DK', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'Oli', u'CUSTOMER_ID': u'697230',
             u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'X_ATTRIBUTES': u'',
             u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'c7f08e2fa58ecc497ae94bbf8d12b6d6', u'BANK_BIC': u'',
             u'CREATED': u'2014-07-24 15:06:07', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-24 15:06:07',
             u'SALUTATION': u'mr', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'oli', u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
             u'CUSTOMER_NUMBER': u'9', u'VAT_ID': u'oli', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Oli',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''}]}

        subscription_call = {u'SUBSCRIPTIONS': [{u'STATUS': u'active', u'X_ATTRIBUTES': u'', u'INVOICE_TITLE': u'',
                                                 u'HASH': u'0d124afc9c8758be0076bd5921c77346',
                                                 u'CANCELLATION_DATE': u'0000-00-00 00:00:00',
                                                 u'EXPIRATION_DATE': u'2014-08-21 12:20:22',
                                                 u'LAST_EVENT': u'2014-07-21 12:20:22',
                                                 u'START': u'2014-07-21 12:20:22', u'SUBSCRIPTION_EXT_UID': u'1',
                                                 u'NEXT_EVENT': u'2014-08-21 12:20:22', u'ARTICLE_NUMBER': u'1',
                                                 u'SUBSCRIPTION_ID': 315458, u'CUSTOMER_ID': 697230, u'ADDONS': [],
                                                 u'QUANTITY': u'1'}]}

        article_call = {u'ARTICLES': [
            {u'SUBSCRIPTION_CANCELLATION': 0, u'ARTICLE_NUMBER': u'1', u'DESCRIPTION': u'', u'TAGS': u'',
             u'TITLE': u'Test', u'TRANSLATIONS': [], u'UNIT_PRICE': u'10.0000', u'IS_ADDON': u'0',
             u'SUBSCRIPTION_TRIAL': 0, u'SUBSCRIPTION_INTERVAL': u'1 month',
             u'CHECKOUT_URL': u'https://automatic.fastbill.com/purchase/4751862ae058864485a7722930137c9f/1',
             u'SETUP_FEE': u'0.0000', u'SUBSCRIPTION_DURATION_FOLLOW': 0, u'RETURN_URL_SUCCESS': u'',
             u'VAT_PERCENT': u'19.00', u'ALLOW_MULTIPLE': u'0', u'RETURN_URL_CANCEL': u'',
             u'SUBSCRIPTION_NUMBER_EVENTS': u'0', u'CURRENCY_CODE': u'EUR', u'SUBSCRIPTION_DURATION': 0}]}

        api_call.side_effect = [
            customer_call,
            subscription_call,
            article_call
        ]

        response = self.client.post(reverse("django-fastbill-notification"), json.dumps(subscription_reactivate),
                                    content_type="application/json", HTTP_AUTHORIZATION=self.auth_string)
        self.assertEqual(response.status_code, 200)

        Customer.objects.get(customer_id=subscription_reactivate["customer"]["customer_id"])
        Subscription.objects.get(subscription_id=subscription_reactivate["subscription"]["subscription_id"])

    @patch("fastbill.FastbillWrapper._request")
    def test_payment_created(self, api_call):
        payment_created = {
            u'customer': {u'city': u'oli', u'customer_id': u'697230', u'hash': u'c7f08e2fa58ecc497ae94bbf8d12b6d6',
                          u'country_code': u'DK', u'firstname': u'Oli', u'companyname': u'Oli', u'lastname': u'ol',
                          u'title': u'', u'zipcode': u'oli', u'customer_number': u'9', u'telefax': u'',
                          u'telephone': u'',
                          u'address_2': u'', u'address': u'Oli', u'salutation': u'Herr',
                          u'payment_data_url': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
                          u'customer_ext_uid': 1, u'email': u'oli@oli.de',
                          u'dashboard_url': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6'},
            u'created': u'2014-07-24 15:06:10', u'id': 772556, u'type': u'payment.created',
            u'payment': {u'payment_id': 409542, u'status': u'open',
                         u'invoice_url': u'https://automatic.fastbill.com/download/nrJLW_WOVBs7AGDefqTgFVMPfSEbDAhqsr2BqLPN76NB-sgotVM91eBQhBxLt',
                         u'total_amount': 20, u'reference': None, u'created': u'2014-07-24 15:06:08',
                         u'invoice_id': 506478,
                         u'next_event': u'2014-08-24 15:06:08', u'gateway': None, u'currency': u'EUR', u'test': 1,
                         u'invoice_number': u'pm108', u'type': u'charge', u'method': u'invoice'},
            u'subscription': {u'hash': u'af39223ed8581bf7473c5d7ba504e552', u'subscription_id': 315458,
                              u'subscription_ext_uid': None, u'article_code': u'1', u'quantity': u'1'}}

        customer_call = {"CUSTOMERS": [
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Oli', u'LAST_NAME': u'ol', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'0,00', u'ZIPCODE': u'oli', u'BANK_ACCOUNT_MANDATE_REFERENCE': u'',
             u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'LANGUAGE_CODE': u'de', u'EMAIL': u'oli@oli.de',
             u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'', u'TAGS': u'', u'PHONE': u'',
             u'CUSTOMER_TYPE': u'business',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/2a01e7a1e717fd2ebf84e980d4888048',
             u'COUNTRY_CODE': u'DK', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'Oli', u'CUSTOMER_ID': u'697230',
             u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'X_ATTRIBUTES': u'',
             u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'c7f08e2fa58ecc497ae94bbf8d12b6d6', u'BANK_BIC': u'',
             u'CREATED': u'2014-07-24 15:06:07', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-24 15:06:07',
             u'SALUTATION': u'mr', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'oli', u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
             u'CUSTOMER_NUMBER': u'9', u'VAT_ID': u'oli', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Oli',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''}]}

        subscription_call = {u'SUBSCRIPTIONS': [{u'STATUS': u'active', u'X_ATTRIBUTES': u'', u'INVOICE_TITLE': u'',
                                                 u'HASH': u'0d124afc9c8758be0076bd5921c77346',
                                                 u'CANCELLATION_DATE': u'0000-00-00 00:00:00',
                                                 u'EXPIRATION_DATE': u'2014-08-21 12:20:22',
                                                 u'LAST_EVENT': u'2014-07-21 12:20:22',
                                                 u'START': u'2014-07-21 12:20:22', u'SUBSCRIPTION_EXT_UID': u'1',
                                                 u'NEXT_EVENT': u'2014-08-21 12:20:22', u'ARTICLE_NUMBER': u'1',
                                                 u'SUBSCRIPTION_ID': 315458, u'CUSTOMER_ID': 697230, u'ADDONS': [],
                                                 u'QUANTITY': u'1'}]}

        article_call = {u'ARTICLES': [
            {u'SUBSCRIPTION_CANCELLATION': 0, u'ARTICLE_NUMBER': u'1', u'DESCRIPTION': u'', u'TAGS': u'',
             u'TITLE': u'Test', u'TRANSLATIONS': [], u'UNIT_PRICE': u'10.0000', u'IS_ADDON': u'0',
             u'SUBSCRIPTION_TRIAL': 0, u'SUBSCRIPTION_INTERVAL': u'1 month',
             u'CHECKOUT_URL': u'https://automatic.fastbill.com/purchase/4751862ae058864485a7722930137c9f/1',
             u'SETUP_FEE': u'0.0000', u'SUBSCRIPTION_DURATION_FOLLOW': 0, u'RETURN_URL_SUCCESS': u'',
             u'VAT_PERCENT': u'19.00', u'ALLOW_MULTIPLE': u'0', u'RETURN_URL_CANCEL': u'',
             u'SUBSCRIPTION_NUMBER_EVENTS': u'0', u'CURRENCY_CODE': u'EUR', u'SUBSCRIPTION_DURATION': 0}]}

        invoice_call = {u'INVOICES': [
            {u'BANK_NAME': [], u'FIRST_NAME': u'Oli', u'LAST_NAME': u'ol', u'BANK_CODE': [], u'ZIPCODE': u'oli',
             u'CASH_DISCOUNT_PERCENT': u'0.00',
             u'PAYMENT_INFO': u'24.07.2014 -20,00 \u20ac () CHARGEBACK | 24.07.2014 20,00 \u20ac (Bank)  | 24.07.2014 20,00 \u20ac (Bank) ',
             u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'INTROTEXT': u'', u'COMMENT': u'', u'DUE_DATE': u'2014-07-24',
             u'SUBSCRIPTION_INVOICE_COUNTER': u'1', u'IS_CANCELED': u'0',
             u'PAYPAL_URL': u'https://automatic.fastbill.com/paypal/nrJLW_WOVBs7AGDefqTgFVMPfSEbDAhqsr2BqLPN76NB-sgotVM91eBQhBxLt',
             u'CASH_DISCOUNT_DAYS': u'0', u'INVOICE_DATE': u'2014-07-24', u'PAID_DATE': u'2014-07-24 00:00:00',
             u'COUNTRY_CODE': u'DK', u'ITEMS': [
                {u'ARTICLE_NUMBER': u'2', u'DESCRIPTION': u'Testprodukt 2<br>', u'UNIT_PRICE': u'20.00000000',
                 u'COMPLETE_GROSS': 20, u'SORT_ORDER': 1, u'INVOICE_ITEM_ID': u'1019812', u'VAT_PERCENT': u'0.00',
                 u'VAT_VALUE': 0, u'COMPLETE_NET': 20, u'QUANTITY': u'1.00'}], u'ORGANIZATION': u'Oli',
             u'CUSTOMER_ID': u'697230', u'BANK_ACCOUNT_NUMBER': [], u'CURRENCY_CODE': u'EUR', u'BANK_BIC': [],
             u'BANK_IBAN': [], u'INVOICE_ID': u'506478', u'SUB_TOTAL': 20, u'DAYS_FOR_PAYMENT': 0,
             u'VAT_ITEMS': [{u'VAT_PERCENT': u'0.00', u'VAT_VALUE': 0, u'COMPLETE_NET': 20}],
             u'DOCUMENT_URL': u'https://automatic.fastbill.com/download/nrJLW_WOVBs7AGDefqTgFVMPfSEbDAhqsr2BqLPN76NB-sgotVM91eBQhBxLt',
             u'ADDRESS_2': u'', u'INVOICE_NUMBER': u'pm108', u'SALUTATION': u'mr', u'CUSTOMER_COSTCENTER_ID': u'0',
             u'CITY': u'oli', u'TOTAL': 20, u'INVOICE_TITLE': u'', u'CUSTOMER_NUMBER': u'9', u'VAT_ID': u'oli',
             u'DELIVERY_DATE': u'24.07.2014 - 23.08.2014', u'ADDRESS': u'Oli', u'BANK_ACCOUNT_OWNER': [],
             u'SUBSCRIPTION_ID': u'315458', u'TYPE': u'outgoing', u'TEMPLATE_ID': u'1', u'VAT_TOTAL': 0}]}

        api_call.side_effect = [
            customer_call,
            subscription_call,
            article_call,
            invoice_call
        ]

        response = self.client.post(reverse("django-fastbill-notification"), json.dumps(payment_created),
                                    content_type="application/json", HTTP_AUTHORIZATION=self.auth_string)
        self.assertEqual(response.status_code, 200)

        Customer.objects.get(customer_id=payment_created["customer"]["customer_id"])
        Subscription.objects.get(subscription_id=payment_created["subscription"]["subscription_id"])
        Invoice.objects.get(invoice_id=payment_created["payment"]["invoice_id"])


    @patch("fastbill.FastbillWrapper._request")
    def test_payment_failed(self, api_call):

        payment_failed = {
            u'customer': {u'city': u'oli', u'customer_id': u'697230', u'hash': u'c7f08e2fa58ecc497ae94bbf8d12b6d6',
                          u'country_code': u'DK', u'firstname': u'Oli', u'companyname': u'Oli', u'lastname': u'ol',
                          u'title': u'', u'zipcode': u'oli', u'customer_number': u'9', u'telefax': u'',
                          u'telephone': u'',
                          u'address_2': u'', u'address': u'Oli', u'salutation': u'Herr',
                          u'payment_data_url': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
                          u'customer_ext_uid': 1, u'email': u'oli@oli.de',
                          u'dashboard_url': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6'},
            u'created': u'2014-07-24 15:36:48', u'id': 772620, u'type': u'payment.failed',
            u'payment': {u'payment_id': u'409542', u'status': u'chargeback',
                         u'invoice_url': u'https://automatic.fastbill.com/download/nrJLW_WOVBs7AGDefqTgFVMPfSEbDAhqsr2BqLPN76NB-sgotVM91eBQhBxLt',
                         u'total_amount': u'20.00', u'reference': None, u'created': u'2014-07-24 15:06:08',
                         u'invoice_id': u'506478', u'next_event': None, u'gateway': None, u'currency': u'EUR',
                         u'test': 0,
                         u'invoice_number': u'pm108', u'type': u'charge', u'method': u'invoice'},
            u'subscription': {u'hash': u'af39223ed8581bf7473c5d7ba504e552', u'subscription_id': 315458,
                              u'subscription_ext_uid': None, u'article_code': u'1', u'quantity': u'1'}}

        customer_call = {"CUSTOMERS": [
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Oli', u'LAST_NAME': u'ol', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'0,00', u'ZIPCODE': u'oli', u'BANK_ACCOUNT_MANDATE_REFERENCE': u'',
             u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'LANGUAGE_CODE': u'de', u'EMAIL': u'oli@oli.de',
             u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'', u'TAGS': u'', u'PHONE': u'',
             u'CUSTOMER_TYPE': u'business',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/2a01e7a1e717fd2ebf84e980d4888048',
             u'COUNTRY_CODE': u'DK', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'Oli', u'CUSTOMER_ID': u'697230',
             u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'X_ATTRIBUTES': u'',
             u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'c7f08e2fa58ecc497ae94bbf8d12b6d6', u'BANK_BIC': u'',
             u'CREATED': u'2014-07-24 15:06:07', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-24 15:06:07',
             u'SALUTATION': u'mr', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'oli', u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
             u'CUSTOMER_NUMBER': u'9', u'VAT_ID': u'oli', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Oli',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''}]}

        subscription_call = {u'SUBSCRIPTIONS': [{u'STATUS': u'active', u'X_ATTRIBUTES': u'', u'INVOICE_TITLE': u'',
                                                 u'HASH': u'0d124afc9c8758be0076bd5921c77346',
                                                 u'CANCELLATION_DATE': u'0000-00-00 00:00:00',
                                                 u'EXPIRATION_DATE': u'2014-08-21 12:20:22',
                                                 u'LAST_EVENT': u'2014-07-21 12:20:22',
                                                 u'START': u'2014-07-21 12:20:22', u'SUBSCRIPTION_EXT_UID': u'1',
                                                 u'NEXT_EVENT': u'2014-08-21 12:20:22', u'ARTICLE_NUMBER': u'1',
                                                 u'SUBSCRIPTION_ID': 315458, u'CUSTOMER_ID': 697230, u'ADDONS': [],
                                                 u'QUANTITY': u'1'}]}

        article_call = {u'ARTICLES': [
            {u'SUBSCRIPTION_CANCELLATION': 0, u'ARTICLE_NUMBER': u'1', u'DESCRIPTION': u'', u'TAGS': u'',
             u'TITLE': u'Test', u'TRANSLATIONS': [], u'UNIT_PRICE': u'10.0000', u'IS_ADDON': u'0',
             u'SUBSCRIPTION_TRIAL': 0, u'SUBSCRIPTION_INTERVAL': u'1 month',
             u'CHECKOUT_URL': u'https://automatic.fastbill.com/purchase/4751862ae058864485a7722930137c9f/1',
             u'SETUP_FEE': u'0.0000', u'SUBSCRIPTION_DURATION_FOLLOW': 0, u'RETURN_URL_SUCCESS': u'',
             u'VAT_PERCENT': u'19.00', u'ALLOW_MULTIPLE': u'0', u'RETURN_URL_CANCEL': u'',
             u'SUBSCRIPTION_NUMBER_EVENTS': u'0', u'CURRENCY_CODE': u'EUR', u'SUBSCRIPTION_DURATION': 0}]}

        invoice_call = {u'INVOICES': [
            {u'BANK_NAME': [], u'FIRST_NAME': u'Oli', u'LAST_NAME': u'ol', u'BANK_CODE': [], u'ZIPCODE': u'oli',
             u'CASH_DISCOUNT_PERCENT': u'0.00',
             u'PAYMENT_INFO': u'24.07.2014 -20,00 \u20ac () CHARGEBACK | 24.07.2014 20,00 \u20ac (Bank)  | 24.07.2014 20,00 \u20ac (Bank) ',
             u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'INTROTEXT': u'', u'COMMENT': u'', u'DUE_DATE': u'2014-07-24',
             u'SUBSCRIPTION_INVOICE_COUNTER': u'1', u'IS_CANCELED': u'0',
             u'PAYPAL_URL': u'https://automatic.fastbill.com/paypal/nrJLW_WOVBs7AGDefqTgFVMPfSEbDAhqsr2BqLPN76NB-sgotVM91eBQhBxLt',
             u'CASH_DISCOUNT_DAYS': u'0', u'INVOICE_DATE': u'2014-07-24', u'PAID_DATE': u'2014-07-24 00:00:00',
             u'COUNTRY_CODE': u'DK', u'ITEMS': [
                {u'ARTICLE_NUMBER': u'2', u'DESCRIPTION': u'Testprodukt 2<br>', u'UNIT_PRICE': u'20.00000000',
                 u'COMPLETE_GROSS': 20, u'SORT_ORDER': 1, u'INVOICE_ITEM_ID': u'1019812', u'VAT_PERCENT': u'0.00',
                 u'VAT_VALUE': 0, u'COMPLETE_NET': 20, u'QUANTITY': u'1.00'}], u'ORGANIZATION': u'Oli',
             u'CUSTOMER_ID': u'697230', u'BANK_ACCOUNT_NUMBER': [], u'CURRENCY_CODE': u'EUR', u'BANK_BIC': [],
             u'BANK_IBAN': [], u'INVOICE_ID': u'506478', u'SUB_TOTAL': 20, u'DAYS_FOR_PAYMENT': 0,
             u'VAT_ITEMS': [{u'VAT_PERCENT': u'0.00', u'VAT_VALUE': 0, u'COMPLETE_NET': 20}],
             u'DOCUMENT_URL': u'https://automatic.fastbill.com/download/nrJLW_WOVBs7AGDefqTgFVMPfSEbDAhqsr2BqLPN76NB-sgotVM91eBQhBxLt',
             u'ADDRESS_2': u'', u'INVOICE_NUMBER': u'pm108', u'SALUTATION': u'mr', u'CUSTOMER_COSTCENTER_ID': u'0',
             u'CITY': u'oli', u'TOTAL': 20, u'INVOICE_TITLE': u'', u'CUSTOMER_NUMBER': u'9', u'VAT_ID': u'oli',
             u'DELIVERY_DATE': u'24.07.2014 - 23.08.2014', u'ADDRESS': u'Oli', u'BANK_ACCOUNT_OWNER': [],
             u'SUBSCRIPTION_ID': u'315458', u'TYPE': u'outgoing', u'TEMPLATE_ID': u'1', u'VAT_TOTAL': 0}]}

        api_call.side_effect = [
            customer_call,
            subscription_call,
            article_call,
            invoice_call
        ]

        response = self.client.post(reverse("django-fastbill-notification"), json.dumps(payment_failed),
                                    content_type="application/json", HTTP_AUTHORIZATION=self.auth_string)
        self.assertEqual(response.status_code, 200)

        Customer.objects.get(customer_id=payment_failed["customer"]["customer_id"])
        Subscription.objects.get(subscription_id=payment_failed["subscription"]["subscription_id"])
        Invoice.objects.get(invoice_id=payment_failed["payment"]["invoice_id"])

    @patch("fastbill.FastbillWrapper._request")
    def test_payment_chargeback(self, api_call):
        payment_chargeback = {
            u'customer': {u'city': u'oli', u'customer_id': u'697230', u'hash': u'c7f08e2fa58ecc497ae94bbf8d12b6d6',
                          u'country_code': u'DK', u'firstname': u'Oli', u'companyname': u'Oli', u'lastname': u'ol',
                          u'title': u'', u'zipcode': u'oli', u'customer_number': u'9', u'telefax': u'',
                          u'telephone': u'',
                          u'address_2': u'', u'address': u'Oli', u'salutation': u'Herr',
                          u'payment_data_url': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
                          u'customer_ext_uid': 1, u'email': u'oli@oli.de',
                          u'dashboard_url': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6'},
            u'created': u'2014-07-24 15:36:48', u'id': 772620, u'type': u'payment.chargeback',
            u'payment': {u'payment_id': u'409542', u'status': u'chargeback',
                         u'invoice_url': u'https://automatic.fastbill.com/download/nrJLW_WOVBs7AGDefqTgFVMPfSEbDAhqsr2BqLPN76NB-sgotVM91eBQhBxLt',
                         u'total_amount': u'20.00', u'reference': None, u'created': u'2014-07-24 15:06:08',
                         u'invoice_id': u'506478', u'next_event': None, u'gateway': None, u'currency': u'EUR',
                         u'test': 0,
                         u'invoice_number': u'pm108', u'type': u'charge', u'method': u'invoice'},
            u'subscription': {u'hash': u'af39223ed8581bf7473c5d7ba504e552', u'subscription_id': 315458,
                              u'subscription_ext_uid': None, u'article_code': u'1', u'quantity': u'1'}}

        customer_call = {"CUSTOMERS": [
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Oli', u'LAST_NAME': u'ol', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'0,00', u'ZIPCODE': u'oli', u'BANK_ACCOUNT_MANDATE_REFERENCE': u'',
             u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'LANGUAGE_CODE': u'de', u'EMAIL': u'oli@oli.de',
             u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'', u'TAGS': u'', u'PHONE': u'',
             u'CUSTOMER_TYPE': u'business',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/2a01e7a1e717fd2ebf84e980d4888048',
             u'COUNTRY_CODE': u'DK', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'Oli', u'CUSTOMER_ID': u'697230',
             u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'X_ATTRIBUTES': u'',
             u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'c7f08e2fa58ecc497ae94bbf8d12b6d6', u'BANK_BIC': u'',
             u'CREATED': u'2014-07-24 15:06:07', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-24 15:06:07',
             u'SALUTATION': u'mr', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'oli', u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
             u'CUSTOMER_NUMBER': u'9', u'VAT_ID': u'oli', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Oli',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''}]}

        subscription_call = {u'SUBSCRIPTIONS': [{u'STATUS': u'active', u'X_ATTRIBUTES': u'', u'INVOICE_TITLE': u'',
                                                 u'HASH': u'0d124afc9c8758be0076bd5921c77346',
                                                 u'CANCELLATION_DATE': u'0000-00-00 00:00:00',
                                                 u'EXPIRATION_DATE': u'2014-08-21 12:20:22',
                                                 u'LAST_EVENT': u'2014-07-21 12:20:22',
                                                 u'START': u'2014-07-21 12:20:22', u'SUBSCRIPTION_EXT_UID': u'1',
                                                 u'NEXT_EVENT': u'2014-08-21 12:20:22', u'ARTICLE_NUMBER': u'1',
                                                 u'SUBSCRIPTION_ID': 315458, u'CUSTOMER_ID': 697230, u'ADDONS': [],
                                                 u'QUANTITY': u'1'}]}

        article_call = {u'ARTICLES': [
            {u'SUBSCRIPTION_CANCELLATION': 0, u'ARTICLE_NUMBER': u'1', u'DESCRIPTION': u'', u'TAGS': u'',
             u'TITLE': u'Test', u'TRANSLATIONS': [], u'UNIT_PRICE': u'10.0000', u'IS_ADDON': u'0',
             u'SUBSCRIPTION_TRIAL': 0, u'SUBSCRIPTION_INTERVAL': u'1 month',
             u'CHECKOUT_URL': u'https://automatic.fastbill.com/purchase/4751862ae058864485a7722930137c9f/1',
             u'SETUP_FEE': u'0.0000', u'SUBSCRIPTION_DURATION_FOLLOW': 0, u'RETURN_URL_SUCCESS': u'',
             u'VAT_PERCENT': u'19.00', u'ALLOW_MULTIPLE': u'0', u'RETURN_URL_CANCEL': u'',
             u'SUBSCRIPTION_NUMBER_EVENTS': u'0', u'CURRENCY_CODE': u'EUR', u'SUBSCRIPTION_DURATION': 0}]}

        invoice_call = {u'INVOICES': [
            {u'BANK_NAME': [], u'FIRST_NAME': u'Oli', u'LAST_NAME': u'ol', u'BANK_CODE': [], u'ZIPCODE': u'oli',
             u'CASH_DISCOUNT_PERCENT': u'0.00',
             u'PAYMENT_INFO': u'24.07.2014 -20,00 \u20ac () CHARGEBACK | 24.07.2014 20,00 \u20ac (Bank)  | 24.07.2014 20,00 \u20ac (Bank) ',
             u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'INTROTEXT': u'', u'COMMENT': u'', u'DUE_DATE': u'2014-07-24',
             u'SUBSCRIPTION_INVOICE_COUNTER': u'1', u'IS_CANCELED': u'0',
             u'PAYPAL_URL': u'https://automatic.fastbill.com/paypal/nrJLW_WOVBs7AGDefqTgFVMPfSEbDAhqsr2BqLPN76NB-sgotVM91eBQhBxLt',
             u'CASH_DISCOUNT_DAYS': u'0', u'INVOICE_DATE': u'2014-07-24', u'PAID_DATE': u'2014-07-24 00:00:00',
             u'COUNTRY_CODE': u'DK', u'ITEMS': [
                {u'ARTICLE_NUMBER': u'2', u'DESCRIPTION': u'Testprodukt 2<br>', u'UNIT_PRICE': u'20.00000000',
                 u'COMPLETE_GROSS': 20, u'SORT_ORDER': 1, u'INVOICE_ITEM_ID': u'1019812', u'VAT_PERCENT': u'0.00',
                 u'VAT_VALUE': 0, u'COMPLETE_NET': 20, u'QUANTITY': u'1.00'}], u'ORGANIZATION': u'Oli',
             u'CUSTOMER_ID': u'697230', u'BANK_ACCOUNT_NUMBER': [], u'CURRENCY_CODE': u'EUR', u'BANK_BIC': [],
             u'BANK_IBAN': [], u'INVOICE_ID': u'506478', u'SUB_TOTAL': 20, u'DAYS_FOR_PAYMENT': 0,
             u'VAT_ITEMS': [{u'VAT_PERCENT': u'0.00', u'VAT_VALUE': 0, u'COMPLETE_NET': 20}],
             u'DOCUMENT_URL': u'https://automatic.fastbill.com/download/nrJLW_WOVBs7AGDefqTgFVMPfSEbDAhqsr2BqLPN76NB-sgotVM91eBQhBxLt',
             u'ADDRESS_2': u'', u'INVOICE_NUMBER': u'pm108', u'SALUTATION': u'mr', u'CUSTOMER_COSTCENTER_ID': u'0',
             u'CITY': u'oli', u'TOTAL': 20, u'INVOICE_TITLE': u'', u'CUSTOMER_NUMBER': u'9', u'VAT_ID': u'oli',
             u'DELIVERY_DATE': u'24.07.2014 - 23.08.2014', u'ADDRESS': u'Oli', u'BANK_ACCOUNT_OWNER': [],
             u'SUBSCRIPTION_ID': u'315458', u'TYPE': u'outgoing', u'TEMPLATE_ID': u'1', u'VAT_TOTAL': 0}]}

        api_call.side_effect = [
            customer_call,
            subscription_call,
            article_call,
            invoice_call
        ]

        response = self.client.post(reverse("django-fastbill-notification"), json.dumps(payment_chargeback),
                                    content_type="application/json", HTTP_AUTHORIZATION=self.auth_string)
        self.assertEqual(response.status_code, 200)

        Customer.objects.get(customer_id=payment_chargeback["customer"]["customer_id"])
        Subscription.objects.get(subscription_id=payment_chargeback["subscription"]["subscription_id"])
        Invoice.objects.get(invoice_id=payment_chargeback["payment"]["invoice_id"])

    @patch("fastbill.FastbillWrapper._request")
    def test_payment_refunded(self, api_call):
        payment_refunded = {
            u'customer': {u'city': u'oli', u'customer_id': u'697230', u'hash': u'c7f08e2fa58ecc497ae94bbf8d12b6d6',
                          u'country_code': u'DK', u'firstname': u'Oli', u'companyname': u'Oli', u'lastname': u'ol',
                          u'title': u'', u'zipcode': u'oli', u'customer_number': u'9', u'telefax': u'',
                          u'telephone': u'',
                          u'address_2': u'', u'address': u'Oli', u'salutation': u'Herr',
                          u'payment_data_url': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
                          u'customer_ext_uid': 1, u'email': u'oli@oli.de',
                          u'dashboard_url': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6'},
            u'created': u'2014-07-24 15:36:48', u'id': 772620, u'type': u'payment.refunded',
            u'payment': {u'payment_id': u'409542', u'status': u'chargeback',
                         u'invoice_url': u'https://automatic.fastbill.com/download/nrJLW_WOVBs7AGDefqTgFVMPfSEbDAhqsr2BqLPN76NB-sgotVM91eBQhBxLt',
                         u'total_amount': u'20.00', u'reference': None, u'created': u'2014-07-24 15:06:08',
                         u'invoice_id': u'506478', u'next_event': None, u'gateway': None, u'currency': u'EUR',
                         u'test': 0,
                         u'invoice_number': u'pm108', u'type': u'charge', u'method': u'invoice'},
            u'subscription': {u'hash': u'af39223ed8581bf7473c5d7ba504e552', u'subscription_id': 315458,
                              u'subscription_ext_uid': None, u'article_code': u'1', u'quantity': u'1'}}

        customer_call = {"CUSTOMERS": [
            {u'BANK_NAME': u'', u'FIRST_NAME': u'Oli', u'LAST_NAME': u'ol', u'SECONDARY_ADDRESS': u'',
             u'BANK_CODE': u'', u'CREDIT_BALANCE': u'0,00', u'ZIPCODE': u'oli', u'BANK_ACCOUNT_MANDATE_REFERENCE': u'',
             u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'LANGUAGE_CODE': u'de', u'EMAIL': u'oli@oli.de',
             u'BANK_ACCOUNT_OWNER_ZIPCODE': u'', u'COMMENT': u'', u'FAX': u'', u'TAGS': u'', u'PHONE': u'',
             u'CUSTOMER_TYPE': u'business',
             u'DASHBOARD_URL': u'https://automatic.fastbill.com/dashboard/4751862ae058864485a7722930137c9f/2a01e7a1e717fd2ebf84e980d4888048',
             u'COUNTRY_CODE': u'DK', u'SHOW_PAYMENT_NOTICE': u'0', u'ORGANIZATION': u'Oli', u'CUSTOMER_ID': u'697230',
             u'BANK_ACCOUNT_NUMBER': u'', u'CURRENCY_CODE': u'EUR', u'X_ATTRIBUTES': u'',
             u'BANK_ACCOUNT_OWNER_CITY': u'', u'HASH': u'c7f08e2fa58ecc497ae94bbf8d12b6d6', u'BANK_BIC': u'',
             u'CREATED': u'2014-07-24 15:06:07', u'BANK_IBAN': u'', u'NEWSLETTER_OPTIN': False,
             u'DAYS_FOR_PAYMENT': u'0', u'STATE': u'', u'ADDRESS_2': u'', u'LASTUPDATE': u'2014-07-24 15:06:07',
             u'SALUTATION': u'mr', u'PAYMENT_MAIL_ADDRESS': u'', u'CITY': u'oli', u'BANK_ACCOUNT_OWNER_EMAIL': u'',
             u'CHANGEDATA_URL': u'https://automatic.fastbill.com/accountdata/4751862ae058864485a7722930137c9f/c7f08e2fa58ecc497ae94bbf8d12b6d6',
             u'CUSTOMER_NUMBER': u'9', u'VAT_ID': u'oli', u'BANK_ACCOUNT_OWNER_ADDRESS': u'', u'ADDRESS': u'Oli',
             u'BANK_ACCOUNT_OWNER': u'', u'CUSTOMER_EXT_UID': 1, u'TITLE_ACADEMIC': u''}]}

        subscription_call = {u'SUBSCRIPTIONS': [{u'STATUS': u'active', u'X_ATTRIBUTES': u'', u'INVOICE_TITLE': u'',
                                                 u'HASH': u'0d124afc9c8758be0076bd5921c77346',
                                                 u'CANCELLATION_DATE': u'0000-00-00 00:00:00',
                                                 u'EXPIRATION_DATE': u'2014-08-21 12:20:22',
                                                 u'LAST_EVENT': u'2014-07-21 12:20:22',
                                                 u'START': u'2014-07-21 12:20:22', u'SUBSCRIPTION_EXT_UID': u'1',
                                                 u'NEXT_EVENT': u'2014-08-21 12:20:22', u'ARTICLE_NUMBER': u'1',
                                                 u'SUBSCRIPTION_ID': 315458, u'CUSTOMER_ID': 697230, u'ADDONS': [],
                                                 u'QUANTITY': u'1'}]}

        article_call = {u'ARTICLES': [
            {u'SUBSCRIPTION_CANCELLATION': 0, u'ARTICLE_NUMBER': u'1', u'DESCRIPTION': u'', u'TAGS': u'',
             u'TITLE': u'Test', u'TRANSLATIONS': [], u'UNIT_PRICE': u'10.0000', u'IS_ADDON': u'0',
             u'SUBSCRIPTION_TRIAL': 0, u'SUBSCRIPTION_INTERVAL': u'1 month',
             u'CHECKOUT_URL': u'https://automatic.fastbill.com/purchase/4751862ae058864485a7722930137c9f/1',
             u'SETUP_FEE': u'0.0000', u'SUBSCRIPTION_DURATION_FOLLOW': 0, u'RETURN_URL_SUCCESS': u'',
             u'VAT_PERCENT': u'19.00', u'ALLOW_MULTIPLE': u'0', u'RETURN_URL_CANCEL': u'',
             u'SUBSCRIPTION_NUMBER_EVENTS': u'0', u'CURRENCY_CODE': u'EUR', u'SUBSCRIPTION_DURATION': 0}]}

        invoice_call = {u'INVOICES': [
            {u'BANK_NAME': [], u'FIRST_NAME': u'Oli', u'LAST_NAME': u'ol', u'BANK_CODE': [], u'ZIPCODE': u'oli',
             u'CASH_DISCOUNT_PERCENT': u'0.00',
             u'PAYMENT_INFO': u'24.07.2014 -20,00 \u20ac () CHARGEBACK | 24.07.2014 20,00 \u20ac (Bank)  | 24.07.2014 20,00 \u20ac (Bank) ',
             u'AFFILIATE': u'', u'PAYMENT_TYPE': u'1', u'INTROTEXT': u'', u'COMMENT': u'', u'DUE_DATE': u'2014-07-24',
             u'SUBSCRIPTION_INVOICE_COUNTER': u'1', u'IS_CANCELED': u'0',
             u'PAYPAL_URL': u'https://automatic.fastbill.com/paypal/nrJLW_WOVBs7AGDefqTgFVMPfSEbDAhqsr2BqLPN76NB-sgotVM91eBQhBxLt',
             u'CASH_DISCOUNT_DAYS': u'0', u'INVOICE_DATE': u'2014-07-24', u'PAID_DATE': u'2014-07-24 00:00:00',
             u'COUNTRY_CODE': u'DK', u'ITEMS': [
                {u'ARTICLE_NUMBER': u'2', u'DESCRIPTION': u'Testprodukt 2<br>', u'UNIT_PRICE': u'20.00000000',
                 u'COMPLETE_GROSS': 20, u'SORT_ORDER': 1, u'INVOICE_ITEM_ID': u'1019812', u'VAT_PERCENT': u'0.00',
                 u'VAT_VALUE': 0, u'COMPLETE_NET': 20, u'QUANTITY': u'1.00'}], u'ORGANIZATION': u'Oli',
             u'CUSTOMER_ID': u'697230', u'BANK_ACCOUNT_NUMBER': [], u'CURRENCY_CODE': u'EUR', u'BANK_BIC': [],
             u'BANK_IBAN': [], u'INVOICE_ID': u'506478', u'SUB_TOTAL': 20, u'DAYS_FOR_PAYMENT': 0,
             u'VAT_ITEMS': [{u'VAT_PERCENT': u'0.00', u'VAT_VALUE': 0, u'COMPLETE_NET': 20}],
             u'DOCUMENT_URL': u'https://automatic.fastbill.com/download/nrJLW_WOVBs7AGDefqTgFVMPfSEbDAhqsr2BqLPN76NB-sgotVM91eBQhBxLt',
             u'ADDRESS_2': u'', u'INVOICE_NUMBER': u'pm108', u'SALUTATION': u'mr', u'CUSTOMER_COSTCENTER_ID': u'0',
             u'CITY': u'oli', u'TOTAL': 20, u'INVOICE_TITLE': u'', u'CUSTOMER_NUMBER': u'9', u'VAT_ID': u'oli',
             u'DELIVERY_DATE': u'24.07.2014 - 23.08.2014', u'ADDRESS': u'Oli', u'BANK_ACCOUNT_OWNER': [],
             u'SUBSCRIPTION_ID': u'315458', u'TYPE': u'outgoing', u'TEMPLATE_ID': u'1', u'VAT_TOTAL': 0}]}

        api_call.side_effect = [
            customer_call,
            subscription_call,
            article_call,
            invoice_call
        ]

        response = self.client.post(reverse("django-fastbill-notification"), json.dumps(payment_refunded),
                                    content_type="application/json", HTTP_AUTHORIZATION=self.auth_string)
        self.assertEqual(response.status_code, 200)

        Customer.objects.get(customer_id=payment_refunded["customer"]["customer_id"])
        Subscription.objects.get(subscription_id=payment_refunded["subscription"]["subscription_id"])
        Invoice.objects.get(invoice_id=payment_refunded["payment"]["invoice_id"])

