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

class TestDifferenceDetection(unittest.TestCase):
    """Tests for `pipecashagents` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.logger = agentWrapper.logWrapper.agentLoggerInstance
        self.logMock = LogMock(self.logger)


    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_AttributeDifference(self):
        from pipecashagents import AttributeDifference

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = AttributeDifference()
        config = {
            "name": "walletName",
            "options": { "path": "name" }
        }
        agent = agentWrapper.AgentWrapper(a, config, {})
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        for i in [ "a", "a", "a", "a" ]:
            agent._AgentWrapper__receiveEvent(
                "area", "name", "state", "sender", { "name":i })
            self.assertEqual(len(events), 0)
        
        agent._AgentWrapper__receiveEvent(
            "area", "name", "state", "sender", { "name":"b" })
        self.assertEqual(len(events), 1)
        self.assertDictEqual(events[0], { "oldValue": "a", "newValue": "b" })

        for i in [ "b", "b", "b", "b" ]:
            agent._AgentWrapper__receiveEvent(
                "area", "name", "state", "sender", { "name":i })
            self.assertEqual(len(events), 1)

        agent._AgentWrapper__receiveEvent(
            "area", "name", "state", "sender", { "name":"a" })
        self.assertEqual(len(events), 2)
        self.assertDictEqual(events[1], { "oldValue": "b", "newValue": "a" })

        for i in [ "a", "a", "a", "a" ]:
            agent._AgentWrapper__receiveEvent(
                "area", "name", "state", "sender", { "name":i })
            self.assertEqual(len(events), 2)

    def test_NumberDifference(self):
        from pipecashagents import NumberDifference

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = NumberDifference()
        config = {
            "name": "walletName",
            "options": { "path": "name" }
        }
        agent = agentWrapper.AgentWrapper(a, config, {})
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        for i in [ 1,"1",1.0,"1.0" ]:
            agent._AgentWrapper__receiveEvent(
                "area", "name", "state", "sender", { "name":i })
            self.assertEqual(len(events), 0)
        
        agent._AgentWrapper__receiveEvent(
            "area", "name", "state", "sender", { "name":3 })
        self.assertEqual(len(events), 1)
        self.assertDictEqual(events[0], {'diff': 2, 'newValue': 3, 'oldValue': 1, 'percentDiff': 2.0})

        for i in [ 3,"3",3.0,"3.0" ]:
            agent._AgentWrapper__receiveEvent(
                "area", "name", "state", "sender", { "name":i })
            self.assertEqual(len(events), 1)

        agent._AgentWrapper__receiveEvent(
            "area", "name", "state", "sender", { "name":1 })
        self.assertEqual(len(events), 2)
        self.assertDictEqual(events[1], {'diff': -2, 'newValue': 1, 'oldValue': 3, 'percentDiff': -0.6667})

        for i in [ 1,"1",1.0,"1.0" ]:
            agent._AgentWrapper__receiveEvent(
                "area", "name", "state", "sender", { "name":i })
            self.assertEqual(len(events), 2)

    def test_NumberDifference_precission(self):
        from pipecashagents import NumberDifference

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = NumberDifference()
        config = {
            "name": "walletName",
            "options": { 
                "path": "name",
                "decimal_precision": 2,
            }
        }
        agent = agentWrapper.AgentWrapper(a, config, {})
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":1 })
        self.assertEqual(len(events), 0)

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":1.001 })
        self.assertEqual(len(events), 0)

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":1.01 })
        self.assertEqual(len(events), 1)
        self.assertDictEqual(events[0], {'diff': 0.01, 'newValue': 1.01, 'oldValue': 1, 'percentDiff': 0.01})

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":1.009 })
        self.assertEqual(len(events), 1)

    def test_NumberDifference_treshold(self):
        from pipecashagents import NumberDifference

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = NumberDifference()
        config = {
            "name": "walletName",
            "options": { 
                "path": "name",
                "treshold": 0.001,
            }
        }
        agent = agentWrapper.AgentWrapper(a, config, {})
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":1 })
        self.assertEqual(len(events), 0)

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":1.001 })
        self.assertEqual(len(events), 0)

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":1.002 })
        self.assertEqual(len(events), 1)
        self.assertDictEqual(events[0], {'diff': 0.001, 'newValue': 1.002, 'oldValue': 1.001, 'percentDiff': 0.001})

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":1.003 })
        self.assertEqual(len(events), 1)

    def test_NumberDifference_treshold_percent(self):
        from pipecashagents import NumberDifference

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = NumberDifference()
        config = {
            "name": "walletName",
            "options": { 
                "path": "name",
                "treshold_percent": 1
            }
        }
        agent = agentWrapper.AgentWrapper(a, config, {})
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":1 })
        self.assertEqual(len(events), 0)

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":0.999 })
        self.assertEqual(len(events), 0)

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":1 })
        self.assertEqual(len(events), 0)

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":1.011 })
        self.assertEqual(len(events), 1)
        self.assertDictEqual(events[0], {'diff': 0.011, 'newValue': 1.011, 'oldValue': 1, 'percentDiff': 0.011})

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":1.02 })
        self.assertEqual(len(events), 1)

    def test_NumberDifference_stable_value(self):
        from pipecashagents import NumberDifference

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = NumberDifference()
        config = {
            "name": "walletName",
            "options": { 
                "path": "name",
                "stable_value": 100,
                "treshold_percent": 10
            }
        }
        agent = agentWrapper.AgentWrapper(a, config, {})
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":99.9 })
        self.assertEqual(len(events), 0)

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":105 })
        self.assertEqual(len(events), 0)

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":95 })
        self.assertEqual(len(events), 0)

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":200 })
        self.assertEqual(len(events), 1)
        self.assertDictEqual(events[0], {'diff': 100, 'newValue': 200, 'oldValue': 100, 'percentDiff': 1.0})

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":105 })
        self.assertEqual(len(events), 1)

        agent._AgentWrapper__receiveEvent("area", "name", "state", "sender", { "name":80 })
        self.assertEqual(len(events), 2)
        self.assertDictEqual(events[1], {'diff': -20, 'newValue': 80, 'oldValue': 100, 'percentDiff': -0.2})

    def test_DeDuplicationDetector_propertyName(self):
        from pipecashagents import DeDuplicationDetector

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = DeDuplicationDetector()
        config = {
            "name": "walletName",
            "options": { 
                'property': 'value',
                'lookback': 10
            }
        }
        agent = agentWrapper.AgentWrapper(a, config, {})
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        for i in range(20):
            agent._AgentWrapper__receiveEvent("a", "n", "s", "s", { "value": 111 })
            self.assertEqual(len(events), 0)
        
        agent._AgentWrapper__receiveEvent("a", "n", "s", "s", { "value": 42 })
        self.assertEqual(len(events), 1)
        self.assertDictEqual(events[0], { "value": 42 })

        for i in range(9):
            agent._AgentWrapper__receiveEvent("a", "n", "s", "s", { "value": 42 })
            self.assertEqual(len(events), 1)
        
        agent._AgentWrapper__receiveEvent("a", "n", "s", "s", { "value": 111 })
        self.assertEqual(len(events), 2)
        self.assertDictEqual(events[1], { "value": 111 })

    def test_DeDuplicationDetector_wholeEvent(self):
        from pipecashagents import DeDuplicationDetector

        events = []
        def create_event(eventDict):
            events.append(eventDict)
        
        a = DeDuplicationDetector()
        config = {
            "name": "walletName",
            "options": { 
                'property': '',
                'lookback': 10
            }
        }
        agent = agentWrapper.AgentWrapper(a, config, {})
        agent._AgentWrapper__createEvent = create_event
        agent.start()

        for i in range(20):
            agent._AgentWrapper__receiveEvent("a", "n", "s", "s", { "foo": 111 })
            self.assertEqual(len(events), 0)
        
        agent._AgentWrapper__receiveEvent("a", "n", "s", "s", { "bar": 42 })
        self.assertEqual(len(events), 1)
        self.assertDictEqual(events[0], { "bar": 42 })

        for i in range(4):
            agent._AgentWrapper__receiveEvent("a", "n", "s", "s", { "bar": 42 })
            self.assertEqual(len(events), 1)
        
        agent._AgentWrapper__receiveEvent("a", "n", "s", "s", { "foo": "bar" })
        self.assertEqual(len(events), 2)
        self.assertDictEqual(events[1], {"foo":"bar"})