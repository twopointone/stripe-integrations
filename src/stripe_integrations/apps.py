# Third Party Stuff
import stripe
from django.apps import AppConfig

# Stripe Integrations Stuff
from stripe_integrations.settings import stripe_settings


class StripeIntegrationsConfig(AppConfig):
    name = "stripe_integrations"

    def ready(self):
        stripe.api_version = stripe_settings.API_VERSION
        stripe.api_key = stripe_settings.API_KEY
