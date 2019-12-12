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
News is stored in SQLiteDict table.
Format of news is dict:
```
{
    'https://news.yahoo.com/rss/': 
    {
        '20191211':
        {
            'https://news.yahoo.com/turkey-retaliate-against-u-sanctions-075046557.html':
            {
                'title': 'Turkey says will retaliate against any sanctions ahead of U.S. vote',
                'date': 'Wed, 11 Dec 2019 02:50:46 -0500',
                'link': 'https://news.yahoo.com/turkey-retaliate-against-u-sanctions-075046557.html',
                'description': '[image: Turkey says will retaliate against any sanctions ahead of U.S. vote][2]Turkey said on Wednesday it would retaliate against any U.S. sanctions over its purchase of Russian defense systems, adding that with Britain it had agreed to speed up a joint fighter jet program to meet Turkish defense needs.  U.S. lawmakers will vote - and likely pass - a defense bill later on Wednesday that calls for sanctions against Turkey over Ankara's decision to procure the S-400 defenses.  Turkey and the United States, NATO allies, have been at odds over the purchase.',
                'raw_description': '<p><a href="https://news.yahoo.com/turkey-retaliate-against-u-sanctions-075046557.html"><img src="http://l2.yimg.com/uu/api/res/1.2/fcUcI61QMQXPduOMWku.Bw--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media.zenfs.com/en-US/reuters.com/529ece937d127bfe076caafa6c8172bd" width="130" height="86" alt="Turkey says will retaliate against any sanctions ahead of U.S. vote" align="left" title="Turkey says will retaliate against any sanctions ahead of U.S. vote" border="0" ></a>Turkey said on Wednesday it would retaliate against any U.S. sanctions over its purchase of Russian
defense systems, adding that with Britain it had agreed to speed up a joint fighter jet program to meet Turkish defense needs.  U.S. lawmakers will vote - and likely pass - a defense bill later on Wednesday that calls for sanctions against Turkey over Ankara's decision to procure the S-400 defenses.  Turkey and the United States, NATO allies, have been at odds over the purchase.<p><br clear="all">',
                'links': [
                    'https://news.yahoo.com/turkey-retaliate-against-u-sanctions-075046557.html (link)',
                    'http://l2.yimg.com/uu/api/res/1.2/fcUcI61QMQXPduOMWku.Bw--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media.zenfs.com/en-US/reuters.com/529ece937d127bfe076caafa6c8172bd (image)'
                ]
            },
            ...
        },
        ...
    },
    ...
}
```
