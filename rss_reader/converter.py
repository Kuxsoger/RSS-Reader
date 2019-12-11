"""Contains converter from RSS to epub format."""

import bs4
from ebooklib import epub
import logging
import os
import requests


def load_images(book, raw_description):
    """Load images into book and replace src to files from book."""
    if not hasattr(load_images, 'counter'):
        load_images.counter = 0

    soup = bs4.BeautifulSoup(raw_description, 'lxml')

    path = 'images/{}.jpg'
    for img in soup.find_all('img', src=True):
        try:
            image = requests.get(img['src']).content
        except requests.exceptions.MissingSchema:
            logging.error('Cannot load image')
            continue

        item = epub.EpubItem(file_name=path.format(load_images.counter), content=image)
        book.add_item(item)
        img['src'] = path.format(load_images.counter)
        load_images.counter += 1

    return soup.prettify()


def convert_to_epub(rss):
    """Convert rss feed to epub book."""
    logging.info('Converting to epub')

    feed_title = rss.get('parsed', {}).get('feed', {}).get('title', 'unknown')

    book = epub.EpubBook()
    book.set_identifier('123')
    book.set_title(feed_title)
    book.add_author(feed_title)
    book.spine = ['nav']
    toc = []

    html_format = (
        '<h3>{title}</h3>'
        '<h5>Date: {date}</h5>'
        '<h5>Link: <a href={link}>{link}</a></h5>'
        '{raw_description}'
    )

    for index, topic in enumerate(rss['topics']):
        file_name = '{}.xhtml'.format(index)
        chapter = epub.EpubHtml(title=topic['title'], file_name=file_name)

        topic['raw_description'] = load_images(book, topic['raw_description'])
        chapter.content = html_format.format(**topic)

        book.add_item(chapter)
        book.spine.append(chapter)
        toc.append(epub.Section(topic['title']))
        toc.append(chapter)

    book.toc = tuple(toc)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    path = rss['args'].output_path
    if not path:
        path = os.path.join(os.getcwd(), 'rss_news.epub')

    epub.write_epub(path, book, {})

    if not os.path.isfile(path):
        raise Exception('Cannot create file with that path')
