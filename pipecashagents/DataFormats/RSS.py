import json


class RssChecker:

    description = '''Checks an RSS feed for new items.
    Creates a new event for each new feed item.

    Requirements:
        This agent depends on 'feedparser'
        Install feedparser with 'pip install feedparser'
    
    Options:
        "url": URL - the url of the RSS feed.
        "max_items": Integer - The maximum number of feed items to check. (use 0 for ALL)

    In case of failure, the created event will look like this:
    { 'state': 'error', 'error': 'Error Message' }

    In case of success, a separate event will be created for each new RSS item.
    The event will contain detailed information about the item.
    '''

    event_description = {
        'title': '',
        'title_detail': { 'type': 'text/plain', 'language': None, 'base': '', 'value': '' },
        'links': [ { 'href': '' } ],
        'link': '',
        'comments': '',
        'published': 'Fri, 05 Apr 2019 17:05:06 +0000',
        'published_parsed': [ 2019, 4, 5, 17, 5, 6, 4, 95, 0 ],
        'authors': [ {'name': ''} ],
        'author': '',
        'author_detail': {'name': ''}, 
        'tags': [ { 'term': '', 'scheme': None, 'label': None } ],
        'id': '',
        'guidislink': False,
        'summary': '',
        'summary_detail': { 'type': 'text/html', 'language': None, 'base': '', 'value': '' },
        'wfw_commentrss': '',
        'slash_comments': '0',
        'media_content': [ { 'url': '', 'duration': '145'} ],
        'media_player': { 'url': '', 'content': '' },
        'content': [ { 'type': 'text/html', 'language': None, 'base': '', 'value': ''} ],
        'media_thumbnail': [ {'url': ''} ],
        'href': '',
        'media_keywords': ''
    }

    default_options = {
        "url": "https://<website>/feed/",
        "max_items": 0
    }

    def start(self, log):
        self.log = log

    def __init__(self):
        self.options = {}
        self.first_check = True

    def check_dependencies_missing(self):
        import feedparser

    def validate_options(self):
        assert "url" in self.options, "'url' not present in options"
        assert "max_items" in self.options, "'max_items' not present in options"

    def check(self, create_event):
        try:
            self.read_rss(create_event)
        except Exception as e:
            create_event({'state': 'error', 'error': str(e)})
            raise(e)

    def read_rss(self, create_event):
        import feedparser

        url = str(self.options["url"])
        max_items = int(self.options["max_items"])
        assert max_items >= 0, "'max_items' needs to be 0 or bigger"

        feed = feedparser.parse(url)

        item_list = [json.loads(json.dumps(i)) for i in feed['items']]

        if self.first_check:
            self.latest_item_id = item_list[0]["published_parsed"]
            self.first_check = False
            return

        if max_items > 0:
            item_list = item_list[:max_items]

        new_list = []
        for i in item_list:
            if self.isArrayBigger(i["published_parsed"], self.latest_item_id):
                new_list.append(i)
                if item_list[0] == i:
                    self.latest_item_id = i["published_parsed"]
            else:
                self.latest_item_id = item_list[0]["published_parsed"]
                break

        if not any(new_list):
            return

        for i in new_list:
            create_event(i)

    def isArrayBigger(self, arr1, arr2):
        '''Returns True if arr1 is bigger than arr2'''
        for i in range(len(arr1)):
            if arr1[i] > arr2[i]:
                return True
        return False
