'''
link_tally.py
a hackish script to figure out how many links may exist between polls and news
'''

__author__ = "Jack Bandy"
__email__ = "jgba225@g.uky.edu"

from bs4 import BeautifulSoup
import numpy as np
import requests
import pickle


def main():
    articles = np.genfromtxt('g_news_articles/g-news-articles-combined.txt', dtype=str)
    raw_polls = np.genfromtxt('poll_list/national_poll_urls.txt', dtype=str,
            delimiter='\n')
    raw_s_polls= np.genfromtxt('poll_list/state_poll_urls.txt', dtype=str,
            delimiter='\n')
    n_polls = [x[:x.find(',')].strip() for x in raw_polls]
    print("{} national polls".format(len(n_polls)))
    s_polls = [x[:x.find(',')].strip() for x in raw_s_polls]
    print("{} state polls".format(len(s_polls)))
    polls = n_polls + s_polls
    print("{} total polls".format(len(polls)))
    np.random.shuffle(polls)

    link_count = 0
    parse_count = 0
    link_dict = {}

    for article in articles:
        try:
            html = requests.get(article).content
            soup = BeautifulSoup(html, 'lxml')
            parse_count += 1
            links = []
            for link in soup.find_all('a'):
                if (link.get('href') in polls 
                        and len(link.get('href').strip()) > 0):
                    #print("MISS: {}".format(link.get('href')))
                    print("HIT: {}".format(link.get('href')))
                    links.append(link.get('href'))
                    link_count +=1
            if len(links) > 0:
                link_dict[article] = links
        except Exception:
            print("problem with {}".format(article))

        print("{} links found after {} articles".format(link_count, parse_count))

    pickle.dump(link_dict, open('link_dict.pkl', 'w'))



if __name__ == "__main__":
    main()
