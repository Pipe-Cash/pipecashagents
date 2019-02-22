#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pipecashagents` package."""


import unittest

from pipecashagents import Binance_Buy
from pipecashagents import Binance_GetBalance
from pipecashagents import Binance_Withdraw
from pipecashagents import Email_Send
from pipecashagents import WalletAgent_GetReceiveAddress
from pipecashagents import WalletAgent_OnBalanceChange


class TestPipecashAgents(unittest.TestCase):
    """Tests for `pipecashagents` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
