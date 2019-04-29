#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pipecashagents` package."""

import unittest
import inspect
import pipecash
import traceback


class TestPipecashAgents(unittest.TestCase):
    """Tests for `pipecashagents` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    expectedAgents = [
        "EmailSend",
        "OnNewEmail",
        "GetWalletReceiveAddress",
        "OnWalletBalanceChange",
        "WalletSend",
        "AttributeDifference",
        "NumberDifference",
        "DeDuplicationDetector",
        "DelayedEventQueue",
        "RegexFilter",
        "ForEach",
        "RssChecker",
        "ScrapeHtmlText",
        "GetHandCashAddress",
        "WatchDirectory",
        "ReadFile",
        "WriteFile",
        "WriteEventToFile",
        "ShellCommand",
        "OpReturn_B",
        "OpReturn_Bitcom",
        "OpReturn_EventAsJson",
        "Twitter_StreamListener",
        "Twitter_GetHomeTimeLine",
        "Twitter_GetUserTimeLine",
        "Twitter_GetRetweetsOfMe",
        "Twitter_GetFollowing",
        "Twitter_GetFollowers",
        "Twitter_GetBlockedUsers",
        "Twitter_WriteTweet",
        "Twitter_ReTweet",
        "Twitter_Follow",
        "Twitter_UnFollow",
        "Twitter_Block",
        "Twitter_UnBlock",
    ]

    def test_allAgents(self):
        import pipecashagents

        agents = {i: getattr(pipecashagents, i) for i in dir(pipecashagents)}
        agents = {i: agents[i] for i in agents if inspect.isclass(agents[i])}
        agents = {i: agents[i]
                  for i in agents if self.__checkIsAgent(agents[i])}

        for n in self.expectedAgents:
            assert n in agents, "expected agent %s not found" % n

        for a in agents:
            assert a in self.expectedAgents, "agent %s not listed in expectedAgents" % a

        for i in agents:
            self.__verifyAgentDefaultOptions(i, agents[i])

    def __checkIsAgent(self, agent):
        '''
        Checks:
            - has empty constructor
            - has 'description' attribute
            - description is String
        '''
        try:
            ag = agent()
            if not hasattr(ag, "description"):
                return False
            if type(ag.description) != str:
                return False
            return True
        except Exception:
            return False

    def __verifyAgentDefaultOptions(self, agentName, agentClass):
        try:
            print("-> checking agent " + agentName)
            
            ag = agentClass()

            secretNames = ag.uses_secret_variables if hasattr(ag, "uses_secret_variables") else {}
            secrets = { i:"secret var" for i in secretNames }
            default_options = ag.default_options if hasattr(ag, "default_options") else {}
            
            agWrapper = pipecash.agentWrapper.AgentWrapper(ag,
                {
                    "name": agentName + "_instance",
                    "options": default_options
                }, pipecash.secretsManager.SecretsManager(secrets) )

        except Exception as ex:

            raise AssertionError("Error when initializing AgentWrapper on %s:\n---\n%s\n---\n%s" % (
                agentName,
                str(ex),
                traceback.format_exc()
            ))
