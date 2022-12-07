# import the module
import tweepy
import json
from datetime import datetime, timedelta

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
api = tweepy.API(auth, wait_on_rate_limit=True)

def fetch_dms():
    dms = api.get_direct_messages(count=200)
    now = datetime.now()
    monday = (now - timedelta(days = now.weekday())).day
    ids = {}

    for dm in dms:
        idsv = ids.keys()
        date = datetime.fromtimestamp(int(dm.created_timestamp)/1000)
        if date.day != monday-1:
            sid = dm.message_create["sender_id"]
            rid = dm.message_create["target"]["recipient_id"]
            if sid not in idsv:
                sender = api.get_user(user_id=sid).name
                ids[sid] = sender
            else: sender = ids[sid]
            if rid not in idsv:
                recipient = api.get_user(user_id=rid).name
                ids[rid] = recipient
            else: sender = ids[rid]

            msg = dm.message_create["message_data"]["text"]
            info = {"date": date,"sender_name":sender, "recipient_name": recipient, "message_text":msg}
            outputs.append(info)

outputs = []
fetch_dms()


print(json.dumps({'items':outputs}, indent=2, ensure_ascii=False, default=str))

