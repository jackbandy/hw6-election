import hashlib  #md5 hashing
import mysql.connector  #mysql connector
from urlparse import urlparse   # url parser
import re
import robotparser  # check robots.txt
import urllib2  # connect url
from bs4 import BeautifulSoup   # parse html
import datetime
import requests #download pdf file
from collections import Counter # for count word frequency
from nltk.stem.porter import *  # for word stemming
import ssl  # for connection error
gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)


def print_url_list():
    query = ("SELECT * FROM CS685_HW5.url_list")
    cursor.execute(query)
    for (md5, url, crawl_status, under_engr) in cursor:
    	print("{},{},{},{}".format(md5, url, crawl_status, under_engr))

# insert a row to url_list table
def insert_url_list(url, crawl_status):
    url_md5 = hash_url(url) # hash value of url

    # under subdomain ?
    if check_subdomain(url) == 0:
        under_engr = False
    else:
        under_engr = True

    query = """INSERT INTO `CS685_HW5`.`url_list` (`md5`, `url`, `crawl_status`, \
    `under_engr`) VALUES (%s,%s,%s,%s)"""

    cursor.execute(query,(url_md5, url, crawl_status, under_engr))
    conn.commit()

# insert a rwo to url_queue table
def insert_url_queue(url):
    url_md5 = hash_url(url) # hash value of url
    cursor.execute("SELECT MAX(qid) from CS685_HW5.url_queue")
    curMax_qid = cursor.fetchone()
    if curMax_qid[0] is None:
        qid=1
    else:
        qid = curMax_qid[0]+1		# get next qid

    query = """INSERT INTO `CS685_HW5`.`url_queue` (`qid`,`url_md5`) VALUES (%s, %s)"""
    cursor.execute(query,(qid, url_md5))
    conn.commit()

# isnert a row to html_content table
def insert_html_content(url, content):
    url_md5 = hash_url(url)
    query = """INSERT INTO `CS685_HW5`.`html_content` (`url_md5`,`content`) VALUES (%s, %s)"""
    cursor.execute(query,(url_md5, content))
    conn.commit()

# insert a row to pdf_file table
def insert_pdf_list(url):
    url_md5 = hash_url(url) # hash value of url

    query = """INSERT INTO `CS685_HW5`.`pdf_list` (`url_md5`,`url`) VALUES (%s, %s)"""
    cursor.execute(query,(url_md5, url))
    conn.commit()

# update url as crawled in url_list table
def set_url_crawled(url):
    url_md5=hash_url(url)
    query = ("UPDATE `CS685_HW5`.`url_list` SET `crawl_status`=1 WHERE `md5`='%s'" %(url_md5))
    cursor.execute(query)
    conn.commit()

# get next url from queue
def get_next_url():
    # get the md5 for first url in url_queue
    cursor.execute("""SELECT * FROM CS685_HW5.url_queue LIMIT 1""")
    row = cursor.fetchone()
    url_md5 = row[1]

    # retrive the url from url_list
    cursor.execute("SELECT * FROM `CS685_HW5`.`url_list` WHERE `md5`='%s'" % (url_md5))
    row = cursor.fetchone()
    url = row[1]

    # remove the top url from table
    cursor.execute("DELETE FROM CS685_HW5.url_queue WHERE url_md5 = '%s'" % (url_md5))
    conn.commit()
    return url

# hashing url, return md5 of given url
def hash_url(url):
    m=hashlib.md5()
    m.update(url)
    url_md5=m.hexdigest()
    return url_md5

# used to verify whether the url is under engr subdomain
def check_subdomain(url):
    under_engr = 1
    u = urlparse(url)
    netloc = u.netloc
    if netloc.find('engr')==-1:
        under_engr = 0
    return under_engr

# check url_crawl_status
def check_url_crawl_status(url):
    url_md5=hash_url(url)
    cursor.execute("SELECT * FROM `CS685_HW5`.`url_list` WHERE `md5`='%s'" % (url_md5))
    row = cursor.fetchone()
    status = row[2]

# check if link is in url_list
def check_url_existed(url):
    url_md5=hash_url(url)
    cursor.execute("SELECT * FROM `CS685_HW5`.`url_list` WHERE `md5`='%s'" % (url_md5))
    row = cursor.fetchone()
    if row is None:
        return 0
    else:
        return 1

# check if html content is saved
def check_html_content_saved(url):
    url_md5=hash_url(url)
    cursor.execute("SELECT * FROM `CS685_HW5`.`html_content` WHERE `url_md5`='%s'" % (url_md5))
    row = cursor.fetchone()
    saved=1
    if row is not None:
        saved = 0
    return saved

# search content in table
def search_in_table(table_name, column_name, key):
    cursor.execute('SELECT * FROM CS685_HW5.%s WHERE %s="%s"' %(table_name, column_name, key))
    row = cursor.fetchone()
    return row

# update dictionary table
def update_dict_table(key, count):
    query = ("UPDATE `CS685_HW5`.`dictionary` SET `count`=%s WHERE `word`='%s'" %(count, key))
    cursor.execute(query)
    conn.commit()

# insert a new row in dictionary table
def insert_disc_table(key, count):
    query = """INSERT INTO `CS685_HW5`.`dictionary` (`word`,`count`) VALUES (%s, %s)"""
    cursor.execute(query,(key, count))
    conn.commit()

