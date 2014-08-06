from django.contrib import admin
from models import Article, Customer, Subscription, Invoice


class ArticleAdmin(admin.ModelAdmin):
    pass
admin.site.register(Article, ArticleAdmin)


class CustomerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Customer, CustomerAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Subscription, SubscriptionAdmin)


class InvoiceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Invoice, InvoiceAdmin)

