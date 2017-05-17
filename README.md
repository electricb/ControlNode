# ControlNode README

The short test script expects an incoming list of URLs to be processed and sent to a function for scraping.
I have set it this way as I expect there to be a feeder function of some description obtaining a list of URLs to be processed. This function can this call my ControllerNode.url_cycle(LIST) and have them cycled through and sent to the scraper at the correct intervals.

For sorting and organising the URLs I initially opted to try out the threading library. I attempted to have a "purgatory" function run in a separate thread for any domain that was at its rate limit whilst the loop continues through the list of URLs.. I could not get it to work how I wanted and decided I would default back to a heap list and shuffle URLs back in a hierarchy and do time checks instead..

When a URL is processed it is sent to a function that logs the date, time, and url to a file and prints to screen (mostly for my use). This can easily be cahnged to an external spider node or repurposed into one itself.

I have done nothing in the way of web work with python before and I am not certain how I would implement such a function in practice. In theory I see this as a reactive service, rather than scanning and searching for input itself, it awaits instruction. A variation could go on the hunt for URLs and process them in waves. But I do not fully understand the HTTP POST "uri" process and the exact format it would come in to offer precise applications.
