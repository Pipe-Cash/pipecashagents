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
        from pipecashagents import EmailSend, OnNewEmail
        from pipecashagents import WalletAgent_GetReceiveAddress
        from pipecashagents import WalletAgent_OnBalanceChange
        from pipecashagents import AttributeDifference
        from pipecashagents import NumberDifference
