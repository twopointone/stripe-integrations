# Third Party Stuff
from django.utils.translation import gettext_lazy as _


class StripeException(Exception):
    default_detail = "Stripe error"

    def __init__(self, detail=None):
        self.detail = detail
        if not self.detail:
            self.detail = self.default_detail
        super().__init__(self.detail)


class StripeAuthException(StripeException):
    default_detail = _("Stripe auth error")
