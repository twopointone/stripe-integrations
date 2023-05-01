# Card

Actions related to cards in Stripe that can be used for various purposes.

!!! Example
    ```python
    from stripe_integrations.actions import StripeCard

    # Set default card for a customer using the stripe provided card token
    StripeCard.set_default_card(customer, card_token)
    ```

### Set default card for a customer

This method creates a new source object, sets it as the new default source for the customer, and deletes the old default source, if there was one.

**Method**

```python
from stripe_integrations.actions import StripeCard

StripeCard.set_default_card(customer, card_token)
```

***Returns***

Local Card object

**Arguments**

| Argument   | Description                              |
| ---------- |------------------------------------------|
| customer   | Customer object to update the source for |
| card_token | The token obtained from Stripe.js         |

### Delete card

Deletes a card for a customer from both Stripe and the local database.

```python
from stripe_integrations.actions import StripeCard

StripeCard.delete_card(customer, source_stripe_id)
```
***Returns***

`None`

**Arguments**

| Argument         | Description                                     |
| ---------------- |-------------------------------------------------|
| customer         | The customer object to update the source for    |
| source_stripe_id | The Stripe ID of the card to delete from Stripe |

### Sync customer from stripe data

Updates the local payment source object with the corresponding data retrieved from Stripe.

**Method**

```python
from stripe_integrations.actions import StripeCard

StripeCard.sync_from_stripe_data(customer, source)
```

***Returns***

Local Card object

**Arguments**

| Argument | Description                                            |
| -------- |--------------------------------------------------------|
| customer | The customer object associated with the payment source |
| source   | The Stripe source data used to update the local object |

### Sync card

This method synchronizes a local Card object with the Stripe API. If no `source` is provided, it will fetch the details from Stripe.

**Method**

```python
from stripe_integrations.actions import StripeCard

StripeCard.sync(customer)
```

***Returns***

Local Card object

**Arguments**

| Argument          | Description                                                           |
| ----------------- | --------------------------------------------------------------------- |
| customer          | Customer's object                                                     |
| source (Optional) | Stripe card object that returned from stripe API <br> Default: `None` |

!!! Note
    It will fetch the details from stripe if source is not passed.

### Retrieve card for customer

Retrieves the default payment source (card) for a given customer.

**Method**

```python
from stripe_integrations.actions import StripeCard

StripeCard.get_for_customer(customer)
```

***Returns***

Local Card object

**Arguments**

| Argument | Description       |
| -------- | ----------------- |
| customer | Customer's object |

### Delete Local Card

Deletes the local card object.

**Method**

```python
from stripe_integrations.actions import StripeCard

StripeCard.delete(stripe_id)
```

***Returns***

`None`

**Arguments**

| Argument  | Description    |
| --------- | -------------- |
| stripe_id | Card stripe id |
