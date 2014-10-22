from django.contrib import admin
from models import Article, Customer, Subscription, Invoice
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

class FastBillAdmin(admin.ModelAdmin):

    extra = ()

    def get_readonly_fields(self, request, obj=None):
        return tuple(self.model._meta.get_all_field_names()) + self.extra


    def subscriptions(self, instance):
        return format_html_join(
            mark_safe('<br/>'),
            '<a href="{0}">{1}</a>',
            ((reverse("admin:django_fastbill_subscription_change", args=(line.pk,)), line,) for line in instance.subscriptions),
        )

    def invoices(self, instance):
        return format_html_join(
            mark_safe('<br/>'),
            '<a href="{0}">{1}</a>',
            ((reverse("admin:django_fastbill_invoice_change", args=(line.pk,)), line,) for line in instance.invoices),
        )

    def customer(self, instance):
        cust = instance.customer
        return None if cust is None else mark_safe(
            '<a href="%s">%s</a>' % (reverse("admin:django_fastbill_customer_change", args=(cust.pk,)), cust,))

    def subscription(self, instance):
        sub = instance.subscription
        return None if sub is None else mark_safe(
            '<a href="%s">%s</a>' % (reverse("admin:django_fastbill_subscription_change", args=(sub.pk,)), sub,))

    def article(self, instance):
        art = instance.article
        return None if art is None else mark_safe(
            '<a href="%s">%s</a>' % (reverse("admin:django_fastbill_article_change", args=(art.pk,)), art,))


class ArticleAdmin(FastBillAdmin):
    extra = ("subscriptions",)
admin.site.register(Article, ArticleAdmin)


class CustomerAdmin(FastBillAdmin):
    extra = ("invoices", "subscriptions")

admin.site.register(Customer, CustomerAdmin)

class SubscriptionAdmin(FastBillAdmin):

    extra = ("invoices", "customer", "article")
admin.site.register(Subscription, SubscriptionAdmin)

class InvoiceAdmin(FastBillAdmin):

    extra = ("customer", "subscription")

admin.site.register(Invoice, InvoiceAdmin)
