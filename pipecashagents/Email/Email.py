#TODO: implement agents

class Email_Send:

    description = '''Sends an email with the specified 'title', 'body' and 'footer'.
    Provide the secret variables to connect to your email provider.
    '''

    event_description = "{ 'state': 'success' }"

    default_options = {
        'title':'',
        'body':'',
        'footer':'',
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

    def check(self):
        raise NotImplementedError()
