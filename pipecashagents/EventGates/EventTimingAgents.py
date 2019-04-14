
class DelayedEventQueue:
    description = '''
    The DelayedEventQueue stores received Events and emits them on a schedule.
    Use this as a buffer or queue of Events.

    Call the check method (with controller or schedule) to unleash the stored events.

    Options:
        `max_events` should be set to the maximum number of events that you'd like to hold in the buffer.
            When this number is reached, new events will either be ignored,
            or will displace the oldest event already in the buffer,
            depending on whether you set `keep` to `newest` or `oldest`.

        `keep` can be "newest" or "oldest", 
            specifying from which side will events be ignored if the 'max_events' option is reached.

        `emit_from` can be "newest" or "oldest", 
            specifying if the list of events should behave as a queue or as a stack.

        `max_emitted_events` is used to limit the number of the maximum events which should be created.
            If you omit this DelayAgent will create events for every event stored in the memory.
            Set to '1' if you want events to be emmited one by one.

        'group' Boolean. Set to 'true' if you want the events to be grouped,
            or 'false' if you want the events to be emmited separetely.
            If 'group' is true, the final event will look like: { "events": [ {Event1}, {Event2} ] }
            If 'group' is not specified, it will default to 'false'
    '''

    event_description = { }

    default_options = {
        'max_emitted_events': 1,
        'max_events': 100,
        'keep': 'oldest',
        'emit_from': 'oldest'
    }

    def start(self, log):
        self.log = log

    def __init__(self):
        self.options = {} 
        self.events = []
        
    def validate_options(self):
        assert "max_emitted_events" in self.options, "'max_emitted_events' not present in options"
        assert int(self.options["max_emitted_events"]) > 0, "'max_emitted_events' must be bigger than 0"

        assert "max_events" in self.options, "'max_events' not present in options"
        assert int(self.options["max_events"]) > 0, "'max_events' must be bigger than 0"

        assert "keep" in self.options, "'keep' not present in options"
        keep = self.options["keep"]
        assert type(keep) == str, "'keep' must be a string"
        assert keep == "oldest" or keep == "newest", "'keep' must be 'oldest' or 'newest'"

        assert "emit_from" in self.options, "'emit_from' not present in options"
        emit_from = self.options["emit_from"]
        assert type(emit_from) == str, "'emit_from' must be a string"
        assert emit_from == "oldest" or emit_from == "newest", "'emit_from' must be 'oldest' or 'newest'"

    def receive(self, event, create_event):
        max_events = int(self.options["max_events"])
        keep = str(self.options["keep"])

        if len(self.events) < max_events:
            self.events.append(event)
        elif keep == 'oldest':
            pass # oldest events are already stored.
        elif keep == 'newest':
            self.events = self.events[-(max_events-1):]
            self.events.append(event)

    def check(self, create_event):
        max_emitted_events = int(self.options["max_emitted_events"])
        emit_from = str(self.options["emit_from"])
        
        if emit_from == "oldest":
            eventsToEmit = self.events[:max_emitted_events]
            self.events = self.events[max_emitted_events:]
        elif emit_from == 'newest':
            eventsToEmit = reversed(self.events[-max_emitted_events:])
            self.events = self.events[:-max_emitted_events]

        group = False
        if "group" in self.options:
            group = bool(self.options["group"])

        if not group:
            for e in eventsToEmit:
                create_event(e)
        else:
            create_event({ "events": list(eventsToEmit) })

