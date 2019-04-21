import datetime

import json


class TwitterAgentBase():
    uses_secret_variables = [
        "CONSUMER_KEY",
        "CONSUMER_SECRET",
        "ACCES_TOKEN",
        "ACCES_TOKEN_SECRET"
    ]

    def __init__(self):
        secrets = {}
        options = {}

    def start(self, log):
        self.log = log
        import tweepy
        self.tweepy = tweepy

    def check_dependencies_missing(self):
        import tweepy

    def getAUTH(self, secrets):
        auth = self.tweepy.OAuthHandler(secrets["CONSUMER_KEY"], secrets["CONSUMER_SECRET"])
        auth.set_access_token(secrets["ACCES_TOKEN"], secrets["ACCES_TOKEN_SECRET"])
        return auth

    def getAPI(self):
        self.auth = self.getAUTH(self.secrets)
        self.api = self.tweepy.API(self.auth,
            wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True)

        return self.api

    def getInfexOf(self, items, condition):
        index = -1
        for i in items:
            if not condition(i):
                index = index + 1
            else:
                break
        return index

    def getImportantTweetFields_Json(self, tweet):
        tweetData = {
            "created_at" : tweet['created_at'],
            "id" : tweet['id'],
            "text" : tweet['text'],
            "user_name" : tweet['user']['name'],
            "user_screen_name" : tweet['user']['screen_name'],
            "hashtags" : [i['text'] for i in tweet['entities']['hashtags']],
            "urls" : [i['expanded_url'] for i in tweet['entities']['urls']],
            "user_mentions" : [i['screen_name'] for i in tweet['entities']['user_mentions']],
            "lang" : tweet['lang'],
        }
        return tweetData

    def getImportantTweetFields(self, tweet):
        tweetData = {
            "created_at" : tweet.created_at,
            "id" : tweet.id,
            "text" : tweet.text,
            "user_name" : tweet.user.name,
            "user_screen_name" : tweet.user.screen_name,
            "hashtags" : [i['text'] for i in tweet.entities['hashtags']],
            "urls" : [i['expanded_url'] for i in tweet.entities['urls']],
            "user_mentions" : [i['screen_name'] for i in tweet.entities['user_mentions']],
            "lang" : tweet.lang,
        }
        return tweetData

    def getImportantUserFields(self, user):
        userData = {
            "created_at": user.created_at,
            "description": user.description,
            "favourites_count": user.favourites_count,
            "followers_count": user.followers_count,
            "friends_count": user.friends_count,
            "id": user.id,
            "location": user.location,
            "muting": user.muting,
            "name": user.name,
            "protected": user.protected,
            "screen_name": user.screen_name,
            "statuses_count": user.statuses_count,
            "url": user.url,
            "verified": user.verified,
        }
        return userData

    user_example_object = {
        "created_at":datetime.datetime(2018, 1, 16, 12, 2, 12),
        "description": 'Description',
        "favourites_count":2320,
        "followers_count":650,
        "friends_count":263,
        "id":952634327057409031,
        "location":'Sofia, Bulgaria',
        "muting":False,
        "name":'$bitcoinsofia',
        "protected":False,
        "screen_name":'bitcoinsofia',
        "statuses_count":1325,
        "url":'https://t.co/Von1mTVar1',
        "verified":False
    }

    tweet_example_object = {
        'created_at':datetime.datetime(2019, 4, 16, 8, 57, 19),
        'hashtags':[],
        'id':1118075888703352832,
        'lang':'en',
        'text':'Hahaha!\nThat is a master level of trolling, @abrkn !\n\nThank you!\nMade me laugh.\n\n"Only dead fish go with the flow!" https://t.co/F2mfev1OCs',
        'urls':['https://twitter.com/sideshiftai/status/1118008800420614145'],
        'user_mentions':['abrkn'],
        'user_name':'Bitcoin Sofia',
        'user_screen_name':'BitcoinSofia'
    }


