from urlparse import urlparse
import urllib2
from bs4 import BeautifulSoup
import mmap


#html ='''
#    <div id="results"><a class="title" href="http://www.breitbart.com/big-government/2016/11/16/5-most-absurd-ways-the-left-has-responded-to-the-2016-election/">5 Most Absurd Ways the Left Has Responded to the 2016 Election</a></div>
#'''
#soup = BeautifulSoup(html)

#url = 'http://www.newslookup.com/politics/?q=2016+election&dp=&mt=-1&s=&groupby=no&cat=-1&from=&fmt=&tp=720'

dashboard = "dashboard.txt"
url_file = 'nlu_article_url.txt'
domain_file = 'nlu_article_domain.txt'

keywords = ['2016+election', '2016+Trump', '2016+Clinton', '2016+poll', 'state+poll', \
    'Trump+leads', 'Clinton+leads', 'Trump+gains', 'Clinton+gains', 'tied', 'electoral+college', \
    'election+demographics', 'battleground+states', 'head-to-head']

#total crawled url number
num_url=0
for j in range (5, len(keywords)):
    for i in range (1,1001):

        print ("  updating Dashboarding")
        print ("\tcurrent keyword: %s\n\tcurrent page: %s\n\ttotal number of url crawled: %s" %(keywords[j], i, num_url))
        with open(dashboard, 'w') as ds_file:
            ds_file.write("current keyword: %s\ncurrent page: %s\ntotal number of url crawled: %s" %(keywords[j], i, num_url))

        url = 'http://www.newslookup.com/politics/page'+str(i)+'?q='+keywords[j]+'&dp=5&mt=-1&ps=10&s=&cat=-1&fmt=&groupby=no&dp=5&tp=720ttt'

        req = urllib2.Request(url)
        response = urllib2.urlopen(req, timeout=4)
        html = response.read()
        soup = BeautifulSoup(html, "lxml")

        # find all 'a' tag
        for tag in soup.find_all('a'):
            # if a 'a' tag doesn't have 'class' attribute, skip
            if 'class' not in tag.attrs:
                continue

            # if 'class' = ['title'], extract the url
            if tag.attrs['class'] == ['title']:

                #poll_name = tag.text
                #link = tag.find('a')
                url = tag.get('href',None)

                # if url is not exist in text file, append it
                with open(url_file, 'r') as fr:
                    s = mmap.mmap(fr.fileno(), 0, access=mmap.ACCESS_READ)
                    if s.find(url) == -1:
                        # append to text file
                        with open(url_file, "a") as fw:
                            fw.write(url+' ,'+'\n')

                # url domain
                url_domain = urlparse(url).scheme+'://'+urlparse(url).netloc
                # if url domain is not exist, append it
                with open(domain_file, 'r') as fr:
                    s = mmap.mmap(fr.fileno(), 0, access=mmap.ACCESS_READ)
                    if s.find(url_domain) == -1:
                        # append to text file
                        with open(domain_file, "a") as fw:
                            fw.write(url_domain+'\n')
                # update total crawled url number
                num_url = num_url+1
