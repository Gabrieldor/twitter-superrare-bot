# import the module
import tweepy
import re
import datetime
import json

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        u"\u2026"
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

# fetch all statuses until it finds a statuses that is older than 7 days
def fetch_statuses(screen_name, id = None):
    statuses = api.user_timeline(screen_name = screen_name, count = 200, max_id = id)
    td = datetime.datetime.today().day

    # get each status and check if it is older than 7 days
    for status in statuses:
        date = status.created_at
        day = date.weekday()
        if day == 6 and date.day != td:
            ind = statuses.index(status)
            return statuses[:ind]
        else:
            id = statuses[-1].id
    return statuses + fetch_statuses(screen_name, id)
        

# assign the values accordingly
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# set access to user's access key and access secret
auth.set_access_token(access_token, access_token_secret)

# calling the api
api = tweepy.API(auth)




# screen name of the account to be fetched
screen_name = "SuperRareBot"


# fetching the statuses
statuses = fetch_statuses(screen_name)
outs = []

# passes through each status to create the dict that will turn into the json file
for status in statuses:
    try:
        text = deEmojify(''.join(status.text.splitlines())[ 0 : 255 ])
        stext = text.split("Sold")
        first = stext[0]

        stext = stext[1].split("for")
        second = "Sold " + stext[0]

        stext = stext[1].split(')')
        third = stext[0] + ")"


        try: fourth = stext[1].split(' ')[1]
        except: fourth = stext[1]


        info = {'date':status.created_at.strftime("%m/%d/%Y, %H:%M:%S"), 'one': first, 'two' : second, 'three': third, 'four': fourth}
        outs.append(info)
    except: pass

# creates the json output
print(json.dumps({'items':outs}, indent=2))
