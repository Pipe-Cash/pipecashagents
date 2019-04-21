import re

class RegexFilter:

    def start(self, log):
        self.log = log

    def __init__(self):

        self.description = '''
        Filters events based on a regex check against one ot it's properties.
        If the property is not a string, the str() method will be called.

        'propertyName' - name of the event property to test

        'proprtyValue' - can be used instead of 'propertyName' in case of more complex events.
                        example: {{tweets[0].text}}

        'regex' - a regex string used to check the property
        '''

        self.options = {}

        self.default_options = {
            "proprtyValue": "{{text}}",
            "regex": "\$[0-9a-zA-Z]+"
        }

        self.event_description = { 
            "regex_matches": [ "$handle", "$HandlE" ],
            "regex_text": "my text with $handle in it and another $HandlE after it."
        }

    def validate_options(self):
        nameInOptions = "propertyName" in self.options
        valueInOptions = "proprtyValue" in self.options
        assert nameInOptions or valueInOptions, "either 'propertyName' or 'proprtyValue' must be in options"
        assert "regex" in self.options, "'regex' not in options"

    def receive(self, event, create_event):
        o = self.options
        propertyName = o["propertyName"] if "propertyName" in o else None
        proprtyValue = o["proprtyValue"] if "proprtyValue" in o else None
        regex_text = str(proprtyValue if proprtyValue is not None else event[propertyName])
        regex = str(o["regex"] if "regex" in o else None)

        matches = re.findall(regex, regex_text)
        if len(matches) > 0:
            create_event({ 
            "regex_matches": matches,
            "regex_text": regex_text
        })