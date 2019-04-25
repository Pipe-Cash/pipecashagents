import os
import json
import hashlib
import base64

class OpReturnBase:

    uses_secret_variables = ['BITSV_KEY']

    def __init__(self):
        self.options = {}
        self.secrets = {}

    def start(self, log):
        import bitsv
        self.log = log
        self.bitsv = bitsv
        self.key = bitsv.Key(self.secrets['BITSV_KEY'])
        self.broadcast_rawtx = bitsv.network.services.BitIndex.broadcast_rawtx

    def check_dependencies_missing(self):
        import bitsv

    def pushData(self, dataArray, encoding='utf-8'):
        lst_of_pushdata = [(d, encoding) for d in dataArray]
        reply = self.key.send_op_return(lst_of_pushdata)
        if 'data' in reply and 'txid' in reply['data']:
            return reply['data']['txid']
        else:
            raise Exception('TXID not found in BitSV reply.\n' + json.dumps(reply))

    def readFile(path):
        if not os.path.exists(path):
            raise FileNotFoundError("File is missing: " + path)
        with open(path, 'rb') as f:
            fileContent = f.read()
        mimetype = self.filetype.guess_mime(fileContent)
        mimetype = mimetype or 'application/binary'
        return [ 
            os.path.basename(path), 
            mimetype,
            'binary',
            fileContent
        ]


class OpReturn_B(OpReturnBase):
    description = '''
    Pushes data to the Metanet in the B format.
    Documentation: https://b.bitdb.network/

    Options:
    - 'path': path to the file to be uploaded 
    
    Alternative Options (all must be present)
    - 'data': (string) The binary data to be uploaded
    - 'filename': (string) Name of the file 
    - 'media_type': (string) The media type of the data (defaults to 'text/plain')
    - 'encoding': (string) The encoding. (Defaults to UTF-8 if missing)
    '''

    default_options = {
        'data': 'hello world!',
        'media_type': 'text/plain',
        'encoding': 'utf-8',
        'filename': 'hello.txt'
    }
    
    event_description = {
        'txid': "<transaction id>",
        'B': "b://<transaction id>",
        'C': "c://<SHA256(data)>",
    }

    def validate_options(self):
        if 'path' in self.options:
            assert os.path.exists(
                self.options['path']), "Path '%s' does not exist" % self.options['path']
        else:
            assert 'data' in self.options, "'data' not in options"
            assert 'filename' in self.options, "'filename' not in options"

    def check(self, create_event):
        if 'path' in self.options:
            [ name, mimetype, encoding, fileContent ] = self.readFile(str(self.options['path']))
        else:
            fileContent = str(self.options['data'])
            mimetype = str(self.options['media_type']) if 'media_type' in self.options else 'text/plain'
            encoding = str(self.options['encoding']) if 'encoding' in self.options else 'utf-8'
            name = str(self.options['filename'])

        txid = self.pushData([
            "19HxigV4QyBv3tHpQVcUEQyq1pzZVdoAut",
            fileContent,
            mimetype,
            encoding,
            name,
        ])

        dataHash = hashlib.sha256(fileContent.encode()).digest()
        cAddr = base64.b16encode(dataHash).decode().lower()

        create_event({
            'txid': txid,
            'B': "b://" + txid,
            'C': "c://" + cAddr,
        })


class OpReturn_Bitcom(OpReturnBase):
    description = '''
    Pushes data to the Metanet in a Custom format.
    Documentation: https://b.bitdb.network/

    Options:
    - 'protocol': (bitcoin address) the id of the upload protocol being used
    - 'data': a string or array of strings, representing the data to be included after the protocol address
    
    example:
    - for the B protocol, the address will be '19HxigV4QyBv3tHpQVcUEQyq1pzZVdoAut' and the data can be:
            ["hello world!", "text/plain", 'utf-8', "hello.txt"]

    '''

    default_options = {
        'data': ["hello world!", "text/plain", "utf-8", "hello.txt"],
        'protocol': '19HxigV4QyBv3tHpQVcUEQyq1pzZVdoAut',
    }
    
    event_description = {
        'txid': "<transaction id>"
    }

    def validate_options(self):
            assert 'data' in self.options, "'data' not in options"
            assert 'protocol' in self.options, "'protocol' not in options"

    def check(self, create_event):
        data = self.options['data']
        protocol = str(self.options['protocol'])

        if type(data) != list:
            data = [str(data)]

        data = [protocol] + data

        txid = self.pushData(data)

        create_event({
            'txid': txid
        })


class OpReturn_EventAsJson(OpReturnBase):
    description = '''
    Receives events from other agents and pushes them on the blockchain with the B protocol
    Documentation: https://b.bitdb.network/
    '''

    default_options = {
    }
    
    event_description = {
        'txid': "<transaction id>"
    }

    def validate_options(self):
            assert 'data' in self.options, "'data' not in options"
            assert 'protocol' in self.options, "'protocol' not in options"

    def receive(self, event, create_event):
        fileContent = json.dumps(event)

        txid = self.pushData([
            "19HxigV4QyBv3tHpQVcUEQyq1pzZVdoAut",
            fileContent,
            'application/json',
            'UTF-8',
            'pipecash_event.json',
        ])

        dataHash = hashlib.sha256(fileContent.encode()).digest()
        cAddr = base64.b16encode(dataHash).decode().lower()

        create_event({
            'txid': txid,
            'B': "b://" + txid,
            'C': "c://" + cAddr,
        })

