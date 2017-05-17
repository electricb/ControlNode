#!/usr/bin/python3.4

import re
import time
import datetime
import heapq


class ControllerNode(object):

    def __init__(self):

        # For the purposes of this test I have set up the example input URLs in a list
        # as I am unfamiliar with the instructions
        # This will then be passed on to the main routine to cycle through.
        # It is assumed that the incoming data will be in list or tuple form for use here.
        inputList = [
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
        # Call method providing it with the list of URLs
        self.url_cycle(inputList)

    @staticmethod
    def url_cycle(urlList):
        """Main cycle looping through list of URLs

        This method takes the incoming list of URLs and converts it to a heap.
        We use a heap so that we can iterate through the list and return
        any URLs required to wait to the back of the queue.

        Any domains that are 'waiting' are kept in a dictionary as a
        key and the time it was last run as its value.
        we refer back to this to check against the time passed
        and if we can now call that domain again.
        """

        # Define dictionary for tracking "waiting" domains
        rateLimitDict = {}

        # Define the heap ready to insert the list items in to.
        # I understand I could just use heapify but that will not maintain the order of
        # the incoming data, should that be important.
        urlHeap = []
        for url in urlList:
            heapq.heappush(urlHeap, (time.time(), url))
            #  Arbitrary time set to sleep before continuing the loop,
            # this makes sure the incoming list maintains its original order
            time.sleep(0.00001)

        # Once we send a url of the be scraped it will be removed from the heap. This will loop
        # while the heap still has items within it
        while len(urlHeap) > 0:
            # Define criteria of a domain
            # Search url string for specific groups to determine domain name only
            # First group  "http(optional s)://"
            # Second group body of domain at least 1 alpha-numeric character and hyphens
            # Third group domain extension 2-6 characters long this allows for
            # small domains like .it or large domains like .com.au

            #############
            # Since writing this I have discovered urlparse.py which does the
            # same thing but a little more elegantly than I have done it
            #############
            domainCriteria = re.compile(r'((https?://)([\da-z\.-]+)\.([a-z\.]{2,6}))')

            # Selects the top url from the heap
            url = heapq.heappop(urlHeap)[1]
            # Pull domain from url
            # Selecting all groups from the regular expression together
            domain = re.search(domainCriteria, url).group()

            # Check if the domain exists in the dictionary of domains at their rate limit
            if domain in rateLimitDict.keys():
                # Check if the current time is beyond the 5 second limit
                # since the last time this domain was called.
                if time.time() >= rateLimitDict[domain] + 5.0:
                    # If the enough time ahs elapsed then we remove the entry
                    # from the dictionary and run the scraper. Once that has
                    # run we add the domain back to the dictionary with the new current time
                    del rateLimitDict[domain]
                    run_scraper_node(url)
                    rateLimitDict[domain] = time.time()
                else:
                    # If not enough time has elapsed then add the url back to the heap
                    # with the current time
                    heapq.heappush(urlHeap, (time.time(), url))
            else:
                # If domain hasn't been scraped before, run the scraper and add to
                # the dictionary of scraped domains with the current time
                run_scraper_node(url)
                rateLimitDict[domain] = time.time()

        exit()


def run_scraper_node(url):
    """Run the scraper node
    """

    timeStamp = time.time()
    dateAndTime = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
    print(dateAndTime, url)

    return

if __name__ == "__main__":
        ControllerNode()
