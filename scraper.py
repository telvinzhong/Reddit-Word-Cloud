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

reddit = praw.Reddit(client_id='qeEY-gzqmsBETQ', client_secret='5kzPlra-qhr2MRt5aYBKWHxRZFY', user_agent='Telvin Zhong')

submission = reddit.submission(url="https://www.reddit.com/r/leagueoflegends/comments/hyfipi/cloud9_vs_team_liquid_lcs_2020_summer_week_7/")
submission.comments.replace_more(limit = 0)

# NLTK stopwords corpus contains common English words that we remove from our dataset.
common = stopwords.words('english')
# print(common)
all_words = []
word_count = 0
banned = ["\n", ".", "'", ")", "(", "*", "?", "!", "’", "[", "]"]

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
    comment_words = ""

    # Iterating through the .csv data file. 
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
    final_wordcloud.to_file(path.join(d, "foo.png"))

    # Displaying the WordCloud.                        
    plt.figure(figsize = (10, 10), facecolor = None) 
    plt.imshow(final_wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    
    plt.show()
    # plt.savefig('foo.png')
    # , bbox_inches = 'tight'


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