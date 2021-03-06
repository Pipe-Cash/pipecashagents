import os
from datetime import datetime
import json

class WriteFile:

    description = '''
    Writes data to a file. Can overwrite, or append.

    Options:

    - 'text': the data to write

    - 'path': the path to the file.
            If the path leads to a directory, 
            filenames will be autogenerated based on time.
            If append mode - 1 file per day
            If write mode - different file every time

    - 'mode': write/append/appendLine
            write - always replaces the contents of the file, or creates a new file
            append - adds the text to the end of the existing file or creates file if not present
            appendLine - same as append, but adds the new line character after each entry
    '''

    default_options = {
        'text': '{{text}}',
        'path': '/home/user/pipecash_logs/',
        'mode': 'appendLine'
    }

    event_description = { 'outputFile': "/path/to/file.txt" }

    def start(self, log):
        pass

    def __init__(self):
        self.options = {}

    def validate_options(self):
        assert 'text' in self.options, "'text' not in options"
        assert 'path' in self.options, "'path' not in options"
        assert 'mode' in self.options, "'mode' not in options"
        m = self.options['mode']
        assert m in ['write', 'append', 'appendLine'], "unknown mode: " + m

    def generateFileNmae(self, mode):
        if mode == 'w':
            return "pipecash_" + datetime.now().strftime("%Y%m%d_%H-%M-%S_%f") + ".txt"
        if mode == 'a':
            return "pipecash_" + datetime.now().strftime("%Y%m%d") + ".txt"

    def check(self, create_event):
        text = str(self.options['text'])
        path = str(self.options['path'])

        m = 'w' if self.options['mode'] == 'write' else 'a'
        if self.options['mode'] == 'appendLine':
            text = text + os.linesep


        if os.path.basename(path) == '': # assuming dir
            pathDir = os.path.dirname(path)
            pathFile = self.generateFileNmae(m)
        else:
            pathDir = os.path.dirname(path)
            pathFile = os.path.basename(path)

        if not os.path.exists(pathDir):
            os.makedirs(pathDir)

        path = os.path.join(pathDir, pathFile)
        with open(path, m) as f:
            f.write(text)
        create_event({ 'outputFile': path })


class WriteEventToFile:

    description = '''
    Writes the event to a file. Can overwrite, or append.
    The event data can be formatted in different ways.
    It is strongly advisible to pass only events with consistent structure,
        in order to avoid invalid formatting.

    Options:

    - 'path': the path to the file.
            If the path leads to a directory, 
            filenames will be autogenerated based on time.
            If append mode - 1 file per day
            If write mode - different file every time

    - 'mode': write/append/appendLine
            write - always replaces the contents of the file, or creates a new file
            append - extends an existing file with the new data

    - 'dataFormat': json/yaml/csv
            json - will write event as json (or will append it to a json array if mode is 'append')
            yaml - will write the event in the yaml format (or add to a yaml collection if mode is 'append')
            csv - will write the event as csv (or add to csv collection if mode is 'append')

    NOTE:   if using the 'yaml' dataFormat,
            you will need to install 'PyYaml'
            
            $ pip install pyyaml
    '''

    default_options = {
        'path': '/home/user/pipecash_logs/',
        'mode': 'append',
        'dataFormat': 'csv'
    }

    event_description = { 'outputFile': "/path/to/file.json" }

    def start(self, log):
        pass

    def __init__(self):
        self.options = {}

    def validate_options(self):
        assert 'path' in self.options, "'path' not in options"
        assert 'mode' in self.options, "'mode' not in options"
        m = self.options['mode']
        assert m in ['write', 'append'], "unknown mode: " + m
        f = self.options['dataFormat']
        assert f in ['json', 'yaml', 'csv'], "unknown data format: " + f

    def generateFileNmae(self, mode, format):
        if mode == 'w':
            return "pipecash_" + datetime.now().strftime("%Y%m%d_%H-%M-%S_%f") + "." + format
        if mode == 'a':
            return "pipecash_" + datetime.now().strftime("%Y%m%d") + "." + format

    def receive(self, event, create_event):
        m = 'w' if self.options['mode'] == 'write' else 'a'
        dataFormat = self.options['dataFormat']
        path = str(self.options['path'])

        if os.path.basename(path) == '': # assuming dir
            pathDir = os.path.dirname(path)
            pathFile = self.generateFileNmae(m, dataFormat)
        else:
            pathDir = os.path.dirname(path)
            pathFile = os.path.basename(path)

        if not os.path.exists(pathDir):
            os.makedirs(pathDir)

        path = os.path.join(pathDir, pathFile)

        if dataFormat == 'json': self.writeToJSON(path, m, event)
        if dataFormat == 'yaml': self.writeToYAML(path, m, event)
        if dataFormat == 'csv': self.writeToCSV(path, m, event)
        
        create_event({ 'outputFile': path })

    def writeToJSON(self, path, m, event):
        if m == 'w':
            with open(path, m) as f:
                json.dump(event, f)
            return
        else:
            if not os.path.exists(path):
                with open(path, m) as f:
                    json.dump([ event ], f)
                return
            else:
                with open(path, 'r') as f:
                    data = json.load(f)
                    data.append(event)
                with open(path, 'w') as f:
                    json.dump(data, f)

    def listToCSVstr(self, arr):
        arr = ['"%s"' % str.replace(str(s), '"', '""') for s in arr ]
        return ','.join(arr)

    def writeToCSV(self, path, m, event):
        keys = [i for i in event if i[0] != '_']
        values = [event[i] for i in keys]
        if m == 'w':
            with open(path, m) as f:
                f.write(self.listToCSVstr(keys) + os.linesep)
                f.write(self.listToCSVstr(values) + os.linesep)
            return
        else:
            if not os.path.exists(path):
                with open(path, m) as f:
                    f.write(self.listToCSVstr(keys) + os.linesep)
                    f.write(self.listToCSVstr(values) + os.linesep)
                return
            else:
                with open(path, m) as f:
                    f.write(self.listToCSVstr(values) + os.linesep)

    def objToYAMLstr(self, obj, indent=0):
        if not hasattr(self, 'pyyaml'):
            import yaml
            self.yaml = yaml
        result = yaml.dump(obj, Dumper=yaml.CDumper)
        indentStr = '\n' + ('\t'*indent)
        result = indentStr + '- ' + str.replace(result, '\n', indentStr + '  ')
        return result

    def writeToYAML(self, path, m, event):
        if m == 'w':
            with open(path, m) as f:
                f.write('---' + os.linesep)
                f.write(self.objToYAMLstr(event) + os.linesep)
            return
        else:
            if not os.path.exists(path):
                with open(path, m) as f:
                    f.write('---' + os.linesep)
                    f.write(self.objToYAMLstr(event, 0) + os.linesep)
                return
            else:
                with open(path, m) as f:
                    f.write(self.objToYAMLstr(event, 0) + os.linesep)
