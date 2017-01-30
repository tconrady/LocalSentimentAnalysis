from TwitterAPI import TwitterAPI, TwitterOAuth
import pandas as pd

LIMIT = 100

creds = TwitterOAuth.read_file()
api = TwitterAPI(creds.consumer_key, 
                 creds.consumer_secret,
                 creds.access_token_key,
                 creds.access_token_secret,
                 auth_type = "oAuth1")

with open('LocationData.csv','r') as csvFile:
    locations = pd.read_csv(csvFile, 
                            index_col='City', 
                            dtype={'Latitude':float, 'Longitude':float})

allTweets = []
for city in locations.index:
    print("Next Stop: {}".format(city))
    tweets = []
    (lo, la) = locations.loc[city,:]
    geobox = "{0:.2f},{1:.2f},{2:.2f},{3:.2f}".format(la-1,lo-1,la+1,lo+1)
    for item in api.request('statuses/filter', 
                             {'locations': geobox}).get_iterator():
        if len(tweets) >= LIMIT:
            break
        if 'text' in item:
            tweets.append(item['text'])
        elif 'limit' in item:
            print '{} tweets missed'.format(item['limit']['track'])
        elif 'disconnected' in item:
            print 'Disconnected: {}'.format(item['disconnected']['reason'])
    allTweets.append((city,tweets))
    
df = pd.pandas(allTweets)
with open('TwitterData.csv','w') as outputFile:
    df.to_csv(outputFile)
