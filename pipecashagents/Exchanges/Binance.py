#TODO: implement agents

class Binance_Buy:

    description = '''Buys the specified amount on the specified trading pair in binance.com
    Specify your Binance connection data in the secret values.

    Examples:

    If the pair is "BCHSVBTC" and the amount is 10,
    the actor will attempt to buy 10 Bitcoin SV by paying with as much BTC as needed.

    If the pair is "BCHSVBTC" and the amount is -2,
    the actor will attempt to sell 2 Bitcoin SV for as much BTC as it is currently exchanged for.
    '''

    event_description = str({
        'state': 'success',
        'bought':'BTC',
        'amount': 1.0,
        'pair': 'BTCUSDT'
    })

    default_options = {
        'amount': -1,
        'pair': 'BTCUSD'
    }

    def start(self, log, create_event):
        self.log = log
        self.create_event = create_event

    def __init__(self):
        self.options = { }
        self.uses_secret_variables = []
        self.secrets = {}

    def receive(self, event):
        raise NotImplementedError()


class Binance_GetBalance:

    description = '''Checks your binance.com profile to get the balance for the specific ticker.
    Specify your Binance connection data in the secret values.
    '''

    event_description = str({
        'state': 'success',
        'ticker':'BCHSV',
        'balance': 1.012
    })

    default_options = {
        'ticker': 'BCHSV'
    }

    def start(self, log, create_event):
        self.log = log
        self.create_event = create_event

    def __init__(self):
        self.options = { }
        self.uses_secret_variables = []
        self.secrets = {}

    def receive(self, event):
        raise NotImplementedError()

    def check(self, event):
        raise NotImplementedError()


class Binance_Withdraw:

    description = '''Connects to your binance.com profile and attempts to make a withdraw.
    Attempts to withdraw the specified 'amount' from the specified 'ticker'.

    Specify your Binance connection data in the secret values.
    '''

    event_description = str({
        'state': 'success',
        'ticker':'BCHSV',
        'withdrawn': 1.0
    })

    default_options = {
        'ticker': 'BCHSV',
        'amount': 7
    }

    def start(self, log, create_event):
        self.log = log
        self.create_event = create_event

    def __init__(self):
        self.options = { }
        self.uses_secret_variables = []
        self.secrets = {}

    def receive(self, event):
        raise NotImplementedError()

