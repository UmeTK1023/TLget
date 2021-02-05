import json
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み
from config import CONFIG
import tweepy
import time
import datetime as dt
import urllib.error
import urllib.request
import re
import sys, calendar
import os
#import update_tweetinfo_csv

CONSUMER_KEY = CONFIG["CONSUMER_KEY"]
CONSUMER_SECRET = CONFIG["CONSUMER_SECRET"]
ACCESS_TOKEN = CONFIG["ACCESS_TOKEN"]
ACCESS_SECRET = CONFIG["ACCESS_SECRET"]


dt_now =dt.datetime.now()
yyyymmdd=dt_now.strftime('%Y%m%d')
directory_name=u'自動生成_'+yyyymmdd
current_directory= os.path.dirname(os.path.abspath(__file__))
create_directory = current_directory + '\\' + directory_name
if(not (os.path.exists(create_directory))):
    os.mkdir(create_directory)
FOLDER_PASS = create_directory+'/'


if not os.path.exists('json'):
   os.mkdir('json')

# 認証
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

path = './json'+'/'+directory_name+'.json'


f = open(path, 'a')


def download_file(url, file_name):
   urllib.request.urlretrieve(url, FOLDER_PASS + file_name)

key_account = input('Enter account name:')
count_no = int(input('Set search count:'))
search_results = tweepy.Cursor(api.user_timeline, screen_name=key_account).items(count_no)


for result in search_results:
   

    if hasattr(result, 'extended_entities'): #resultが'extended_entities'属性を持っているか判定
        ex_media = result.extended_entities['media']
        tweet_id = result.id
        print('tweetId : ', result.id)               # tweetのID
        print('tweetUser : ', result.user.screen_name)  # ユーザー名
        print('tweetDate : ', result.created_at)      # 呟いた日時
        print(result.text)                  # tweet内容
        print('favo : ', result.favorite_count)  # tweetのいいね数
        print('retw : ', result.retweet_count)  # tweetのRT数
        print('='*80) # =を80個表示(区切り線)
        
        if 'video_info' in ex_media[0]:
            ex_media_video_variants = ex_media[0]['video_info']['variants']
            media_name = '%s-%s.mp4' % (key_account, tweet_id)
            if 'animated_gif' == ex_media[0]['type']:
                #GIFファイル
                gif_url = ex_media_video_variants[0]['url']
                download_file(gif_url, media_name)
                
            else:
                #動画ファイル
                bitrate_array = []
                for movie in ex_media_video_variants:
                    bitrate_array.append(movie.get('bitrate',0))
                max_index = bitrate_array.index(max(bitrate_array))
                movie_url = ex_media_video_variants[max_index]['url']
                download_file(movie_url, media_name)
        else:
            #画像ファイル
            for image in ex_media:
                image_url = image['media_url']
                image_name = image_url.split("/")[len(image_url.split("/"))-1]
                download_file(image_url + ':orig', image_name)

f.write(str(result.id))
f.write(image_url) 
f.close() 
print('終了')