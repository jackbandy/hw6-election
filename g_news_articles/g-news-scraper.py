from bs4 import BeautifulSoup # pip install beautifulsoup4
import requests # pip install requests
import sys

user_agent = "Mozilla/5.0 (Windows NT x.y; WOW64; rv:10.0) Gecko/20100101 Firefox/10.0"
urls = []
results = set()

if len(sys.argv) != 2:
	print("Usage: <list-of-urls.txt>")
	sys.exit()

with open(sys.argv[1],'r') as infile:
	for line in infile:
		urls.append(line.strip('\n'))

for url in urls:
	page = requests.get(url, headers={'User-Agent': user_agent, 'Upgrade-Insecure-Requests': '1'}, allow_redirects=True).content
	soup = BeautifulSoup(page, "lxml")

	for anc_primary in soup.findAll('a', attrs={'class':'l _HId'}):
		results.add(anc_primary['href'])

	for anc_secondary in soup.findAll('a', attrs={'class':'_sQb'}):
		results.add(anc_secondary['href'])

results = list(results)
with open('news-articles1.txt','w') as outfile:
	for link in results:
		outfile.write(link + '\n')
