from feed_reader import FeedReader

fr = FeedReader(url='http://feeds.bbci.co.uk/news/rss.xml')

for item in fr.items:
    print(item)

print(fr.feeds)

print(fr.meta)
