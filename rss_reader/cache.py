"""Functions for caching news."""

import dateutil.parser
import logging
import os
import sqlitedict


CACHE_FILE = '.rsscache'


def cache_topics(rss):
    """Add topics to cache file."""
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), CACHE_FILE)
    with sqlitedict.SqliteDict(path) as db:
        feed_link = rss['args'].source
        dates = db.get(feed_link, {})

        for topic in rss['topics']:
            date = dateutil.parser.parse(topic['date'])
            date = date.strftime('%Y%m%d')

            news = dates.get(date, {})

            link = topic['link']
            if link in news:
                logging.info('Topic with link {} already cached'.format(link))
                continue

            logging.info('Cache topic with link {} from {}'.format(link, feed_link))
            news[link] = topic
            dates[date] = news

        db[feed_link] = dates
        db.commit()


def get_topics(feed_link, date):
    """Get topics with given date from cache."""
    logging.info('Get topics from cache file with date {} and source {}'.format(date, feed_link))
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), CACHE_FILE)
    with sqlitedict.SqliteDict(path) as db:
        return list(db.get(feed_link, {}).get(date, {}).values())
