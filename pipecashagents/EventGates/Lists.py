import re

class ForEach:

    def start(self, log):
        self.log = log

    def __init__(self):

        self.description = '''
        Creates an event for each item in a list coming from an event.

        'listName' - name of the list property in the event

        'list' - can be used instead of 'listName' in case of more complex events.
                        example: {{text.split(' ')}} to create an event for each word in the text.
        '''

        self.options = {}

        self.default_options = {
            "list": "{{range(5)}}",
        }

        self.event_description = { 
            "item": "four",
            "index": 3
        }

    def validate_options(self):
        nameInOptions = "listName" in self.options
        valueInOptions = "list" in self.options
        assert nameInOptions or valueInOptions, "either 'listName' or 'list' must be in options"

    def receive(self, event, create_event):
        o = self.options
        listByName = o["listName"] if "listName" in o else None
        listValue = o["list"] if "list" in o else None
        collection = listValue if listValue is not None else event[listByName]
        
        if type(collection) != list:
            raise TypeError("'collection' must be a list but was " + type(collection))
        
        for i in range(len(collection)):
            create_event({
                "item": collection[i],
                "index": i
            })