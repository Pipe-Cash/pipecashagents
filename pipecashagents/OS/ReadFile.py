import os
import base64


class ReadFile:

    def start(self, log):
        self.log = log

        import mimetypes
        self.mimetypes = mimetypes

    def __init__(self):

        self.description = '''
        Reads a file and returns it in the requested format.

        Options:
        - 'path': path to the file to read
        - 'format': utf8/hex/base64

        '''

        self.options = {}

        self.default_options = {
            'path': '/home/USERNAME/Desktop/test-folder/file.txt',
            'format': 'utf8',
        }

        self.event_description = {
            'fileContent': 'contents of file',
            'mimetypes': None, 
            'path': '/home/alex/Desktop/test-folder/secrets.json',
            'encoding': "utf8"
        }

    def validate_options(self):
        assert 'path' in self.options, "'path' not in options"
        assert 'format' in self.options, "'track' not in options"
        assert self.options['format'] in ['utf8','hex','base64'], "Unknown format: " + self.options['format'] 

    def check_dependencies_missing(self):
        import mimetypes

    def check(self, create_event):
        path = str(self.options['path'])
        dataFormat = str(self.options['format'])

        if not os.path.exists(path):
            raise FileNotFoundError("File is missing: " + path)
        
        if dataFormat == 'utf8':
            with open(path, 'r') as f:
                fileContent = f.read()
        elif dataFormat == 'hex':
            with open(path, 'rb') as f:
                fileContent = f.read().hex()
        elif dataFormat == 'base64':
            with open(path, 'rb') as f:
                fileContent = base64.b64encode(f.read()).decode()
        else:
            raise AttributeError("Unknown format : " + dataFormat)

        mime = self.mimetypes.guess_type(path)[0]
        mime = mime or 'application/binary'

        create_event({
            'fileContent': fileContent,
            'fileType': mime,
            'path': path,
            'format': dataFormat
        })
