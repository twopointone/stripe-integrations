# Standard Library
import uuid

# Third Party Stuff
from django.db import models


class UUIDModel(models.Model):
    """An abstract base class model that makes primary key `id` as UUID
    instead of default auto incremented number.
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class TimeStampedUUIDModel(UUIDModel):
    """An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields with UUID as primary_key field.
    """

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class StripeObject(TimeStampedUUIDModel):
    """
    An abstract base class model that provides stripe_id field
    with UUID as primary_key along with self-updating
    created_at and modified_at fields
    """

    stripe_id = models.CharField(max_length=255, unique=True)
    livemode = models.BooleanField(
        default=False,
        help_text=(
            "Has the value true if the object exists in live mode or"
            "the value false if the object exists in test mode."
        ),
    )
    metadata = models.JSONField(
        null=True,
        blank=True,
        default=dict,
        help_text=(
            "Set of key-value pairs that you can attach to an object."
            "This can be useful for storing additional information "
            "about the object in a structured format."
        ),
    )

    class Meta:
        abstract = True
