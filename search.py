from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse
import urllib.request
import re
import asyncio
import aiohttp
import concurrent


class Search(object):

    def __init__(self, urls):
        self.urls = urls
        self.results = []
        self.pattern = r"@(?:\w){1,15}"

    @property
    def get_results(self):
        """Get the current results."""
        return self.results

    def get_handles(self, mode):
        self.mode = mode
        self.results = []

        coros = []
        for url in self.urls:
            coros.append(asyncio.Task(self.fetch_page(url)))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*coros))

        return self.results

    @asyncio.coroutine
    def fetch_page(self, url):
        response = yield from aiohttp.request('GET', url)
        content = yield from response.read()
        response.close()

        if response.status == 200:
            if self.mode == 'text':
                self.parse_text(content, url)
            elif self.mode == 'links':
                self.parse_links(content, url)
        else:
            msg = [str(response.status) + " code returned from server"]
            self.results.append({
                "url": url,
                "results": msg
            })

    def parse_text(self, content, url):
        '''Get data from a URL, convert html to plain text, and save any
        results that match the twitter handle pattern.
        '''
        soup = BeautifulSoup(content, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text()
        url_results = re.findall(self.pattern, text)

        self.results.append({"url": url, "results": url_results})

    def parse_links(self, content, url):
        '''Get all links from an URL, check that they point to twitter.com
        and that their contents match the twitter handle pattern.
        '''
        url_results = []
        for link in BeautifulSoup(content, "html.parser",
                                  parse_only=SoupStrainer('a')):
            if not link.has_attr('href'):
                continue

            is_twitter = urlparse(link['href']).hostname == 'twitter.com'
            search = re.search(self.pattern, link.get_text())

            if is_twitter and bool(search):
                url_results.append(search.group(0))

        self.results.append({"url": url, "results": url_results})
