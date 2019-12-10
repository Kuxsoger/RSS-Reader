from setuptools import setup, find_packages
from rss_reader import __version__


setup(
    name='rss_reader',
    version=__version__,
    description='Command-line RSS reader.',
    author='Andrey Kuksik',
    author_email='andrey.kuksik@gmail.com',
    url='https://github.com/Kuxsoger/RSS-Reader',
    python_requires='>=3.8',
    install_requires=[
        'beautifulsoup4',
        'lxml',
        'feedparser',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['rss-reader = rss_reader.reader:run']
    }
)