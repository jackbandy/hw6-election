'''
electspider.py
A spider designed to get urls,
parse their data,
and add edges to our graph if any hits occur
'''

import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup

def main():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(ElectionSpider)
    process.start() # the script will block here until the crawling is finished



class ElectionSpider(scrapy.Spider):
    name = 'election'
    def start_requests(self):
        urls = [
            'http://www.marketwatch.com/story/polls-show-clinton-widening-lead-over-trump-and-no-its-not-a-conspiracy-2016-10-19' 
                ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        bod = response.body
        soup = BeautifulSoup(bod, 'lxml')
        links = []
        for link in soup.find_all('a'):
            print('LINK: {}'.format(link.get('href')))





if __name__ == "__main__":
    main()
