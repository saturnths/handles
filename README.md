# Handle Scraper
An asynchronous scraper. Given a list of urls, returns all twitter handles for each url.

Python 3, Flask, asyncio/aiohttp.

![UI](https://raw.githubusercontent.com/saturnths/handles/master/screenshots/UI.png)

## Search options
* **text**: ignore HTML tags and search within page content.
* **links**: search within the links that point to twitter.com.

## Server
To start the server:

`python3 main.py`

## Tests
From the parent directory, run:

`python3 -m unittest discover tests`
