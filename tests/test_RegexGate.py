
import unittest
import logging

from pipecash import agentWrapper, walletWrapper

import unittest

class TestRegexFilter(unittest.TestCase):
    """Tests for `pipecashagents` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_RegexFilter_WithName(self):
        from pipecashagents import RegexFilter

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = RegexFilter()
        config = {
            'name': 'agent',
            'options': {
                'propertyName': "text",
                'regex': "\$[0-9a-zA-Z]+"
            }
        }
        agent = agentWrapper.AgentWrapper(a, config, {})
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        for i in range(3):
            agent._AgentWrapper__receiveEvent("a", "a", "a", "a", { 
                "text": "my text with $handle in it and another $HandlE after it."
            })
            self.assertEqual(len(events), i+1)
            self.assertDictEqual(events[i], { 
                "regex_matches": [ "$handle", "$HandlE" ],
                "regex_text": "my text with $handle in it and another $HandlE after it."
            })

    def test_RegexFilter_WithValue(self):
        from pipecashagents import RegexFilter

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = RegexFilter()
        config = {
            'name': 'agent',
            'options': {
                "propertyValue": "{{texts[0]+texts[0]}}",
                'regex': "\$[0-9a-zA-Z]+"
            }
        }
        agent = agentWrapper.AgentWrapper(a, config, {})
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        for i in range(3):
            agent._AgentWrapper__receiveEvent("a", "a", "a", "a", { 
                "texts": ["my text with $handle in it."]
            })
            self.assertEqual(len(events), i+1)
            self.assertDictEqual(events[i], { 
                "regex_matches": [ "$handle", "$handle" ],
                "regex_text": "my text with $handle in it.my text with $handle in it."
            })