class Twitter_StreamListener(TwitterAgentBase):
    description = '''
    Actively listens to all tweets on twitter, that match the 'track' filters.

    'track' - A string or list of strings, 
            specifying phrases that the tweets must include
            in order to pass the filter

    All tweets will be collected until the 'check' method is called
        where the collection will be emptied and sent as event
    '''

    tweetsCollection = []

    def stdOutListener(self):
        class _StdOutListener(self.tweepy.streaming.StreamListener):
            parent = self
            def on_data(self, data):
                parsed = json.loads(data)
                tweet = self.parent.getImportantTweetFields_Json(parsed)
                self.parent.tweetsCollection.append(tweet)
            def on_error(self, status):
                print(status)
        return _StdOutListener()
    
    default_options = {
        "track": [ "bitcoin sv", "bitcoinsv", "BSV" ]
    }

    event_description = {"tweets":[TwitterAgentBase.tweet_example_object]}

    def validate_options(self):
        assert "track" in self.options, "'track' not present in options"

    def start(self, log):
        super(Twitter_StreamListener, self).start(log)
        self.listener = self.stdOutListener()
        self.auth = self.getAUTH(self.secrets)
        self.stream = self.tweepy.Stream(self.auth, self.listener)

        track = self.options['track']
        track = track if type(track) == list else [track]

        self.stream.filter(track=track, is_async=True)
    
    def check(self, create_event):
        tweets = self.tweetsCollection
        self.tweetsCollection = []
        create_event({"tweets": tweets})


class Twitter_GetHomeTimeLine(TwitterAgentBase):
    description = '''
    Returns the 20 most recent statuses, including retweets, 
    posted by the authenticating user and that user’s friends. 
    This is the equivalent of /timeline/home on the Web.

    'new_only' - set that option to only create events with the new tweets.

    If no tweets are present, no events will be created
    '''

    def start(self, log):
        super(Twitter_GetHomeTimeLine, self).start(log)
        self.api = self.getAPI()
        self.since_id = None

    default_options = { "new_only": True }
    event_description = {"tweets":[TwitterAgentBase.tweet_example_object]}

    def check(self, create_event):
        newOnly = 'new_only' in self.options and self.options['new_only']
        tweets = self.api.home_timeline(since_id=self.since_id)
        if len(tweets)>0:
            tweets = [self.getImportantTweetFields(t) for t in tweets]
            if newOnly:
                self.since_id = tweets[0]['id']
            create_event({ "tweets": tweets })


class Twitter_GetUserTimeLine(TwitterAgentBase):
    description = '''
    Returns the 20 most recent statuses posted
    from a user’s timeline via the screen_name parameter.

    'new_only' - set that option to only create events with the new tweets.
    'screen_name' - Fill twitter username (like 'pipe_cash') to get that users tweets.
                    Leave out, to read your own tweets.

    If no tweets are present, no events will be created
    '''

    def start(self, log):
        super(Twitter_GetUserTimeLine, self).start(log)
        self.api = self.getAPI()
        self.since_id = None

    default_options = { 'new_only': True, 'screen_name': 'bitcoinsofia'}
    event_description = {"tweets":[TwitterAgentBase.tweet_example_object]}

    def check(self, create_event):
        newOnly = 'new_only' in self.options and self.options['new_only']
        screen_name = self.options['screen_name'] if 'screen_name' in self.options else None

        if screen_name is not None:
            tweets = self.api.user_timeline(screen_name, since_id=self.since_id)
        else:
            tweets = self.api.user_timeline(since_id=self.since_id)

        if len(tweets)>0:
            tweets = [self.getImportantTweetFields(t) for t in tweets]
            if newOnly:
                self.since_id = tweets[0]['id']
            create_event({ "tweets": tweets })


class Twitter_GetRetweetsOfMe(TwitterAgentBase):
    description = '''
    Returns the 20 most recent tweets of the authenticated user 
        that have been retweeted by others.

    'new_only' - set that option to only create events with the new tweets.

    If no tweets are present, no events will be created
    '''

    def start(self, log):
        super(Twitter_GetRetweetsOfMe, self).start(log)
        self.api = self.getAPI()
        self.since_id = None

    default_options = { "new_only": True }
    event_description = {"retweets":[TwitterAgentBase.tweet_example_object]}

    def check(self, create_event):
        newOnly = 'new_only' in self.options and self.options['new_only']
        tweets = self.api.retweets_of_me(since_id=self.since_id)
        if len(tweets)>0:
            tweets = [self.getImportantTweetFields(t) for t in tweets]
            if newOnly:
                self.since_id = tweets[0]['id']
            create_event({ "retweets": tweets })


