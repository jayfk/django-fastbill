# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Article'
        db.create_table(u'django_fastbill_article', (
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('changed_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('subscription_cancellation', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('article_number', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('unit_price', self.gf('django.db.models.fields.FloatField')()),
            ('is_addon', self.gf('django.db.models.fields.BooleanField')()),
            ('subscription_trial', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('subscription_interval', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('checkout_url', self.gf('django.db.models.fields.URLField')(max_length=300)),
            ('setup_fee', self.gf('django.db.models.fields.FloatField')()),
            ('subscription_duration_follow', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('return_url_success', self.gf('django.db.models.fields.URLField')(max_length=300)),
            ('vat_percent', self.gf('django.db.models.fields.FloatField')()),
            ('allow_multiple', self.gf('django.db.models.fields.BooleanField')()),
            ('return_url_cancel', self.gf('django.db.models.fields.URLField')(max_length=300)),
            ('subscription_number_events', self.gf('django.db.models.fields.IntegerField')()),
            ('currency_code', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('subscription_duration', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'django_fastbill', ['Article'])

        # Adding model 'Customer'
        db.create_table(u'django_fastbill_customer', (
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('changed_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('customer_number', self.gf('django.db.models.fields.IntegerField')()),
            ('customer_ext_uid', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('customer_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('dashboard_url', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('changedata_url', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='fastbill_customer', unique=True, null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'django_fastbill', ['Customer'])

        # Adding model 'Subscription'
        db.create_table(u'django_fastbill_subscription', (
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('changed_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('x_attributes', self.gf('django.db.models.fields.TextField')()),
            ('invoice_title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('cancellation_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('expiration_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_event', self.gf('django.db.models.fields.DateTimeField')()),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('subscription_ext_uid', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('next_event', self.gf('django.db.models.fields.DateTimeField')()),
            ('article_number', self.gf('django.db.models.fields.IntegerField')()),
            ('subscription_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('customer_id', self.gf('django.db.models.fields.IntegerField')()),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('fastbill_customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subscriptions', null=True, to=orm['django_fastbill.Customer'])),
            ('fastbill_article', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subscriptions', null=True, to=orm['django_fastbill.Article'])),
        ))
        db.send_create_signal(u'django_fastbill', ['Subscription'])

        # Adding model 'Invoice'
        db.create_table(u'django_fastbill_invoice', (
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('changed_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('cash_discount_percent', self.gf('django.db.models.fields.FloatField')()),
            ('affiliate', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('payment_type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('introtext', self.gf('django.db.models.fields.TextField')()),
            ('due_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('subscription_invoice_counter', self.gf('django.db.models.fields.IntegerField')()),
            ('is_canceled', self.gf('django.db.models.fields.BooleanField')()),
            ('paypal_url', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('cash_discount_days', self.gf('django.db.models.fields.IntegerField')()),
            ('invoice_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('paid_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('customer_id', self.gf('django.db.models.fields.IntegerField')()),
            ('currency_code', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('invoice_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('sub_total', self.gf('django.db.models.fields.FloatField')()),
            ('days_for_payment', self.gf('django.db.models.fields.IntegerField')()),
            ('document_url', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('invoice_number', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('total', self.gf('django.db.models.fields.FloatField')()),
            ('customer_number', self.gf('django.db.models.fields.IntegerField')()),
            ('invoice_ttitle', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('delivery_date', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('subscription_id', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('vat_total', self.gf('django.db.models.fields.FloatField')()),
            ('template_id', self.gf('django.db.models.fields.IntegerField')()),
            ('fastbill_customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invoices', null=True, to=orm['django_fastbill.Customer'])),
            ('fastbill_subscription', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invoices', null=True, to=orm['django_fastbill.Subscription'])),
        ))
        db.send_create_signal(u'django_fastbill', ['Invoice'])


    def backwards(self, orm):
        # Deleting model 'Article'
        db.delete_table(u'django_fastbill_article')

        # Deleting model 'Customer'
        db.delete_table(u'django_fastbill_customer')

        # Deleting model 'Subscription'
        db.delete_table(u'django_fastbill_subscription')

        # Deleting model 'Invoice'
        db.delete_table(u'django_fastbill_invoice')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'django_fastbill.article': {
            'Meta': {'object_name': 'Article'},
            'allow_multiple': ('django.db.models.fields.BooleanField', [], {}),
            'article_number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'changed_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'checkout_url': ('django.db.models.fields.URLField', [], {'max_length': '300'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'currency_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'is_addon': ('django.db.models.fields.BooleanField', [], {}),
            'return_url_cancel': ('django.db.models.fields.URLField', [], {'max_length': '300'}),
            'return_url_success': ('django.db.models.fields.URLField', [], {'max_length': '300'}),
            'setup_fee': ('django.db.models.fields.FloatField', [], {}),
            'subscription_cancellation': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subscription_duration': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subscription_duration_follow': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subscription_interval': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subscription_number_events': ('django.db.models.fields.IntegerField', [], {}),
            'subscription_trial': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {}),
            'vat_percent': ('django.db.models.fields.FloatField', [], {})
        },
        u'django_fastbill.customer': {
            'Meta': {'object_name': 'Customer'},
            'changed_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'changedata_url': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'customer_ext_uid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'customer_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'customer_number': ('django.db.models.fields.IntegerField', [], {}),
            'dashboard_url': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'fastbill_customer'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'django_fastbill.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'affiliate': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'cash_discount_days': ('django.db.models.fields.IntegerField', [], {}),
            'cash_discount_percent': ('django.db.models.fields.FloatField', [], {}),
            'changed_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'currency_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'customer_id': ('django.db.models.fields.IntegerField', [], {}),
            'customer_number': ('django.db.models.fields.IntegerField', [], {}),
            'days_for_payment': ('django.db.models.fields.IntegerField', [], {}),
            'delivery_date': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'document_url': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {}),
            'fastbill_customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invoices'", 'null': 'True', 'to': u"orm['django_fastbill.Customer']"}),
            'fastbill_subscription': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invoices'", 'null': 'True', 'to': u"orm['django_fastbill.Subscription']"}),
            'introtext': ('django.db.models.fields.TextField', [], {}),
            'invoice_date': ('django.db.models.fields.DateTimeField', [], {}),
            'invoice_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'invoice_number': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'invoice_ttitle': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'is_canceled': ('django.db.models.fields.BooleanField', [], {}),
            'paid_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'paypal_url': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'sub_total': ('django.db.models.fields.FloatField', [], {}),
            'subscription_id': ('django.db.models.fields.IntegerField', [], {}),
            'subscription_invoice_counter': ('django.db.models.fields.IntegerField', [], {}),
            'template_id': ('django.db.models.fields.IntegerField', [], {}),
            'total': ('django.db.models.fields.FloatField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'vat_total': ('django.db.models.fields.FloatField', [], {})
        },
        u'django_fastbill.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'article_number': ('django.db.models.fields.IntegerField', [], {}),
            'cancellation_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'changed_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'customer_id': ('django.db.models.fields.IntegerField', [], {}),
            'expiration_date': ('django.db.models.fields.DateTimeField', [], {}),
            'fastbill_article': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriptions'", 'null': 'True', 'to': u"orm['django_fastbill.Article']"}),
            'fastbill_customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriptions'", 'null': 'True', 'to': u"orm['django_fastbill.Customer']"}),
            'invoice_title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'last_event': ('django.db.models.fields.DateTimeField', [], {}),
            'next_event': ('django.db.models.fields.DateTimeField', [], {}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'subscription_ext_uid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'subscription_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'x_attributes': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['django_fastbill']