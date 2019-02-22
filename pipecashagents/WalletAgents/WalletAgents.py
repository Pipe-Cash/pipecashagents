#TODO: implement agents

class WalletAgent_OnBalanceChange:

    description = '''Monitors the associated wallet for any change in the available funds.'''

    event_description = str({
        'balance': 14.14234,
        'balanceDiff': -3.1342,
    })

    def __init__(self):
        self.wallet = None
        self.uses_wallet = True
        self.__oldBalance = None

    def start(self, log, create_event):
        self.log = log
        self.create_event = create_event

    def check(self):
        balance = self.wallet.checkBalance()

        if self.__oldBalance is None:
            self.__oldBalance = balance
            return
        if self.__oldBalance != balance:
            self.create_event({
                "balance": balance,
                "balanceDiff": self.__oldBalance - balance
            })



class WalletAgent_GetReceiveAddress:

    description = '''Asks the associated wallet for a receive address.'''

    event_description = str({
        'address': '<the address>',
    })

    def __init__(self):
        self.wallet = None
        self.uses_wallet = True

    def start(self, log, create_event):
        self.log = log
        self.create_event = create_event

    def check(self):
        self.create_event({
            "address": self.wallet.getReceiveAddress()
        })

