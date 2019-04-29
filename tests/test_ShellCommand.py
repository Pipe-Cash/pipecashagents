
import unittest
import logging

from pipecash import agentWrapper

import unittest

class TestShellCommand(unittest.TestCase):
    """Tests for `pipecashagents` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_ShellCommand_sucess(self):
        from pipecashagents import ShellCommand

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = ShellCommand()
        config = {
            'name': 'agent',
            'options': {
                'commandString': "ls",
            }
        }
        agent = agentWrapper.AgentWrapper(a, config, {})
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        agent._AgentWrapper__runCheck()
        self.assertEqual(len(events), 1)
        self.assertDictEqual(events[0], { "exitCode": 0 })

        agent._AgentWrapper__runCheck()
        self.assertEqual(len(events), 2)
        self.assertDictEqual(events[1], { "exitCode": 0 })


    def test_ShellCommand_noSuchCommand(self):
        from pipecashagents import ShellCommand

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = ShellCommand()
        config = {
            'name': 'agent',
            'options': {
                'commandString': "noSuchCommand",
            }
        }
        agent = agentWrapper.AgentWrapper(a, config, {})
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        agent._AgentWrapper__runCheck()
        self.assertEqual(len(events), 1)
        self.assertDictEqual(events[0], { "exitCode": 32512 })

        agent._AgentWrapper__runCheck()
        self.assertEqual(len(events), 2)
        self.assertDictEqual(events[1], { "exitCode": 32512 })