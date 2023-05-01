# Event

Actions related to events in Stripe that can be used for various purposes.

!!! Example
    ```python
    from stripe_integrations.actions import StripeEvent

    StripeEvent.add(stripe_id, kind, livemode, api_version, message)
    ```

!!! Note
    The action is for webhook implementation purpose

## Add event

Add event that comes from stripe webhook.

!!! Info
    When a event is added, based on event type it will initialise the webhook event class and process it.

**Method**

```python
from stripe_integrations.actions import StripeEvent

StripeEvent.add(stripe_id, kind, livemode, api_version, message)
```

***Returns***

`None`

**Arguments**

| Argument         | Description                                                |
| ---------------- | ---------------------------------------------------------- |
| stripe_id        | event's stripe id                                          |
| kind             | the label of the event                                     |
| livemode         | True or False if the webhook was sent from livemode or not |
| message          | the data of the webhook                                    |
| request_id       | the id of the request that initiated the webhook           |
| pending_webhooks | the number of pending webhooks                             |
