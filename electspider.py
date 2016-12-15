'''
electspider.py
A spider designed to get urls,
parse their data,
and add edges to our graph if any hits occur
'''

import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from bs4 import BeautifulSoup
import numpy as np
import pickle

def main():
    global articles
    global polls
    global sublinks
    global link_dict
    global poll_link_count
    global total_crawl_count
    global poll_tally
    global prev_articles

    link_dict = {}
    poll_link_count = 0
    total_crawl_count = 0
    d_articles = {}
    articles = []

    raw_polls = np.genfromtxt('poll_list/national_poll_urls.txt',
            dtype=str, delimiter='\n')
    raw_s_polls= np.genfromtxt('poll_list/state_poll_urls.txt',
            dtype=str, delimiter='\n')
    n_polls = [x[:x.find(',')].strip() for x in raw_polls]
    print("{} national polls".format(len(n_polls)))
    s_polls = [x[:x.find(',')].strip() for x in raw_s_polls]
    print("{} state polls".format(len(s_polls)))
    polls = n_polls + s_polls
    print("{} total polls".format(len(polls)))
    poll_tally = dict.fromkeys(polls)
    for l in polls:
        poll_tally[l] = 0

    print('loading articles...')
    prev_articles_r = np.genfromtxt('all_articles.txt',
            dtype=str, delimiter='\n')
    prev_articles = dict.fromkeys(prev_articles_r)
    for a in prev_articles_r:
        prev_articles[a] = 1

    #r_articles = pickle.load(open('pickle_jar/depth1_links.pkl', 'r'))
    r_articles = np.genfromtxt('pickle_jar/depth1_links.txt',
            dtype=str, delimiter='\n')
    print('removing duplicates...')
    for a in r_articles:
        if (not prev_articles.get(a) and not d_articles.get(a)
                and not poll_tally.get(a) and a[:4] =='http'
                and 'facebook' not in a
                and 'twitter' not in a
                and 'google' not in a):
            d_articles[a] = 1
    articles = [ k for k in d_articles.keys()]
    np.random.shuffle(articles)

    
    print("all_articles has {} articles to crawl".format(len(articles)))


    sublinks = []

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(ElectionSpider)
    process.start() # the script will block here until the crawling is finished
    '''

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()
    d = runner.crawl(ElectionSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    '''

    print("{} hits / {} crawled".format(poll_link_count, total_crawl_count))
    a_sublinks = []
    for l in sublinks:
        a_sublinks.append(l.encode('ascii', 'ignore'))
    np.savetxt('depth2_links.txt', a_sublinks, fmt='%s', delimiter='\n')
    pickle.dump(link_dict, open('depth1_link_dict.pkl', 'wb'))
    pickle.dump(poll_tally, open('poll_tally_depth1.pkl', 'wb'))



class ElectionSpider(scrapy.Spider):
    name = 'election'
    DOWNLOAD_HANDLERS = {
        'file': None,
        'http': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler',
        'https': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler',
        's3': None,
        'ftp': None
    }
    DOWNLOAD_DELAY = 0.2
    REDIRECT_MAX_TIMES = 4
    DOWNLOAD_MAXSIZE = 2097152 # no more than 2MB
    USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    DOWNLOAD_TIMEOUT = 16
    CONCURRENT_ITEMS = 4000
    ROBOTSTXT_OBEY = True
    CONCURRENT_REQUESTS_PER_IP = 4
    CONCURRENT_REQUESTS = 32
    REACTOR_THREADPOOL_MAXSIZE = 32

    def start_requests(self):
        global articles
        toreturn = []
        for start_url in articles:
            try:
                toreturn.append(Request(start_url, self.parse))
            except Exception:
                pass

        return toreturn
        '''
        for url in articles:
            yield scrapy.Request(url=url, callback=self.parse)
        '''

    def parse(self, response):
        global articles
        global raw_polls
        global raw_s_polls
        global sublinks
        global link_dict
        global poll_link_count
        global total_crawl_count
        global poll_tally
        global prev_articles

        bod = response.body
        url = response.url
        if url in polls:
            # a redirect eventually led to a poll
            red_poll_link_count += 1
            poll_tally[url] += 1
        try:
            poll_links = []
            soup = BeautifulSoup(bod, 'lxml')
            for link in soup.find_all('a'):
                href = link.get('href')
                if href is not None and len(href) > 0 and not prev_articles.get(href):
                    href = href.strip()
                    if href in polls: # link to poll!
                        poll_link_count += 1
                        poll_links.append(href)
                        poll_tally[href] += 1
                    elif 'http' in href:
                        sublinks.append(href)

            if len(poll_links) > 0 and len(poll_links) < 10:
                link_dict[url] = poll_links

            total_crawl_count += 1
            if (total_crawl_count % 100 == 0):
                print("\nELECTSPIDER crawled {} urls\n".format(total_crawl_count))

        except Exception:
            print("error with {}".format(url))
            





if __name__ == "__main__":
    main()
