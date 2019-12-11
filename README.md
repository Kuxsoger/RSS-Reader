# RSS Reader
This is command line utility that recieves RSS URL and print news in human-readable format.

# Usage

```
  rss-reader [-h] [--limit LIMIT] [--json] [--version] [--verbose] [--date DATE] 
             [--to-epub] [--output-path OUTPUT_PATH] [--colorize] source

positional arguments:
  source                RSS URL

optional arguments:
  -h, --help            show this help message and exit
  --limit LIMIT         Limit news tops if this parameter provided
  --json                Print result as JSON in stdout
  --version             Print version info
  --verbose             Outputs verbose status messages
  --date DATE           Read from cache news with date given in YYYYMMDD format
  --to-epub             Generate file with news in epub format
  --output-path OUTPUT_PATH
                        Path to new file where book will be placed
  --colorize            Enable colorized mode
```

# JSON structure

```
{
    "feed title": "New Movies",
    "topics": [
        {
            "title": "Black Christmas (2019)",
            "date": "Wed, 11 Dec 2019 09:14:42 GMT",
            "link": "http://www.fandango.com/blackchristmas2019-220065/movie-overview?wssaffid=11840&wssac=123",
            "links": [
                "http://www.fandango.com/blackchristmas2019-220065/movie-overview?wssaffid=11840&wssac=123 (link)",
                "https://images.fandango.com/r1.0.819/ImageRenderer/111/168/images/no_image_111x168.jpg/220065/images/masterrepository/fandango/220065/blackchristmas2019.jpg (image)",
                "http://www.fandango.com/blackchristmas2019-220065/movie-overview?wssaffid=11840&wssac=123 (link)",
                "http://www.fandango.com/movie-trailer/blackchristmas2019-trailer/220065?wssaffid=11840&wssac=123 (link)",
                "https://images.fandango.com/r1.0.819//images/global/buy_tickets.gif (image)"
            ],
            "description": "[image: Black Christmas (2019)][2] Opens Friday, Dec 13, 2019Movie Details[3]Play Trailers[4][image: Click here to see showtimes and buy tickets!][5]"
        },
        {
            ...
        },
        ...
    ]
}
```

# Caching
News is stored in SQLite table.
