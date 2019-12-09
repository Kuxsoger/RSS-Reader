"""Contains functions for reading RSS feed."""

import bs4
import feedparser
import html
import json
import logging


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


def read_topics(rss, limit):
    """Read topics in feed according to limit

    if limit is greater than count of topics then read all topics
    return list contains topics represented in dict.
    """
    result = []

    if not limit or limit > len(rss.entries):
        logging.info('Set limit equals to count of items.')
        limit = len(rss.entries)

    for item in rss.entries[:limit]:
        logging.info('Create topic')

        topic = {}
        topic['title'] = html.unescape(item.title)
        topic['date'] = item.published
        topic['link'] = item.link

        topic['links'] = [topic['link'] + ' (link)'] if item.link else []
        if item.description:
            soup = bs4.BeautifulSoup(item.description, 'lxml')
            replace_links(soup, topic['links'])
            topic['description'] = soup.get_text().strip()

        result.append(topic)

    return result


def print_topics(feed_title, topics):
    """Print topics."""
    logging.info('Print news')
    print('Feed:', feed_title)
    for topic in topics:
        print('\nTitle:', topic['title'])
        print('Date:', topic['date'])
        print('Link:', topic['link'], end='\n\n')
        print(topic['description'], end='\n\n')

        links = topic['links']
        if links:
            print('Links:')
            for i, link in enumerate(links, 1):
                print('[{}] - {}'.format(i, link))


def print_json(feed_title, topics):
    """Print topics in json format."""
    logging.info('Converting to json')
    js = {'feed title': feed_title, 'topics': topics}
    print(json.dumps(js, indent=4, ensure_ascii=False))


def run_reader(args):
    """Read feed with given args."""
    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    logging.info('Started with following args: {}'.format(args))

    logging.info('Getting rss')
    rss = feedparser.parse(args.source)
    feed_title = rss.feed.title

    logging.info('Read topics')
    topics = read_topics(rss, args.limit)

    if not topics:
        raise Exception('No news found')

    if args.json:
        print_json(feed_title, topics)
    else:
        print_topics(feed_title, topics)
