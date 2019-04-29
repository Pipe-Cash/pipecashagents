import os

class ShellCommand:

    description = '''
    Executes a command on the shell of the specific OS.
    On Linux & Mac it executes on the Terminal, on Windows - in the CMD.

    Options:
        **commandString**: (string) The command to execute.
                        commandString format = "<programName> <args>"
    '''

    default_options = {
        "commandString": "{{'<programName> <programCommand> ' + argumentName}}"
    }

    event_description = {
        "exitCode": 0
    }

    def start(self, log):
        self.log = log

    def __init__(self):
        self.options = {}

    def validate_options(self):
        assert "commandString" in self.options, "'commandString' not in Options"

    def check(self, create_event):
        commandString = str(self.options['commandString'])

        exitCode = os.system(commandString)

        create_event({
            "exitCode": exitCode
        })