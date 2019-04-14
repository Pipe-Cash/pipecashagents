class AttributeDifference:
    description = '''
    The Attribute Difference Agent receives events and emits a new event with
    the difference or change of a specific attribute in comparison to the previous
    event received.

    The comparison mechanism is the standard Python "==".

    'path' specifies the name of the object in the events that's being traced.
    To track the whole event, leave the path empty.
    '''

    event_description = { 
        "oldValue": "PewDiePie",
        "newValue": "T-Series"
    }

    def start(self, log):
        self.log = log
        self.defaultObj = object()
        self.oldAttribute = self.defaultObj

    def __init__(self):

        self.options = {}
        self.default_options = {"path": "attribute name"}
        
    def validate_options(self):
        assert "path" in self.options, "'path' not present in options"

    def receive(self, event, create_event):
        index = self.options["path"]
        newAttribute = event[index]

        if self.defaultObj == self.oldAttribute:
            self.oldAttribute = newAttribute

        if self.oldAttribute != newAttribute:
            create_event({
                "oldValue": self.oldAttribute,
                "newValue": newAttribute
            })
            self.oldAttribute = newAttribute

class NumberDifference:
    description = '''
    The Number Difference Agent receives events and emits a new event with
    the difference or change of the number value of the attribute in comparison 
    to the previous event received, or in comparison to the stable value provided.

    'path' specifies the name of the object in the events that's being traced.
    To track the whole event, leave the path empty.

    'decimal_precision' can be specified if working with decimal numbers.

    'treshold' can be specified to ignore small changes (example: 0.001).

    'treshold_percent' can be specified to ignore small changes (example: 1 for ignoring < 1%).

    'stable_value' can be used to specify an expected value to compare against, instead of the previous value.
    '''

    event_description = { 
        "oldValue": 40.441,
        "newValue": 44.544,
        "diff": 4.103,
        "percentDiff": 0.10145644272
    }

    def start(self, log):
        self.log = log
        self.defaultObj = object()
        self.oldNum = self.defaultObj

    def __init__(self):

        self.options = {}
        self.default_options = {
            "path": "attribute name",
            "decimal_precision": 3,
            "treshold": 0.001,
            "treshold_percent": 1,
            # "stable_value": 100
        }
        
    def validate_options(self):
        assert "path" in self.options, "'path' not present in options"

    def receive(self, event, create_event):
        index = self.options["path"]
        newNum = event[index]

        if type(newNum) is str:
            newNum = float(newNum)

        if "decimal_precision" in self.options:
            precision = self.options["decimal_precision"]
            assert type(precision) is int, "'precision' is not an integer"
            assert precision >= 0, "'precision' must be 0 or bigger"
            newNum = round(newNum, precision)
        else:
            precision = 4

        if self.defaultObj == self.oldNum:
            if "stable_value" in self.options:
                stable_value = self.options["stable_value"]
                assert type(stable_value) is float or type(stable_value) is int, "'stable_value' must be int or float"
                self.oldNum = stable_value
            else:
                self.oldNum = newNum

        if self.oldNum != newNum:
            old = self.oldNum
            if "stable_value" not in self.options:
                self.oldNum = newNum

            diff = newNum - old
            percentDiff = diff / old

            if "treshold" in self.options:
                treshold = self.options["treshold"]
                assert type(treshold) is float or type(treshold) is int, "'treshold' must be int or float"
                assert treshold >= 0, "'treshold' must be 0 or bigger"
                if abs(diff) < treshold:
                    return

            if "treshold_percent" in self.options:
                treshold_percent = self.options["treshold_percent"]
                assert type(treshold_percent) is float or type(treshold_percent) is int, "'treshold_percent' must be int or float"
                assert treshold_percent >= 0, "'treshold_percent' must be 0 or bigger"
                if abs(percentDiff) < treshold_percent/100:
                    return
        
            create_event({
                "oldValue": old,
                "newValue": newNum,
                "diff": round(diff, precision),
                "percentDiff": round(percentDiff, precision)
            })

class DeDuplicationDetector:
    description = '''
    The De-duplication Agent receives a stream of events and remits the event if it is not a duplicate.
        `property` the value that should be used to determine the uniqueness of the event (empty to use the whole payload)
        `lookback` amount of past Events to compare the value to (0 for unlimited)
    '''

    event_description = { }

    default_options = {
        'property': '{{value}}',
        'lookback': 10
    }

    def start(self, log):
        self.log = log

    def __init__(self):
        self.options = {}
        self._memory = []
        
    def validate_options(self):
        assert "lookback" in self.options, "'lookback' not present in options"

    def receive(self, event, create_event):
        import json

        val = event
        if "property" in self.options and str(self.options["property"]) != "":
            val = event[str(self.options["property"])]

        obj_hash = hash(json.dumps(val))
        if any(self._memory):
            if obj_hash not in self._memory:
                create_event(event)
            
        lookback = int(self.options["lookback"])
        self._memory.append(obj_hash)
        if lookback > 0:
            self._memory = self._memory[-lookback:]
