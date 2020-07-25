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

reddit = praw.Reddit(client_id='qeEY-gzqmsBETQ', client_secret='5kzPlra-qhr2MRt5aYBKWHxRZFY', user_agent='Telvin Zhong')

submission = reddit.submission(url="https://www.reddit.com/r/worldnews/comments/hwugz3/mike_pompeo_says_free_world_must_change_china_or/")
submission.comments.replace_more(limit = 0)

# NLTK stopwords corpus contains common English words that we remove from our dataset.
common = stopwords.words('english')
print(common)
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
    # with open('text.csv', 'w') as myfile:
    #     wr = csv.writer(myfile, quoting = csv.QUOTE_ALL)
    #     wr.writerow(all_words)



    wordcloud = WordCloud().generate(all_words)

    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    # lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(all_words)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


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