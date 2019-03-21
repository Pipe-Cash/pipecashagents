class ExampleMinimalAgent:

    def start(self, log):
        '''Help:
        log debug => log.debug("some string")
        log info => log.info("some string")
        log warning => log.warn("some string")
        log error => log.error("some string")
        '''
        pass

    def __init__(self):

        self.description = "A few words about the agent"
        # Describes how the wallet works and how to configure the options.
        # Markdown is permitted.

        self.options = {}
        # the options field will be populated
        #   with options from the scenario file,
        #   or with the default options.

        self.default_options = {}
        # in case no options are provided in the scenario,
        # these default options will be used.



class ExampleAgent:

    def start(self, log):
        '''Help:
        log debug => log.debug("some string")
        log info => log.info("some string")
        log warning => log.warn("some string")
        log error => log.error("some string")
        '''
        pass

    def __init__(self):

        self.description = "A few words about the agent"
        # Describes how the wallet works and how to configure the options.
        # Markdown is permitted.

        self.options = {}
        # the options field will be populated
        #   with options from the scenario file,
        #   or with the default options.

        self.default_options = {}
        # in case no options are provided in the scenario,
        # these default options will be used.

        self.wallet = None
        # Will be set to an actual wallet instance by PipeCash if:
        #   - uses_wallet is True
        #   - a wallet is provided in the scenario configuration

        self.uses_wallet = False
        # Set this variable to True if the agent needs to use a wallet.

        self.event_description = { }

        self.default_schedule = "every_1h"
        # specifies a default value of how often should the 'check' method be called.
        #
        # possible values by period:
        #
        # "every_1s", "every_2s", "every_5s", "every_10s", "every_30s",
        # "every_1m", "every_2m", "every_5m", "every_10m", "every_30m",
        # "every_1h", "every_2h", "every_5h", "every_12h",
        # "every_1d", "every_2d", "every_7d", "every_30d",
        #
        # possible values by time of day:
        #
        # "midnight", "1am", "2am", "3am", "4am", "5am",
        # "6am", "7am", "8am", "9am", "10am", "11am",
        # "noon", "1pm", "2pm", "3pm", "4pm", "5pm",
        # "6pm", "7pm", "8pm", "9pm", "10pm", "11pm"

        self.uses_secret_variables = []
        # list of secrets variable names
        #   used to get access to sensitive data
        #   that can't be included in the scenario or options.
        #   Example - wallet private keys

        self.secrets = {}
        # will be populated with variables requested in uses_secret_variables

    def validate_options(self):
        '''Called once, before the wallet is started.
        Should raise an exception if provided options are invalid'''
        pass

    def check_dependencies_missing(self):
        '''Called once, before the wallet is started.
        Should raise an exception if wallet dependencies are missing'''
        pass

    def check(self, create_event):
        '''A method to call at a scheduled intervals,
        or when a controller agent triggers an event.

        Usually used for checking a condition.

        Expected outcome options:
        - Nothing happens (if condition is negative)
        - An event is created
        - The internal state of the agent gets updated

        create event => create_event({ "someKey" : "someValue" })
        '''
        pass

    def receive(self, event, create_event):
        '''A method to call when an event from a triggering actor is created.
        The event object is passed to this method.

        Usually used for reacting on data.

        Expected outcome options:
        - An action is done
        - An event is created
        - The internal state of the agent gets updated

        create event => create_event({ "someKey" : "someValue" })
        '''
        pass
