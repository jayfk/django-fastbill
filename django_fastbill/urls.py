from django.conf.urls import patterns, url
from .notifications import notification_view
from django.views.generic import TemplateView

urlpatterns = patterns("",
                       url(r"^notification/$", notification_view, name="django-fastbill-notification"),
                       url(r"^checkout/error/$", TemplateView.as_view(template_name="django_fastbill/checkout_error.html"),
                           name="django-fastbill-error-url")
)