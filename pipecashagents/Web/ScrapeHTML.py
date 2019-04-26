
class ScrapeHtmlText:
    
    description = '''
    Gets the full text of the HTML page at the specified URL.
    Javascript and CSS will be ignored

    Requirements:
        - 'beautifulsoup4' ( "pip install beautifulsoup4" )

    Options:
        - 'url': the URL of the page
    '''

    default_options = {
        "url": "http://pipe.cash/"
    }

    event_description = {
        "html": '<!DOCTYPE html><html lang="en">.....</html>',
        "text": 'The text on the page, without HTML tags and without Scripts'
    }

    def start(self, log):
        import requests
        import bs4
        self.log = log
        self.requests = requests
        self.bs4 = bs4

    def __init__(self):
        self.options = {}

    def validate_options(self):
        assert 'url' in self.options, "'url' not in options"

    def check_dependencies_missing(self):
        import requests
        import bs4

    def check(self, create_event):
        url = str(self.options['url'])

        html = self.requests.get(url).text
        soup = self.bs4.BeautifulSoup(html)

        for tag in soup(["script", "style"]):
            tag.extract()

        text = soup.get_text()
        lines = [line.strip() for line in text.splitlines()]
        chunks = [phrase.strip() for line in lines for phrase in line.split("  ")]
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        create_event({
            "html": html,
            "text": text
        })