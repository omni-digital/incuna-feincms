from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


class PaypalContent(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6,decimal_places=2)

    class Meta:
        abstract = True
        verbose_name = _('paypal')
        verbose_name_plural = _('paypals')

    def render(self, **kwargs):
        self.paypal_email = settings.PAYPAL_EMAIL
        self.paypal_url = settings.PAYPAL_URL

        return render_to_string([
            'content/paypal/%s.html' % self.region,
            'content/paypal/default.html',
            ], {'content': self})


