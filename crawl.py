import tweepy
import os
from tweepy import OAuthHandler
import json
import wget
import re

consumer_key = 'E5XKKHyKbiaEevFzt43NytwBm'
consumer_secret = 'K0tZukSHIkSXYuBpzCdqzcUuTdO41wehuSeBptE6JjBmISsoL4'
access_token = '358077337-02wnlw8U7OyElkANVmIIS3GDWspcnbnVojZaBOrR'
access_secret = 'EuKESKZ4B3Le3HONY7mneGxsLo1J5YUyF6epTwjBb2t9S'

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)



#get it all!!
tweets = api.user_timeline(screen_name='wikipedigo', count=200, include_rts=False, exclude_replies=True)
last_id = tweets[-1].id
#comment this out if you dont want to get it all
#start here
while (True):
    more_tweets = api.user_timeline(screen_name='wikipedigo', count=200, include_rts=False, exclude_replies=True, max_id=last_id-1)
    if (len(more_tweets) == 0):
        break
    else:
        last_id = more_tweets[-1].id-1
        tweets = tweets + more_tweets
#end here

def whoareyou(my_file):
    filename_noext, filename_ext = os.path.splitext(my_file)
    loop = True
    n = 0
    while loop:
        if os.path.isfile(my_file):
            n = n + 1
            my_file = filename_noext + ' (' + str(n) + ')' + filename_ext
        else:
            loop = False

    if(n == 0):
        return igoname  + filename_ext
    else:
        return igoname  + ' (' + str(n) + ')' + filename_ext


media_files = set()
for status in tweets:
    media = status.entities.get('media', [])
    if(len(media) > 0):
        #media_files.add(media[0]['media_url'])
        filename = wget.download(media[0]['media_url'])
        filename_noext, filename_ext = os.path.splitext(filename)

        igoname = re.search('(.*)http.*t.co', status.text).group(1)
        igoname = ''.join([c for c in igoname if c.isalpha() or c.isdigit() or c == ' ' or c == '-']).strip()
        igoname = whoareyou(igoname + filename_ext)
        os.rename(filename, igoname)
