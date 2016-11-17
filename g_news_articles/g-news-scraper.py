from bs4 import BeautifulSoup # pip install beautifulsoup4
import requests # pip install requests
import sys

user_agent = "Mozilla/5.0 (Windows NT x.y; WOW64; rv:10.0) Gecko/20100101 Firefox/10.0"
urls = []
results = []

if len(sys.argv) != 2:
	print("Usage: <list-of-urls.txt>")
	sys.exit()

with open(sys.argv[1]) as infile:
	for line in infile:
		urls.append(line.strip('\n'))

for url in urls:
	page = requests.get(url, headers={'User-Agent': user_agent, 'Upgrade-Insecure-Requests': '1'}, allow_redirects=True).content
	soup = BeautifulSoup(page, "lxml")

	for anc_pri in soup.findAll('a', attrs={'class':'l _HId'}):
		results.append(anc_pri['href'])

	for anc_sec in soup.findAll('a', attrs={'class':'_sQb'}):
		results.append(anc_sec['href'])

	with open('news-articles.txt','w') as outfile:
		for link in results:
			outfile.write(link + '\n')
