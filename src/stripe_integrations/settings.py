# Third Party Stuff
from django.conf import settings
from django.test.signals import setting_changed
from django.utils.module_loading import import_string

DEFAULTS = {
    "CUSTOMER_MODEL": "",
    "CARD_MODEL": "",
    "PRODUCT_MODEL": "",
    "PRICE_MODEL": "",
    "COUPON_MODEL": "",
    "EVENT_MODEL": "",
    "SUBSCRIPTION_MODEL": "",
    "CUSTOMER_FIELD_NAME": "customer",
    "USER_FIELD_NAME": "user",
    "API_VERSION": "",
    "API_KEY": "",
}

IMPORT_STRINGS = [
    "CUSTOMER_MODEL",
    "CARD_MODEL",
    "PRODUCT_MODEL",
    "PRICE_MODEL",
    "COUPON_MODEL",
    "EVENT_MODEL",
    "SUBSCRIPTION_MODEL",
]


def perform_import(val, setting_name):
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    return val


def import_from_string(val, setting_name):
    try:
        return import_string(val)
    except ImportError as e:
        msg = "Could not import '%s' for Stripe setting '%s'. %s: %s." % (
            val,
            setting_name,
            e.__class__.__name__,
            e,
        )
        raise ImportError(msg)


class StripeSettings:
    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = user_settings
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "STRIPE_CONFIG", {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid Stripe setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


stripe_settings = StripeSettings(None, DEFAULTS, IMPORT_STRINGS)


def reload_stripe_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "STRIPE_CONFIG":
        stripe_settings.reload()


setting_changed.connect(reload_stripe_settings)
