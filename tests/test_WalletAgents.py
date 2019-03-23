#TODO: implement agents

import unittest
import logging

import walletMock

from pipecash import agentWrapper, walletWrapper

class TestWalletAgents(unittest.TestCase):
    """Tests for `pipecashagents` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.w = walletMock.MockWallet()
        config = { "name": "walletName" }
        self.wallet = walletWrapper.WalletWrapper(self.w, config, {})
        self.getConfig = lambda: config


    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_WalletAgent_OnBalanceChange(self):
        from pipecashagents import WalletAgent_OnBalanceChange

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = WalletAgent_OnBalanceChange()
        agent = agentWrapper.AgentWrapper(a, self.getConfig(), {})
        agent.setWallet(self.wallet)
        agent._AgentWrapper__createEvent = create_event
        agent.start()
        
        for i in range(5):
            agent._AgentWrapper__runCheck()
            self.assertListEqual(events, [])

        # change balance + receive
        self.w.addTransaction(10)

        # check - an event should be created
        agent._AgentWrapper__runCheck()
        self.assertEqual(len(events), 1)
        ev1 = events[0]
        self.assertDictEqual(ev1, {"balance": 10, "balanceDiff": 10})

        for i in range(5):
            # check again - no new events
            agent._AgentWrapper__runCheck()
            self.assertEqual(len(events), 1)

        # change balance - send
        self.w.addTransaction(-1)

        # check - an event should be created
        agent._AgentWrapper__runCheck()
        self.assertEqual(len(events), 2)
        ev2 = events[1]
        self.assertDictEqual(ev2, {"balance":9, "balanceDiff":-1})

    def test_WalletAgent_GetReceiveAddress(self):
        from pipecashagents import WalletAgent_GetReceiveAddress

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = WalletAgent_GetReceiveAddress()
        agent = agentWrapper.AgentWrapper(a, self.getConfig(), {})
        agent.setWallet(self.wallet)
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        for i in range(1, 5):
            agent._AgentWrapper__runCheck()
            self.assertEqual(len(events), i)
            ev = events[-1]
            self.assertDictEqual(ev, { "address": self.w.pubKey })