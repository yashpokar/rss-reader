import xml.etree.ElementTree as ET
import requests


class HTTPResponseError(Exception):
    pass


class FeedReader(object):
    _url = ''
    _items = []

    def __init__(self, url):
        """ FeedReader
            ------------------
            @url string
        """
        self._url = url

        self._load_items()

    @property
    def items(self):
        """ items
            --------------
            @return list
        """
        return self._items

    def _load_items(self):
        """ _load_items
            ----------------------
            @return
        """

        feeds_page = self._fetch_feeds_page()
        r = self._parse_feeds(feeds_page)
        # print(r)

    def _fetch_feeds_page(self):
        """ _fetch_feeds_page
            ---------------------
            @return string
        """
        # It is not necessary to put user agent in header
            # but let server feel this request is comming from known browser (Chrome here)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

        # Requesting for the feeds
        response = requests.get(self._url, headers=headers)

        if response.status_code != 200:
            raise HTTPResponseError(f'RSS Feed isn\'t accessible, got http response code {response.status_code}')

        return response.content

    def _parse_feeds(self, page):
        """ _parse_feeds
            -------------------
            @page string xml
            @return json
        """

        # Basic promised structre of feeds
        parsed_feeds = {
            'meta_data': {},
            'items': [],
        }

        # Let instantiate the xml parser
        selector = ET.fromstring(page)

        # It is not required any more
        del page

        # Collect meta data
        children = selector.find('./channel').getchildren()

        for child in children:

            # Collect all the feeds (items)
            if child.tag == 'item':
                items = child.getchildren()

                for item in items:
                    item = {
                        'text': item.text,
                        'attributes': item.attrib,
                        'tag': item.tag,
                    }

                    parsed_feeds['items'].append(item)
            else:
                # Assuming that rest of the tag would be meta data
                meta = child.tag

                if meta:
                    parsed_feeds['meta_data'][meta] = child.text

        return parsed_feeds
