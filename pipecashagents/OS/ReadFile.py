import os
import base64


class ReadFile:

    def start(self, log):
        self.log = log

        import filetype
        self.filetype = filetype

    def __init__(self):

        self.description = '''
        Reads a file and returns it in the requested format.

        Options:
        - 'path': path to the file to read
        - 'format': default/base64

        '''

        self.options = {}

        self.default_options = {
            'path': '/home/USERNAME/Desktop/test-folder/file.txt',
            'format': 'default',
        }

        self.event_description = {
            'fileContent': b'contents of file',
            'fileType': None, 
            'path': '/home/alex/Desktop/test-folder/secrets.json'}

    def validate_options(self):
        assert 'path' in self.options, "'path' not in options"
        assert 'format' in self.options, "'track' not in options"

    def check_dependencies_missing(self):
        import filetype

    def check(self, create_event):
        path = str(self.options['path'])
        dataFormat = str(self.options['format'])

        if not os.path.exists(path):
            raise FileNotFoundError("File is missing: " + path)
        
        with open(path, 'rb') as f:
            fileContent = f.read()

        mime = self.filetype.guess_mime(fileContent)
        mime = mime or 'application/binary'

        if dataFormat == 'base64':
            fileContent = base64.b64encode(fileContent)

        create_event({
            'fileContent': fileContent,
            'fileType': mime,
            'path': path,
        })



