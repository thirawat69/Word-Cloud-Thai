import pythainlp
from pythainlp import word_tokenize
from pythainlp.corpus import get_corpus # for getting stopwords

import wordcloud
from wordcloud import WordCloud

import matplotlib.pyplot as plt
import numpy as np
import re

# %matplotlib inline
# %config InlineBackend.figure_format='retina'

def wordcloudThai(all_tweet):


    words = word_tokenize(all_tweet)
    print(words)

    all_words = ' '.join(words).lower().strip()


    # stop word
    stopwords = {'\n'} # set
    print(type(stopwords))
    print(stopwords)

    wordcloud = WordCloud(
    #     font_path='c:/windows/fonts/browalia.ttc',
    #     font_path='C:/Users/thirawat/Desktop/word_cloud_thai/font_path/Fahkwang-Medium.ttf',
    #     font_path='font_path/Kanit-Black.ttf',
        font_path='font_path/Fahkwang-Medium.ttf',
        regexp='[ก-๙]+',

        stopwords=stopwords,
        width=2000, height=1000,

        prefer_horizontal=.9,
        max_words=20, 

    #     colormap='viridis', # default matplotlib colormap
        colormap='tab20c',
    #     colormap='plasma',
        background_color = 'white').generate(all_words)
    plt.figure(figsize = (10, 9))
    # plt.imshow(wordcloud)
    plt.savefig('myfig')
    plt.axis('off')
    plt.tight_layout(pad=0)
    # plt.show()

    return wordcloud