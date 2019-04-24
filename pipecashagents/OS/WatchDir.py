import os
import fnmatch

class WatchDirectory:

    def start(self, log):
        self.log = log
        self.prev = None

    def __init__(self):

        self.description = '''
        Watches a directory for changed files and/or folders.
        Creates events with the summory of what was changed.

        Options:
        
        - 'path': path to the directory to track
        - 'track': files/folders/all
        - 'event': new/change

        - 'filter': (optional) A wildcard to filter out the significant results.
                    Example: '*.json' will match JSON files only
                    Read the documentation for more information:
                    [Link to Docs about filtering](https://docs.python.org/2/library/fnmatch.html)
        '''

        self.options = {}

        self.default_options = {
            'path': '/home/USERNAME/Desktop/test-folder/',
            'track': 'files',
            'event': 'change',
        }

        self.event_description = {
            'event': 'change',
            'dir': '/home/USERNAME/Desktop/test-folder',
            'name': 'myfile.json',
            'path': '/home/USERNAME/Desktop/test-folder/myfile.json',
            'size': 0,
            'mtime': 1556058186.792873,
            'ctime': 1556133881.4865649
        }

    def validate_options(self):
        assert 'path' in self.options, "'path' not in options"
        assert 'track' in self.options, "'track' not in options"
        assert 'event' in self.options, "'event' not in options"
        assert os.path.exists(
            self.options['path']), "Path '%s' does not exist" % self.options['path']
        assert self.options['track'] in ['files', 'folders', 'all'], 'Unknown track option'
        assert self.options['event'] in ['new', 'change', 'all'], 'Unknown event option'

    def pathToPathObject(self, p, event):
        return {
            'event': event,
            'dir':os.path.dirname(p),
            'name':os.path.basename(p),
            'path':p,
            'size':os.path.getsize(p),
            'mtime':os.path.getmtime(p),
            'ctime':os.path.getctime(p),
        }

    def check(self, create_event):
        path = str(self.options['path'])
        track = str(self.options['track'])
        event = str(self.options['event'])
        nameFilter = str(self.options['filter'])

        paths = [os.path.join(path, n) for n in os.listdir(path)]

        if track == 'files':
            paths = [os.path.isfile(p) for p in paths]
        elif track == 'folders':
            paths = [os.path.isdir(p) for p in paths]
        if nameFilter is not None:
            paths = fnmatch.filter(paths, nameFilter)

        files = { p : os.path.getmtime(p) for p in paths }

        if self.prev is None: # first iteration.
            self.prev = files
            return
        
        prevFiles = self.prev.keys()
        results = []

        if event in ['new', 'all']:
            newPaths = [p for p in paths if p not in prevFiles]
            newResults = [self.pathToPathObject(p, 'new') for p in newPaths]
            results = results + newResults

        if event in ['change', 'all']:
            changedPaths = [p for p in paths if p in self.prev and self.prev[p] != files[p]]
            changedResults = [self.pathToPathObject(p, 'change') for p in changedPaths]
            results = results + changedResults

        for c in results:
            create_event(c)

        self.prev = files
