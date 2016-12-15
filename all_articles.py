'''
all_articles.py
create all_articles list
'''
import numpy as np

all_articles = {}

print("adding g_articles")
g_articles = np.genfromtxt('g_news_articles/g-news-articles-combined.txt',
        dtype=str)
for article in g_articles:
    if not all_articles.get(article): all_articles[article] = 1

print("adding fark_articles")
fark_articles = np.genfromtxt('fark_articles/articles.txt',
        dtype=str)
for article in fark_articles:
    if not all_articles.get(article): all_articles[article] = 1

print("adding nlu_articles")
nlu_articles = np.genfromtxt('NewsLookUp_article_url/nlu_article_url.txt',
        dtype=str)
for article in nlu_articles:
    if not all_articles.get(article): all_articles[article] = 1

'''
print("adding arch_articles")
arch_articles = np.genfromtxt('urls_from_archive.txt',
        dtype=str, delimiter='\n')
for article in arch_articles:
    if not all_articles.get(article): all_articles[article] = 1
'''

print("all_articles has {} articles".format(len(all_articles.keys())))
print("saving all_articles.txt")
np.savetxt('all_articles.txt', all_articles.keys(), fmt='%s', delimiter='\n')

