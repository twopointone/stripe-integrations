# Standard Library
import json

# Third Party Stuff
import stripe
from six import with_metaclass

# Stripe Integrations Stuff
from stripe_integrations.actions import StripeCustomer
from stripe_integrations.base.webhooks import WebhookRegistry

registry = WebhookRegistry()
del WebhookRegistry


class Registerable(type):
    def __new__(cls, clsname, bases, attrs):
        new_class = super(Registerable, cls).__new__(cls, clsname, bases, attrs)

        if getattr(new_class, "name", None) is not None:
            registry.register(new_class)

        return new_class


class BaseWebhook(with_metaclass(Registerable, object)):
    """
    REGISTRY: webhook registry
    name: webhook event name
    """

    REGISTRY = registry
    name = None

    def __init__(self, event):
        if event.kind != self.name:
            raise Exception(
                "The Webhook handler ({}) received the wrong type of Event ({})".format(
                    self.name, event.kind
                )
            )
        self.event = event

    def validate(self):
        """
        Validate incoming events
        We fetch the event data to ensure it is legit
        """
        evt = stripe.Event.retrieve(
            self.event.stripe_id,
        )
        self.event.validated_message = json.loads(
            json.dumps(
                evt.to_dict(),
                sort_keys=True,
            )
        )
        self.event.valid = self.is_event_valid(
            self.event.webhook_message["data"], self.event.validated_message["data"]
        )
        self.event.save()

    @staticmethod
    def is_event_valid(webhook_message_data, validated_message_data):
        return (
            "object" in webhook_message_data
            and "object" in validated_message_data
            and webhook_message_data["object"]["id"]
            == validated_message_data["object"]["id"]
        )

    def send_signal(self):
        signal = self.REGISTRY.get_signal(self.name)
        if signal:
            return signal.send(sender=self.__class__, event=self.event)

    def process(self):
        if self.event.processed:
            return
        self.validate()
        if not self.event.valid:
            return

        try:
            StripeCustomer.link_customer(self.event)
            self.process_webhook()
            self.send_signal()
            self.event.processed = True
            self.event.save()
        except Exception as e:
            raise e

    def process_webhook(self):
        return
