
import unittest
import logging

from pipecash import agentWrapper, walletWrapper

import unittest

class TestForEach(unittest.TestCase):
    """Tests for `pipecashagents` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_ForEach_WithName(self):
        from pipecashagents import ForEach

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = ForEach()
        config = {
            'name': 'agent',
            'options': {
                'listName': "texts",
            }
        }
        agent = agentWrapper.AgentWrapper(a, config, {})
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        agent._AgentWrapper__receiveEvent("a", "a", "a", "a", { 
            "texts": ["one", "two", "three"]
        })
        self.assertEqual(len(events), 3)
        self.assertDictEqual(events[0], { "item": "one", "index": 0 })
        self.assertDictEqual(events[1], { "item": "two", "index": 1 })
        self.assertDictEqual(events[2], { "item": "three", "index": 2 })

    def test_ForEach_WithValue(self):
        from pipecashagents import ForEach

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = ForEach()
        config = {
            'name': 'agent',
            'options': {
                'list': "{{text.split(' ')}}",
            }
        }
        agent = agentWrapper.AgentWrapper(a, config, {})
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        agent._AgentWrapper__receiveEvent("a", "a", "a", "a", { 
            "text": "one two three"
        })
        self.assertEqual(len(events), 3)
        self.assertDictEqual(events[0], { "item": "one", "index": 0 })
        self.assertDictEqual(events[1], { "item": "two", "index": 1 })
        self.assertDictEqual(events[2], { "item": "three", "index": 2 })