# count number of rows in a table
def count_table(table):
    query = "SELECT COUNT(*) FROM CS685_HW5."+table
    cursor.execute(query)
    row = cursor.fetchone()
    row = row[0]
    return row

# parse url
def parse_url(url):
    u = urlparse(url)
    scheme = u.scheme
    netloc = u.netloc
    path = u.path
    newURL = scheme + '://' + netloc + path
    newURL = newURL.lower()
    return newURL

# count words in string
def word_count_str(input_string):
    text = input_string.split()
    counters = Counter(text)
    return counters

# word stemmer
def stem_word(word):
    stemmer = PorterStemmer()
    word = stemmer.stem(word)
    return word

# connect to database
conn = mysql.connector.connect(
	user='root',
	password='w13085000',
	host='127.0.0.1',
	database='CS685_HW5')
cursor = conn.cursor()


# read robots.txt
robotsFile = "http://www.engr.uky.edu/robots.txt"
#robotsFile = "http://www.uky.edu/robots.txt"
x = robotparser.RobotFileParser()
x.set_url(robotsFile)
x.read()


# while queue is not empty
while count_table('url_queue')>0:
#for i in range(1,2):
    cur_url = get_next_url()
    if not cur_url:
        continue
    if check_url_crawl_status(cur_url) == 0:
        print ("==== url: %s has crawled, continue ====" %(cur_url))
        continue

    # print current time and current url
    print ("=====%s %s=====" %(datetime.datetime.now().date(), datetime.datetime.now().time()))
    print ("Get -%s- from queue" %(cur_url))

    # catch if url has unicode
    try:
        if x.can_fetch("*", cur_url):
            pass
    except Exception as e:
            continue

    if x.can_fetch("*", cur_url):
        # connect server
        print("     connecting to url...")

        #if content_type is pdf, download
        ext_name = cur_url[-4:]
        if ext_name == '.pdf':
            print("     downloading .pdf file...")
            md5 = hash_url(cur_url)
            try:
                response = requests.get(cur_url)
            except Exception as e:
                continue
            with open('./pdf/'+md5+'.pdf', 'wb') as f:
                f.write(response.content)
            # insert a row in pdf table
            insert_pdf_list(cur_url)
            # update url_crawl_status
            set_url_crawled(cur_url)
            continue

        try:
            response = urllib2.urlopen(cur_url, timeout=4, context=gcontext)
        except Exception as e:
            continue

        # check url content type
        print("     check url content type...")
        content_type = response.headers.getheader('Content-Type')

        if content_type is None:
            continue

        # if the url content_type is not html, skip
        if "text/html" not in  content_type:
            continue

        # fetch the url
        try:
            html = response.read()
        except Exception as e:
            continue

        soup = BeautifulSoup(html, "lxml") #web data payload

#=========================================
#   1. edit download web context
        # insert html content in html_content table
        print("     saving html content...")
        try:
            if check_html_content_saved(cur_url)==1:
                # kill all script and style elements
                for script in soup(["script", "style"]):
                    script.extract()    # rip it out
                # get text
                text = soup.get_text()
                # break into lines and remove leading and trailing space on each
                lines = (line.strip() for line in text.splitlines())
                # break multi-headlines into a line each
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # drop blank lines
                text = '\n'.join(chunk for chunk in chunks if chunk)

                # insert a row to html_content table
                insert_html_content(cur_url, text)
                # update url_crawl_status
                set_url_crawled(cur_url)
        except Exception as e:
            pass

#==========================================
# 2. add word count
        # word stemming

        counters = word_count_str(text)
        for word in list(counters):
            # check if word is in the dictionary table
            table_name = 'dictionary'
            column_name = 'word'
            key = word  # the word
            count = counters[word]  # count of the word

            # remove ' in text
            key = key.replace("'", "")

            #stemmed word
            stemmed_word = stem_word(key)
            # if the stemmed_word too long, skip
            if len(stemmed_word)>32:
                continue

            # existed_row == None, key word is not existing
            try:
                existed_row = search_in_table(table_name, column_name, stemmed_word)
            except Exception as e:
                continue

            # if word in dictionary table, update word count
            if existed_row is not None:
                current_count = existed_row[1]
                count = current_count+counters[word]
                #update table
                try:
                    update_dict_table(stemmed_word, count)
                except Exception as e:
                    continue

            # if word is not in dictionary table
            else:
                insert_disc_table(stemmed_word, count)



        # fetch urls, add into url_list and queue
        links = soup.find_all('a')  # all links in cur page
        print ("     extracting urls...")

        for tag in links:
            link = tag.get('href',None)
            print("          - %s" %(link))
            if link is not None:
                link = parse_url(link)
                # if link is exsiting in url_list, skip
                if check_url_existed(link)==1:
                    continue

                # if url under subdomain
                if check_subdomain(link)==1:
                    crawl_status = False
                    insert_url_list(link, crawl_status)
                    insert_url_queue(link)
                # if url not under subdomain
                else:
                    crawl_status = False
                    insert_url_list(link, crawl_status)


'''

url = 'http://www.engr.uky.edu/'
#url = 'https://www.engr.uky.edu/paducah/files/2016/06/final-exam-schedule-2016.pdf'
#url = 'http://www.uky.edu/registrar/Major-Sheets/MS1213/eng/ee.pdf'

crawl_status = False


insert_url_list(url, crawl_status)
insert_url_queue(url)
'''
