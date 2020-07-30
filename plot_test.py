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

data = pd.read_csv(r"text.csv", encoding ="latin-1")
comment_words = ""
# Iterating through the .csv data file 
for i in data: 
    i = str(i) 
    separate = i.split(",")
    for j in range(len(separate)): 
        separate[j] = separate[j].lower() 
      
    comment_words += " ".join(separate)+" "

# Creating the Word Cloud
final_wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                # stopwords = stop_words, 
                min_font_size = 10).generate(comment_words)

# Displaying the WordCloud                    
plt.figure(figsize = (10, 10), facecolor = None) 
plt.imshow(final_wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show()
plt.savefig('foo.png', bbox_inches = 'tight')