from rss_reader import __version__
from setuptools import find_packages
from setuptools import setup


setup(
    name='rss_reader',
    version=__version__,
    description='Command-line RSS reader.',
    author='Andrey Kuksik',
    author_email='andrey.kuksik@gmail.com',
    url='https://github.com/Kuxsoger/RSS-Reader',
    python_requires='>=3.7',
    install_requires=[
        'beautifulsoup4',
        'lxml',
        'feedparser',
        'httpretty',
        'sqlitedict',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['rss-reader = rss_reader.reader:run']
    }
)
