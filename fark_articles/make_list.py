'''
make_list.py
collect all outlinks from fark archives,
given a list of archive links
'''

import numpy as np
import requests
from bs4 import BeautifulSoup
links = np.genfromtxt('archive_links.txt', dtype=np.str)
articles = np.empty((0), dtype=np.str)
for link in links:
    print("requesting {}".format(link))
    page = requests.get(link).content
    soup = BeautifulSoup(page, 'lxml')

    for outlink in soup.findAll('a', attrs={'class':'outbound_link'}):
        print("outlink: {}".format(outlink['href']))
        articles = np.append(articles, outlink['href'])

np.savetxt('articles.txt', articles, delimiter='\n', fmt='%s')


    
