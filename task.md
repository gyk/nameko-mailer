# Programming Task

Write a [nameko](https://nameko.readthedocs.org) service that sends an email via [Mandrill](https://mandrill.com) whenever an [event](http://nameko.readthedocs.org/en/latest/built_in_extensions.html#events-pub-sub) is received from another service.

The email sent via Mandrill should be plaintext with the following body:

```
Dear {payee},

You have received a payment of {amount} {currency} from {client} ({email}).

Yours,
student.com
```

Below is a service you can use to generate appropriate events while prototyping. Its only dependencies are [Faker](http://fake-factory.readthedocs.org) and nameko. While running it will dispatch an event every 10 seconds.

``` python
from faker import Factory

from nameko.events import EventDispatcher
from nameko.timer import timer

fake = Factory.create()


class PaymentService(object):
    name = "payments"

    dispatch = EventDispatcher()

    @timer(interval=10)
    def emit_event(self):

        payload = {
            'client': {
                'name': fake.name(),
                'email': fake.safe_email()
            },
            'payee': {
                'name': fake.name(),
                'email': fake.safe_email()
            },
            'payment': {
                'amount': fake.random_int(),
                'currency': fake.random_element(
                    ("USD", "GBP", "EUR")
                )
            }
        }
        self.dispatch("payment_received", payload)
```

You can create a free and disposable account on Mandrill to integrate your service against.

Your solution should be a single nameko service plus unit and integration tests for it. Take as long as you need to produce something that is as complete and polished as you can. Feel free to email any questions to matt.bennett@student.com, we expect there will be some.

When you test your service, be sure to apply the `eventlet.monkey_patch()`. If you choose pytest to run your tests, it will be automatically applied for you.
