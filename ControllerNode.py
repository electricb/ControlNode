#!/usr/bin/python3.3

import re
import time
import threading


class ControllerNode():

    def __init__(self):
        self.rateLimitList = []
        self.inputList = [
            'https://en.wikipedia.org/wiki/Web_scraping',
            'https://support.google.com/webmasters/answer/182072?hl=es',
            'https://en.wikipedia.org/wiki/Web_crawler',
            'https://en.wikipedia.org/wiki/Internet_bot',
            'https://support.google.com/webmasters/answer/48620',
            'http://www.dictionary.com/browse/scraping',
            'https://en.wikipedia.org/wiki/Web_indexing',
            'https://en.wikipedia.org/wiki/Data_scraping',
            'https://en.wikipedia.org/wiki/Data_cleansing',
            'https://aws.amazon.com/products/'
        ]
        self.url_cycle(self.inputList)

    def purgatory(self, domain, url):
        """Put domains here for 5 seconds once they have been run."""

        # wait 5 seconds then run scraper node
        p = threading.Timer(5.0, run_scraper_node(url))
        p.start()
        self.rateLimitList.remove(domain)
        return

    def url_cycle(self, urlList):
        """Main cycle looping through list of inputs"""

        # loop through urls in list
        for url in urlList:
            # Define criteria of a domain
            # Search url string for specific groups to determine domain name only
            # First group  "http(optional s)://"
            # Second group body of domain at least 1 alpha-numeric character and hyphens
            # Third group domain extension 2-6 characters long this allows for
            # small domains like .it or large domains like .com.au
            domainCriteria = re.compile(r'((https?://)([\da-z\.-]+)\.([a-z\.]{2,6}))')

            # Pull domain from url
            # Selecting all groups from the regular expression together
            domain = re.search(domainCriteria, url).group()

            # if the domain exists in list of domains at the rate limit
            # then send domain to purgatory to wait until rate limit has passed
            # otherwise run scraper node
            if domain in self.rateLimitList:
                self.purgatory(domain, url)
            else:
                run_scraper_node(url)

            self.rateLimitList.append(domain)


def run_scraper_node(url):
    """Run the scraper node
    """

    print(time.time, url)
    return

