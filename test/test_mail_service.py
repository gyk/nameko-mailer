from nameko.runners import ServiceRunner
from nameko.testing.services import worker_factory
from nameko.testing.utils import get_container
from nameko.testing.services import entrypoint_hook, entrypoint_waiter
from nameko.testing.services import restrict_entrypoints

import sys
sys.path.insert(0, '..')

from MailService import MailService
from PaymentService import PaymentService

class TestMailService(object):
    def _get_payload(self):
        return {
            'client': {
                'name': 'John Doe',
                'email': 'john.doe@example.com'
            },
            'payee': {
                'name': 'J. Random Hacker',
                'email': 'foo@bar.baz'
            },
            'payment': {
                'amount': 8753,
                'currency': 'USD'
            }
        }

    def test_mail_service_unit(self):
        mail_service = worker_factory(MailService)
        payload = self._get_payload()

        assert mail_service.on_payment_received(payload)

        del payload['payee']
        assert mail_service.on_payment_received(payload) == False

    def test_mail_service_integration(self):
        config = {'AMQP_URI': 'amqp://guest:guest@localhost:5672/'}
        runner = ServiceRunner(config)
        runner.add_service(PaymentService)
        runner.add_service(MailService)


        payment_container = get_container(runner, PaymentService)
        mail_container = get_container(runner, MailService)

        # turns off timer event
        # restrict_entrypoints(payment_container, *[])

        runner.start()

        with entrypoint_hook(payment_container, 'emit_event') as entrypoint:
            with entrypoint_waiter(mail_container, 'on_payment_received'):
                entrypoint()

        assert True
