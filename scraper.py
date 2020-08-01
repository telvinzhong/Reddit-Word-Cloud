import praw
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from os import path
from PIL import Image
import csv
import re
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from praw.models import MoreComments
import urllib.request
import base64
import json


################################################################    Wordcloud Setup    ################################################################

'''
# NLTK stopwords corpus contains common English words that we remove from our dataset. I've imported it ahead of time to reduce overhead.
import nltk
common = stopwords.words('english')
'''

common = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself',
'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their',
'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up',
'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 
'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn',
"didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't",
'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

banned = ["\n", ".", "'", ")", "(", "*", "?", "!", "’", "[", "]"] # Removing undesired characters from strings while cleaning.

all_words = []
word_count = 0

################################################################    Praw Setup    ################################################################


reddit = praw.Reddit(client_id='qeEY-gzqmsBETQ', client_secret='5kzPlra-qhr2MRt5aYBKWHxRZFY', user_agent='Telvin Zhong')
 
subreddit = reddit.subreddit("AskReddit")

for comment in subreddit.stream.comments():
    # print(comment.body)
    if re.search("!Wordcloud", comment.body, re.IGNORECASE):
        print("string found")
        submission = reddit.submission(url=str(comment.submission.url))
        submission.comments.replace_more(limit = 0)
        print(submission)
        break
        
    

################################################################    Main Methods    ################################################################

def clean(word):
    # Helper function to ensure alphanumeric, lowercase inputs. 
    res = []
    for i in word:
        # Remove items like \n and punctuation from the dataset.
        if i in banned:
            continue
        elif i.isalnum:
            res.append(i.lower())
    return "".join(res)

# Assumes that the local foo.png has already been updated.
def upload():
    f = open("foo.png", "rb") # open our image file as read only in binary mode
    image_data = f.read()              # read in our image file
    b64_image = base64.standard_b64encode(image_data)

    client_id = "5f4ec90a7daf0da" # put your client ID here
    headers = {'Authorization': 'Client-ID ' + client_id}

    data = {'image': b64_image, 'title': 'test'} # create a dictionary.

    request = urllib.request.Request(url="https://api.imgur.com/3/upload.json", data=urllib.parse.urlencode(data).encode('utf-8'),headers=headers)
    response = urllib.request.urlopen(request).read()

    parse = json.loads(response)
    print(parse['data']['link'])

def main():
    for comment in submission.comments.list():
        # Split comments by spaces into words and clean/append words.
        com = str(comment.body).split(" ")
        for word in com:
            word = clean(word)
            if len(word) >= 3 and word not in common:
                all_words.append(word)

    # Add cleaned words to text.csv.
    with open('text.csv', 'w') as myfile:
        wr = csv.writer(myfile, quoting = csv.QUOTE_ALL)
        wr.writerow(all_words)

    data = pd.read_csv(r"text.csv", encoding ="latin-1")



    # Iterating through the .csv data file. 
    comment_words = ""
    for i in data: 
        i = str(i) 
        separate = i.split(",")
        for j in range(len(separate)): 
            separate[j] = separate[j].lower() 
        
        comment_words += " ".join(separate)+" "

    # Creating the Word Cloud.
    final_wordcloud = WordCloud(width = 800, height = 800, 
                    background_color ='white', 
                    # Second layer of stopwords for quality control.
                    # stopwords = stop_words, 
                    min_font_size = 10).generate(comment_words)
    d = path.dirname(__file__)
    # Save wordcloud to local file (Not sure how this will work online).
    final_wordcloud.to_file(path.join(d, "foo.png"))

    # Displaying the WordCloud.                        
    plt.figure(figsize = (10, 10), facecolor = None) 
    plt.imshow(final_wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    
    plt.show()
    
    upload()


main()

#--------------------------------------------- ALTERNATIVE ---------------------------------------------------


# if isinstance(top_level_comment, MoreComments):      Another way to skip more comments

# dic = {}
# for comment in submission.comments.list():
#     com = str(comment.body).split(" ")
#     for word in com:
#         word = clean(word)
#         if len(word) >= 4 and word not in common:
#             dic[word] = dic.get(word, 0) + 1