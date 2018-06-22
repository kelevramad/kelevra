import twitter
import time

api = twitter.Api(consumer_key='consumer_key',
                  consumer_secret='consumer_secret',
                  access_token_key='access_token_key',
                  access_token_secret='access_token_secret')

results = api.GetFollowers(user_id=None, screen_name='OdeCarvalho', cursor=None, count=None, total_count=None, skip_status=False, include_user_entities=True)
print results

#results = api.GetSearch(term=None, raw_query="q=%23bolsonaro&count=1&since=2018-03-31&until=2018-04-01", geocode=None, since_id=None, max_id=None, until=None, since=None, count=100, lang=None, locale=None, result_type='mixed', include_entities=None)

#for num, ret in enumerate(results, 1):
#	print "%s " %ret.in_reply_to_screen_name
#	print "%s " %ret.user.screen_name


#user = api.CreateFriendship(user_id=None, screen_name='flaviogordon', follow=True)
#print user


#users = api.GetFollowers()
#print([u for u in users])

#results = api.GetRetweetsOfMe()
#print results

#results = api.GetSearch(term=None, raw_query="q=serie indica&count=100&since=2018-03-30&until=2018-04-01", geocode=None, since_id=None, max_id=None, until=None, since=None, count=100, lang=None, locale=None, result_type='mixed', include_entities=None)

#for num, ret in enumerate(results, 1):
#	print "%s - %s" %(num, ret.text)

#---------------------------------------------------------------------------------------------------

#Post Random Message

#message = ["is simply dummy text of the printing and typesetting industry. https://www.lipsum.com", "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s https://www.lipsum.com", "when an unknown printer took a galley of type and scrambled it to make a type specimen book. https://www.lipsum.com", "It has survived not only five centuries, but also the leap into electronic typesetting https://www.lipsum.com", "remaining essentially unchanged. It was popularised in the 1960s https://www.lipsum.com"]

#for msg in message:
#	status = api.PostUpdate(msg)
#	print status, '\n'

#---------------------------------------------------------------------------------------------------

# Verify Credentials

#print(api.VerifyCredentials())

#---------------------------------------------------------------------------------------------------

#Get Search

#results = api.GetSearch(raw_query="q=filme%20online%20indica&result_type=recent&since=2014-01-01&count=200")
#print results

#---------------------------------------------------------------------------------------------------

#Direct Message

#twitter_handle = '_mentira_'
#t = time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime())
#msg = "Alert !! Motion detected at " + t
# Send Direct Message to official Twitter handle
#send_msg = api.PostDirectMessage(msg, user_id=None, screen_name=twitter_handle)

#---------------------------------------------------------------------------------------------------

#Get Status Tweet

#tweet = api.GetStatus(979944640001519617)
#print(tweet)

#---------------------------------------------------------------------------------------------------

#Replying Tweet By Id

#status = api.PostUpdate('sample...', None, None, None, 979944640001519617, auto_populate_reply_metadata=True)

#---------------------------------------------------------------------------------------------------

#Get Trends

#trends_str = ""
#trends_idx = 0
#trends = api.GetTrendsWoeid(23424768)
#print trends

#for t in trends:
#	if t.name[:1] == "#" and trends_idx < 5:
#	        trends_str += t.name + " "
#		trends_idx += 1

#Post Timeline
#status = api.PostUpdate('COB enxuga premiacao de melhores do ano ' + "\n\r" + trends_str + ' https://olharolimpico.blogosfera.uol.com.br/2018/03/28/em-novo-momento-financeiro-cob-enxuga-premiacao-de-melhores-do-ano')

#---------------------------------------------------------------------------------------------------

