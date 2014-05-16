import unittest

from . import testcase
from . import testing


class PublishTestCase(testcase.RabbitTestCase, unittest.TestCase):

    _multiprocess_can_split_ = True

    @testing.coroutine
    def test_publish(self):
        # declare
        yield from self.queue_declare("q", exclusive=True, no_wait=False)
        yield from self.exchange_declare("e", "fanout")
        yield from self.channel.queue_bind("q", "e", routing_key='')

        # publish
        yield from self.channel.publish("coucou", "e", routing_key='')

        # retrieve queue info from rabbitmqctl
        queues = yield from self.list_queues()
        self.assertIn("q", queues)
        self.assertEqual(1, queues["q"]['messages'])
