#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pipecashagents` package."""

import unittest

class TestPipecashAgents(unittest.TestCase):
    """Tests for `pipecashagents` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_canImportWallets(self):
        from pipecashagents import EmailSend
        from pipecashagents import OnNewEmail

        from pipecashagents import GetWalletReceiveAddress
        from pipecashagents import OnWalletBalanceChange
        from pipecashagents import WalletSend

        from pipecashagents import AttributeDifference
        from pipecashagents import NumberDifference
        from pipecashagents import DeDuplicationDetector
        from pipecashagents import DelayedEventQueue
        from pipecashagents import RegexFilter
        from pipecashagents import ForEach

        from pipecashagents import RssChecker

        from pipecashagents import ScrapeHtmlText

        from pipecashagents import GetHandCashAddress

        from pipecashagents import WatchDirectory
        from pipecashagents import ReadFile
        from pipecashagents import WriteFile
        from pipecashagents import WriteEventToFile

        from pipecashagents import OpReturn_B
        from pipecashagents import OpReturn_Bitcom
        from pipecashagents import OpReturn_EventAsJson

        from pipecashagents import Twitter_StreamListener
        from pipecashagents import Twitter_GetHomeTimeLine
        from pipecashagents import Twitter_GetUserTimeLine
        from pipecashagents import Twitter_GetRetweetsOfMe
        from pipecashagents import Twitter_GetFollowing
        from pipecashagents import Twitter_GetFollowers
        from pipecashagents import Twitter_GetBlockedUsers
        from pipecashagents import Twitter_WriteTweet
        from pipecashagents import Twitter_ReTweet
        from pipecashagents import Twitter_Follow
        from pipecashagents import Twitter_UnFollow
        from pipecashagents import Twitter_Block
        from pipecashagents import Twitter_UnBlock
