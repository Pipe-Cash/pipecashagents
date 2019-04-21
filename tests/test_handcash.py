
import unittest
import logging
import re

from pipecash import agentWrapper, walletWrapper

import unittest

class TestHandCash(unittest.TestCase):
    """Tests for `pipecashagents` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_GetHandCashAddress(self):
        from pipecashagents import GetHandCashAddress

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = GetHandCashAddress()
        config = {
            'name': 'agent',
            'options': {
                'handle': "bitcoinsofia",
            }
        }
        agent = agentWrapper.AgentWrapper(a, config, {})
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        agent._AgentWrapper__runCheck()
        
        self.assertEqual(len(events), 1)
        self.assertTrue('receivingAddress' in events[0])
        self.assertTrue('publicKey' in events[0])

        match = re.match("^1[a-km-zA-HJ-NP-Z1-9]{25,34}$", events[0]['receivingAddress'])
        self.assertEqual(match.string, events[0]['receivingAddress'])