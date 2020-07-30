import praw
import re
import praw
import numpy as np
import pandas as pd
from os import path
from PIL import Image
import csv
import nltk
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.corpus import stopwords
from praw.models import MoreComments
import matplotlib.pyplot as plt

# [bot1]
# client_id='qeEY-gzqmsBETQ'
# client_secret='5kzPlra-qhr2MRt5aYBKWHxRZFY'
# password=12345678
# username=show_me_words
# user_agent=Wordcloudbot

reddit = praw.Reddit(client_id='qeEY-gzqmsBETQ', client_secret='5kzPlra-qhr2MRt5aYBKWHxRZFY', user_agent='Telvin Zhong')
 
subreddit = reddit.subreddit("Askreddit")

# for comment in subreddit.stream.comments():
#     print(comment.body)
#     if re.search("Wordcloud me", comment.body, re.IGNORECASE):
#         print("string found")
#         submission = reddit.submission(url=str(comment.submission.url))
#         submission.comments.replace_more(limit = 0)
#         print(submission)
#         break
        
    
reddit = praw.Reddit(client_id='qeEY-gzqmsBETQ', client_secret='5kzPlra-qhr2MRt5aYBKWHxRZFY', user_agent='Telvin Zhong')

# submission = reddit.submission(url="https://www.reddit.com/r/leagueoflegends/comments/hyfipi/cloud9_vs_team_liquid_lcs_2020_summer_week_7/")
# submission.comments.replace_more(limit = 0)

# NLTK stopwords corpus contains common English words that we remove from our dataset.
common = stopwords.words('english')
print(common)