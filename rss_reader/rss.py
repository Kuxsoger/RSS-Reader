"""Contains functions for reading RSS feed."""

import bs4
import colorama
import coloredlogs
import feedparser
import html
import json
import logging

from rss_reader import cache
from rss_reader import converter


def replace_links(soup, links):
    """Replace <a> and <img> in BeautifulSoup with it text/title + [] contains index of link

    store all links in given list.
    """
    for link in soup.find_all(['a', 'img']):
        if link.name == 'a' and link.text and link.get('href', None):
            links.append(link['href'] + ' (link)')
            link.replace_with('{}[{}]'.format(link.text, len(links)))
        elif link.name == 'img' and link.get('src', None):
            links.append(link['src'] + ' (image)')

            # Image title on different feeds can be in title or alt attributes
            img_title = link.get('title', '').strip()
            if not img_title:
                img_title = link.get('alt', '').strip()

            link.replace_with('[image: {}][{}]'.format(img_title, len(links)))

    return links


def read_topics(rss):
    """Read topics in feed according to limit

    if limit is greater than count of topics then read all topics
    return list contains topics represented in dict.
    """
    result = []

    limit = rss['args'].limit
    items = rss['parsed'].get('entries', [])
    if not limit or limit > len(items):
        logging.info('Set limit equals to count of items.')
        limit = len(items)

    for item in items[:limit]:
        logging.info('Create topic')

        topic = {
            'title': html.unescape(item.get('title', 'unknown')),
            'date': item.get('published', 'unknown'),
            'link': item.get('link', None),
        }

        topic['links'] = [topic['link'] + ' (link)'] if topic['link'] else []
        if item.get('description', None):
            soup = bs4.BeautifulSoup(item['description'], 'lxml')
            topic['raw_description'] = item['description']
            replace_links(soup, topic['links'])
            topic['description'] = soup.get_text().strip()

        result.append(topic)

    return result


def print_topics(rss):
    """Print topics."""
    logging.info('Print news')
    feed_title = rss.get('parsed', {}).get('feed', {}).get('title', 'unknown')
    colorize = rss['args'].colorize
    
    if colorize:
        print(colorama.Fore.RED, end='')

    print('Feed:', feed_title)
    for topic in rss['topics']:
        if colorize:
            print(colorama.Fore.LIGHTGREEN_EX, end='')
        print('\nTitle:', topic['title'])

        if colorize:
            print(colorama.Fore.LIGHTYELLOW_EX, end='')
        print('Date:', topic['date'])

        if colorize:
            print(colorama.Fore.LIGHTBLUE_EX, end='')
        print('Link:', topic['link'], end='\n\n')

        if colorize:
            print(colorama.Fore.LIGHTCYAN_EX, end='')
        print(topic['description'], end='\n\n')

        if colorize:
            print(colorama.Fore.BLUE, end='')
        links = topic['links']
        if links:
            print('Links:')
            for i, link in enumerate(links, 1):
                print('[{}] - {}'.format(i, link))

    if colorize:
        print(colorama.Fore.RESET)


def print_json(rss):
    """Print topics in json format."""
    logging.info('Converting to json')

    feed_title = rss.get('parsed', {}).get('feed', {}).get('title', 'unknown')

    for dct in rss['topics']:
        dct.pop('raw_description', None)

    js = {'feed title': feed_title, 'topics': rss['topics']}
    
    if rss['args'].colorize:
        print(colorama.Fore.LIGHTBLUE_EX)

    print(json.dumps(js, indent=4, ensure_ascii=False))
    
    if rss['args'].colorize:
        print(colorama.Fore.RESET)


def read_from_url(args):
    """Read RSS feed from url and cache it."""
    parsed = feedparser.parse(args.source)

    if parsed['bozo']:
        if type(parsed['bozo_exception']) is not feedparser.NonXMLContentType:
            raise Exception('Wrong validate or no Internet connection.')
        logging.info('NonXMLContentType found')

    rss = {
        'args': args,
        'parsed': parsed,
    }

    logging.info('Read topics')
    rss['topics'] = read_topics(rss)
    cache.cache_topics(rss)

    return rss


def run_reader(args):
    """Read feed with given args."""
    if args.colorize:
        coloredlogs.install()
        colorama.init()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    logging.info('Started with following args: {}'.format(args))

    logging.info('Getting rss')

    if args.date:
        topics = cache.get_topics(args.source, args.date)
        limit = args.limit

        if not limit or limit > len(topics):
            logging.info('Set limit equals to count of topics')
            limit = len(topics)

        rss = {
            'args': args,
            'topics': topics[:limit],
        }
    else:
        rss = read_from_url(args)

    if not rss['topics']:
        raise Exception('No news found')

    if args.to_epub:
        converter.convert_to_epub(rss)
    elif args.json:
        print_json(rss)
    else:
        print_topics(rss)
