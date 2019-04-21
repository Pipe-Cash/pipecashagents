import json
import requests

class GetHandCashAddress:

    def start(self, log):
        self.log = log

    def __init__(self):

        self.description = '''
        Gets a bitcoin public address corresponding to the given HandCash handle

        'handle' - a string with the handcash handle.
                    like: "$bitcoinsofia"
                    if it doesn't start with '$', the '$' will be added
                    must be a single word
        '''

        self.options = {}

        self.default_options = {
            "handle": "$bitcoinsofia",
        }

        self.event_description = { 
            "receivingAddress": "1DeBSX6uSMCTj1NQECTMy5TRCciX71CmMz",
            "publicKey": "024343375e863f2c35fec81295665c9da5501df6f5816b5ef745e332dc5f188efb"
        }

    def validate_options(self):
        assert "handle" in self.options,"'handle' not in options"

    def check(self, create_event):
        handle = str(self.options["handle"]).strip()

        handle = handle[1:] if handle.startswith('$') else handle
        assert len(handle) > 0, "no handcash handle given"
        
        r = requests.get("http://api.handcash.io/api/receivingAddress/" + handle)
        response = json.loads(r.text)

        create_event({
            "receivingAddress": response['receivingAddress'],
            "publicKey": response['publicKey']
        })