class Twitter_GetFollowing(TwitterAgentBase):
    description = '''
    Returns an array containing the IDs of users 
        being followed by the specified user.

    'user' - set that option to only create events with the new tweets.
    'new_only' - set that option to only create events with the new users followed.

    If nobody is followed, no event will be created
    '''

    def start(self, log):
        super(Twitter_GetFollowing, self).start(log)
        self.api = self.getAPI()

    default_options = { "user": "bitcoinsofia", "new_only": False }
    event_description = {"following":[TwitterAgentBase.user_example_object]}

    def check(self, create_event):
        user = self.options['user'] if 'user' in self.options else None
        newOnly = 'new_only' in self.options and self.options['new_only']
        results = self.api.friends(user)
        results = [self.getImportantUserFields(i) for i in results]
        if len(results)>0:
            create_event({ "following": results })


class Twitter_GetFollowers(TwitterAgentBase):
    description = '''
    Returns an user’s followers ordered in which they were added 100 at a time.
    If no user is specified by id/screen name, it defaults to the authenticated user.

    'user' - set that option to only create events with the new tweets.

    If nobody is following, no event will be created
    '''

    def start(self, log):
        super(Twitter_GetFollowers, self).start(log)
        self.api = self.getAPI()

    default_options = { "user": "bitcoinsofia" }
    event_description = {"followers":[TwitterAgentBase.user_example_object]}

    def check(self, create_event):
        user = self.options['user'] if 'user' in self.options else None
        newOnly = 'new_only' in self.options and self.options['new_only']
        results = self.api.followers(user)
        results = [self.getImportantUserFields(i) for i in results]
        if len(results)>0:
            create_event({ "followers": results })


class Twitter_GetBlockedUsers(TwitterAgentBase):
    description = '''
    Returns an array of user objects that the authenticating user is blocking.

    If nobody is blocked, no event will be created
    '''

    def start(self, log):
        super(Twitter_GetBlockedUsers, self).start(log)
        self.api = self.getAPI()

    event_description = {"blocked_users":[TwitterAgentBase.user_example_object]}

    def check(self, create_event):
        results = self.api.blocks()
        results = [self.getImportantUserFields(i) for i in results]
        if len(results)>0:
            create_event({ "blocked_users": results })


class Twitter_WriteTweet(TwitterAgentBase):
    description = '''
    Update the authenticated user’s status.
    Statuses that are duplicates or too long will be silently ignored.

    'status' String - the text of the tweet.
    'reply_to_id' Number - (optional) the ID of the tweet to reply to.
    '''

    def start(self, log):
        super(Twitter_WriteTweet, self).start(log)
        self.api = self.getAPI()

    default_options = {
        'status': "#BitcoinSV is the real #Bitcoin",
        'reply_to_id': None,
    }

    event_description = {"tweet":TwitterAgentBase.tweet_example_object}

    def validate_options(self):
        assert "status" in self.options, "'status' not present in options"

    def receive(self, event, create_event):
        self.check(create_event)
        
    def check(self, create_event):
        status = self.options['status']
        assert len(status) > 0, "Status text can not be empty."
        reply_to_id = self.options['reply_to_id'] if 'reply_to_id' in self.options else None

        if reply_to_id is None:
            result = self.api.update_status(status)
        else:
            result = self.api.update_status(status, in_reply_to_status_id=reply_to_id)
        result = self.getImportantTweetFields(result)
        create_event({ "tweet": result })


