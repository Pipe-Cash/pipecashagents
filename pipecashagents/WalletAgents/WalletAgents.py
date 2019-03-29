#TODO: implement agents

class OnWalletBalanceChange:

    description = '''Monitors the associated wallet for any change in the available funds.'''

    event_description = {
        'balance': 14.14234,
        'balanceDiff': -3.1342,
    }

    def __init__(self):
        self.wallet = None
        self.uses_wallet = True
        self.__oldBalance = None

    def start(self, log):
        self.log = log

    def check(self, create_event):
        balance = self.wallet.checkBalance()

        if self.__oldBalance is None:
            self.__oldBalance = balance
            return
        if self.__oldBalance != balance:
            create_event({
                "balance": balance,
                "balanceDiff": balance - self.__oldBalance
            })
            self.__oldBalance = balance

class GetWalletReceiveAddress:

    description = '''Asks the associated wallet for a receive address.'''

    event_description = {
        'address': '<the address>',
    }

    def __init__(self):
        self.wallet = None
        self.uses_wallet = True

    def start(self, log):
        self.log = log

    def check(self, create_event):
        ev = { "address": self.wallet.getReceiveAddress() }
        create_event(ev)

class WalletSend:

    description = '''Sends 'amount' money from the associated wallet to specified 'recipient'.'''

    event_description = { "status": "success" }

    def __init__(self):
        self.wallet = None
        self.uses_wallet = True
        self.options = {}
        self.default_options = {
            'amount': 3.14159,
            'recipient': '149vgRXB9ouVCxPq8Fx9E7QqHhreRUGruo',
        }

    def start(self, log):
        self.log = log

    def validate_options(self):
        self.verifyOption(self.options, 'amount')
        self.verifyOption(self.options, 'recipient')

    def check(self, create_event):
        self.send(create_event)

    def receive(self, eventDict, create_event):
        self.send(create_event)

    def send(self, create_event):
        try:
            self.verifyOption(self.options, 'amount', [float, int])
            self.verifyOption(self.options, 'recipient', [str])
            amount = self.options['amount']
            recipient = self.options['recipient']
            self.wallet.send(amount, recipient)
            create_event({ "status": "success" })
        except Exception as e:
            self.log.error(str(e))
            create_event({
                "status": "error",
                "error": str(e)
            })

    def verifyOption(self, options, name, typesArr=None):
        if name not in options:
            raise AttributeError("The '" + name + "' option was not present.")
        
        if typesArr is not None:
            if type(options[name]) not in typesArr:
                raise AttributeError("The '" + name + "' option should be ")