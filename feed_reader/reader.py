import requests
import xml.etree.ElementTree as ET
from .exceptions import HTTPResponseError


class FeedReader(object):
    _url = ''
    _feeds = {
        'meta': {},
        'items': [],
    }

    def __init__(self, url):
        self._url = url

        self._load_items()

    def __getattr__(self, attr):
        try:
            return self._feeds[attr]
        except KeyError:
            return AttributeError(f'Object has no attribute called {attr}')

    @property
    def items(self):
        return self._feeds['items']

    @property
    def feeds(self):
        return self._feeds

    @property
    def meta(self):
        return self._feeds['meta']

    def _load_items(self):
        feeds_page = self._fetch_feeds_page()
        return self._parse_feeds(feeds_page)

    def _fetch_feeds_page(self):
        # It is not necessary to put user agent in header
            # but let server feel this request is comming from known browser (Chrome here)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

        # Requesting for the feeds
        response = requests.get(self._url, headers=headers)

        if response.status_code != 200:
            raise HTTPResponseError(
                f'RSS Feed isn\'t accessible, got http response code {response.status_code}')

        return response.content

    def _parse_feeds(self, page):

        # Let instantiate the xml parser
        selector = ET.fromstring(page)

        # It is not required any more
        del page

        # Collect meta data
        children = selector.find('./channel').getchildren()

        for child in children:

            # Collect all the feeds (items)
            if child.tag == 'item':
                feed_items = child.getchildren()
                items = []

                for item in feed_items:
                    tag = item.tag

                    if tag.endswith('thumbnail'):
                        tag = 'thumbnail'

                    item = {
                        'text': item.text,
                        'attributes': item.attrib,
                        'tag': tag,
                    }

                    items.append(item)
                self._feeds['items'].append(items)

            else:
                # Assuming that rest of the tag would be meta data
                meta = child.tag

                if meta:
                    # Get text of meta tags Except image
                        # Get url of image
                    self._feeds['meta'][meta] = child.find('./url').text \
                        if meta == 'image' \
                        else child.text

        return self._feeds