class Twitter_ReTweet(TwitterAgentBase):
    description = '''
    Retweets a tweet. Requires the id of the tweet you are retweeting.

    'id' Number - (optional) the ID of the tweet to reply to.
    '''

    def start(self, log):
        super(Twitter_ReTweet, self).start(log)
        self.api = self.getAPI()

    default_options = {
        'id': 1118651303213916161,
    }

    event_description = {"tweet":TwitterAgentBase.tweet_example_object}

    def validate_options(self):
        assert "id" in self.options, "'id' not present in options"

    def receive(self, event, create_event):
        self.check(create_event)
        
    def check(self, create_event):
        id = self.options['id'] if 'id' in self.options else None
        result = self.api.retweet(id)
        result = self.getImportantTweetFields(result)
        create_event({ "tweet": result })


class Twitter_Follow(TwitterAgentBase):
    description = '''
    Create a new friendship with the specified user (aka follow).

    'screen_name' - Fill twitter username (like 'pipe_cash') of the user to follow.
    '''

    def start(self, log):
        super(Twitter_Follow, self).start(log)
        self.api = self.getAPI()

    default_options = { 'screen_name': 'bitcoinsofia'}

    event_description = {"followed":TwitterAgentBase.user_example_object}

    def validate_options(self):
        assert "screen_name" in self.options, "'screen_name' not present in options"

    def receive(self, event, create_event):
        self.check(create_event)
        
    def check(self, create_event):
        screen_name = self.options['screen_name'] if 'screen_name' in self.options else None
        result = self.api.create_friendship(screen_name)
        result = self.getImportantUserFields(result)
        create_event({ "followed": result })


class Twitter_UnFollow(TwitterAgentBase):
    description = '''
    Destroy a friendship with the specified user (aka unfollow).

    'screen_name' - Fill twitter username (like 'pipe_cash') of the user to unfollow.
    '''

    def start(self, log):
        super(Twitter_UnFollow, self).start(log)
        self.api = self.getAPI()

    default_options = { 'screen_name': 'Blockstream'}

    event_description = {"unfollowed":TwitterAgentBase.user_example_object}

    def validate_options(self):
        assert "screen_name" in self.options, "'screen_name' not present in options"

    def receive(self, event, create_event):
        self.check(create_event)
        
    def check(self, create_event):
        screen_name = self.options['screen_name'] if 'screen_name' in self.options else None
        result = self.api.destroy_friendship(screen_name)
        result = self.getImportantUserFields(result)
        create_event({ "unfollowed": result })


class Twitter_Block(TwitterAgentBase):
    description = '''
    Blocks the user specified in the ID parameter as the authenticating user.
    Destroys a friendship (following) to the blocked user if it exists.

    'screen_name' - Fill twitter username (like 'pipe_cash') of the user to unfollow.
    '''

    def start(self, log):
        super(Twitter_Block, self).start(log)
        self.api = self.getAPI()

    default_options = { 'screen_name': 'Blockstream'}

    event_description = {"blocked":TwitterAgentBase.user_example_object}

    def validate_options(self):
        assert "screen_name" in self.options, "'screen_name' not present in options"

    def receive(self, event, create_event):
        self.check(create_event)

    def check(self, create_event):
        screen_name = self.options['screen_name'] if 'screen_name' in self.options else None
        result = self.api.create_block(screen_name)
        result = self.getImportantUserFields(result)
        create_event({ "blocked": result })


class Twitter_UnBlock(TwitterAgentBase):
    description = '''
    Un-blocks the user specified in the ID parameter for the authenticating user.

    'screen_name' - Fill twitter username (like 'pipe_cash') of the user to unfollow.
    '''

    def start(self, log):
        super(Twitter_UnBlock, self).start(log)
        self.api = self.getAPI()

    default_options = { 'screen_name': 'bitcoinsofia'}

    event_description = {"blocked":TwitterAgentBase.user_example_object}

    def validate_options(self):
        assert "screen_name" in self.options, "'screen_name' not present in options"

    def receive(self, event, create_event):
        self.check(create_event)

    def check(self, create_event):
        screen_name = self.options['screen_name'] if 'screen_name' in self.options else None
        result = self.api.destroy_block(screen_name)
        result = self.getImportantUserFields(result)
        create_event({ "unblocked": result })
