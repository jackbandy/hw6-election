# hw6-election
Final project for cs685, aimed at organizing and ranking polls from the 2016 presidential election.

###Directory
NewsLookUp-article-url/
  - Tools for scraping NewsLookUp 
  - Results from NewsLookUp
fark-articles/
  - Tools for scraping fark aggregator 
  - Results from fark
g-news-articles/
  - Tools for scraping google news aggregator
  - Results from google news
all-articles.py
  - Used to combine results from all aggregation efforts


fte-poll-list/
  - Tools for scraping FiveThirtyEight polls
  - Results
rcp-poll-list/
  - Tools for scraping RealClearPolitics polls
  - Results
poll-list/
  - Combined results

PageRank/
  - The code we used for ranking polls

electspider.py
  - The scrapy-based spider for our large-scale crawl
feature-tally.py
  - Used to generate output data

data/
  - All output data

### TODO
(In order of priority)

  - Create test parser, run on subset of current article links, create graph (Jack)
  - Implement ranking scheme and test on small graph (Shaila)
  - Generate more news article links (everyone)
  - Implement Scrapy spider for crawling articles
  - Optimize ranking scheme

