# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, JsonResponse

from textblob import TextBlob #for sentiment analysis
import tweepy #for fetching tweets
import csv
import json
import os
import traceback
import time
import nltk

#twitter keys
consumer_key = "e4dhqF2LMoj9miJHf6AjZZZSA"
consumer_secret = "bbFO5TOOYMLedm709QcYHCAGRIxEZALvOLJUO18TSKJu77qhlG"
access_token = "1001347904575946752-ymlT6aaJ4PztVhFQ1f5Vf5NW4mZrRr"
access_token_secret = "lkVXqo7Osivgnu1na6z5WlJWm85lx97ydy7hTiF2goBuV"

#set up twitter lib
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# Helper functions
def getSentimentScore(arr):
	sentiment_score = 0

	for a in arr:
		blob = TextBlob(a)

		for sentence in blob.sentences:
			sentiment_score = sentiment_score + sentence.sentiment.polarity

	return sentiment_score


#Download Tweets from username account
def get_tweets(username):
	try:
		result = [] 

		# if tweets in json file , send them
		all_tweets = readJSON('AllTweets.json')
		for userObj in all_tweets:
			if(userObj['handle'] == username):
				result = userObj['tweets']
				return result

		# else fetch them from twitter
		for status in tweepy.Cursor(api.user_timeline,screen_name=username, language = ["en"]).items(200):
			result.append(status.text)
		return result
	except:
		return []


def readJSON(file):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	with open(BASE_DIR+'/webapp/static/js/'+file) as json_data:
		result = json.load(json_data)
		return result


# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def interests(request):
    return render(request, 'interests.html', {})

def mp(request):
    return render(request, 'mp.html', {})


def get_mp_rating(request):
	if(request.method == 'GET'):
		state = request.GET.get('state', None)
		constituency = request.GET.get('constituency', None)
		categories_string = request.GET.get('categories', None)

		categories_string = categories_string.replace("[","")
		categories_string = categories_string.replace("]","")
		categories_arr = categories_string.split(',')

		categories = []

		for cat in categories_arr:
			tmp = cat.replace("'","")
			tmp1 = tmp.replace('"',"")

			categories.append(tmp1)

		nltk.data.path.append("/home/ubuntu/nltk_data")



		if(not state or not constituency or not categories or categories==[]):
			return JsonResponse({'error':"not enough info"})

		mp_info = readJSON("AllMPs.json")

		try:
			tw_handle = (mp_info[constituency][4])
			if (tw_handle == ""):
				print ('no handle')
				return JsonResponse({'error':"not enough info"})

			if(tw_handle[0] == '@'):
				tw_handle = tw_handle[1:]

			all_tweets = get_tweets(tw_handle)
			score_list = []

			for category in categories:
				tw = []
				for tweet in all_tweets:
					if (category in tweet):
						tw.append(tweet)
					if (category.lower() in tweet):
						tw.append(tweet)
				
				score = getSentimentScore(tw)
				score_list.append({'category':category,'score':score})

			result = {'state': (mp_info[constituency][0]),'constituency':(mp_info[constituency][1]),'mp_name':(mp_info[constituency][2]),'image':(mp_info[constituency][3]),'verified':(mp_info[constituency][5]),'score':score_list}
			return JsonResponse(result)

		except Exception:
			print(traceback.format_exc())
			return JsonResponse({'error':"not enough info"})






def get_all_users_tweets():
	input = readJSON('AllMPs.json')
	tws_list = []
	# for each key in the json file

	for i in input:
		tw_handle = (input[i][4])
		if not tw_handle == "" and not tw_handle == " ":
			# remove the @ from the twitter handle
			try:
				if(tw_handle[0] == '@'):
					tw_handle = tw_handle[1:]
				print('getting tweets of '+ tw_handle)

				tweets = get_tweets(tw_handle)
				tws_list.append({'handle':tw_handle, 'tweets':tweets})

				time.sleep(12)
			except:
				print(tw_handle)
				pass

	#now write tws_list to json file
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	with open(BASE_DIR+'/webapp/static/js/AllTweets.json', 'w') as file:
		json.dump(tws_list, file)
			


