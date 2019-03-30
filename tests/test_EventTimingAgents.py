
import unittest
import logging

from pipecash import agentWrapper, walletWrapper

import unittest

class TestEventTimingAgentss(unittest.TestCase):
    """Tests for `pipecashagents` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_DelayedEventQueue_queue(self):
        from pipecashagents import DelayedEventQueue

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = DelayedEventQueue()
        config = {
            'name': 'agent',
            'options': {
                'max_emitted_events': 2,
                'max_events': 10,
                'keep': 'oldest',
                'emit_from': 'oldest'
            }
        }
        agent = agentWrapper.AgentWrapper(a, config, {})
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        for i in range(20):
            agent._AgentWrapper__receiveEvent("a", "a", "a", "a", { "foo":i })
        
        agent._AgentWrapper__runCheck()
        self.assertEqual(len(events), 2)
        self.assertDictEqual(events[0], { "foo": 0 })
        self.assertDictEqual(events[1], { "foo": 1 })

        agent._AgentWrapper__runCheck()
        self.assertEqual(len(events), 4)
        self.assertDictEqual(events[2], { "foo": 2 })
        self.assertDictEqual(events[3], { "foo": 3 })

    def test_DelayedEventQueue_stack(self):
        from pipecashagents import DelayedEventQueue

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = DelayedEventQueue()
        config = {
            'name': 'agent',
            'options': {
                'max_emitted_events': 2,
                'max_events': 10,
                'keep': 'newest',
                'emit_from': 'newest'
            }
        }
        agent = agentWrapper.AgentWrapper(a, config, {})
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        for i in range(20):
            agent._AgentWrapper__receiveEvent("a", "a", "a", "a", { "foo":i })
        
        agent._AgentWrapper__runCheck()
        self.assertEqual(len(events), 2)
        self.assertDictEqual(events[0], { "foo": 19 })
        self.assertDictEqual(events[1], { "foo": 18 })

        agent._AgentWrapper__runCheck()
        self.assertEqual(len(events), 4)
        self.assertDictEqual(events[2], { "foo": 17 })
        self.assertDictEqual(events[3], { "foo": 16 })

    def test_DelayedEventQueue_stack(self):
        from pipecashagents import DelayedEventQueue

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = DelayedEventQueue()
        config = {
            'name': 'agent',
            'options': {
                'max_emitted_events': 2,
                'max_events': 10,
                'keep': 'newest',
                'emit_from': 'newest',
                'group': "true"
            }
        }
        agent = agentWrapper.AgentWrapper(a, config, {})
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        for i in range(20):
            agent._AgentWrapper__receiveEvent("a", "a", "a", "a", { "foo":i })
        
        agent._AgentWrapper__runCheck()
        self.assertEqual(len(events), 1)
        self.assertDictEqual(events[0], {"events":[{ "foo": 19 },{ "foo": 18 }]})

        agent._AgentWrapper__runCheck()
        self.assertEqual(len(events), 2)
        self.assertDictEqual(events[1], {"events":[{ "foo": 17 },{ "foo": 16 }]})
