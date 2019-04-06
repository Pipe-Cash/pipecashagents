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

        from pipecashagents import RssChecker
