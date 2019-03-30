
import unittest
import logging

from pipecash import agentWrapper, walletWrapper

try: # debug
    from walletMock import MockWallet
    from logMock import LogMock
    print("> Import")
except Exception as e: # tox
    from .walletMock import MockWallet
    from .logMock import LogMock
    print("> Import Failed : " + str(e))
    print("> Relative Import")

class TestWalletAgents(unittest.TestCase):
    """Tests for `pipecashagents` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.w = MockWallet()
        self.config = { "name": "walletName" }
        self.wallet = walletWrapper.WalletWrapper(self.w, self.config, {})

        self.logger = agentWrapper.logWrapper.agentLoggerInstance
        self.logMock = LogMock(self.logger)


    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_WalletAgent_OnBalanceChange(self):
        from pipecashagents import OnWalletBalanceChange

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = OnWalletBalanceChange()
        agent = agentWrapper.AgentWrapper(a, self.config, {})
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
        from pipecashagents import GetWalletReceiveAddress

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = GetWalletReceiveAddress()
        agent = agentWrapper.AgentWrapper(a, self.config, {})
        agent.setWallet(self.wallet)
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        for i in range(1, 5):
            agent._AgentWrapper__runCheck()
            self.assertEqual(len(events), i)
            ev = events[-1]
            self.assertDictEqual(ev, { "address": self.w.pubKey })

    def test_WalletAgent_Send(self):
        from pipecashagents import WalletSend

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = WalletSend()

        config = {
            "name": "agentName",
            "options": {
                "amount": 1,
                "recipient": "$bitcoinsofia"
            }
        }

        agent = agentWrapper.AgentWrapper(a, config, {})
        agent.setWallet(self.wallet)
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        self.w.addTransaction(10)

        with self.logMock:
            for i in range(1,3):
                agent._AgentWrapper__runCheck()
                self.assertEqual(len(events), i)
                self.assertDictEqual(events[i-1], { "status": "success" })
                self.assertEqual(self.w.checkBalance(), 10-i)
            for i in range(3,5):
                agent._AgentWrapper__receiveEvent(
                    "area", "name", "state", "sender", {})
                self.assertEqual(len(events), i)
                self.assertDictEqual(events[i-1], { "status": "success" })
                self.assertEqual(self.w.checkBalance(), 10-i)
        
        

