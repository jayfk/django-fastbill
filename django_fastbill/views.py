from django.views.generic import DetailView, TemplateView
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from braces.views import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _


class OrderView(LoginRequiredMixin, DetailView):

    template_name = "django_fastbill/order.html"
    iframe = False

    def get_subscription_id(self, user):
        raise NotImplementedError("Subclass django_fastbill.views.OrderView and provide your own")

    def can_order(self, user, obj, article):
        return (True, _(""),) if article is not None else (False, _("Internal Error"))

    def get_context_data(self, **kwargs):

        data = super(OrderView, self).get_context_data(**kwargs)
        data["can_checkout"], data["checkout_error"] = self.can_order(self.request.user, self.object,
                                                                         self.object.article)
        data["checkout_url"] = self.object.article.checkout_url
        data["iframe"] = self.iframe
        data["customer_ext_uid"] = self.request.user.pk
        data["user_mail"] = self.request.user.email
        data["subscription_ext_uid"] = self.get_subscription_id(self.request.user)
        return data


class UserView(LoginRequiredMixin, TemplateView):

    template_name = "django_fastbill/user.html"

    def get_context_data(self, **kwargs):
        data = super(UserView, self).get_context_data(**kwargs)
        data["customer"] = self.request.user.fastbill_customer
        return data