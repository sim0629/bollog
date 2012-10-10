# coding: utf8
from __future__ import unicode_literals

from . import _util
from ._compat import Request, urljoin, urlopen
from .daum import DaumBlogHandler
from .egloos import EgloosHandler
from .naver import NaverBlogHandler
from .textcube import TextcubeHandler
from .tistory import TistoryHandler

HANDLER_CLASS = {
    'daum': DaumBlogHandler,
    'egloos': EgloosHandler,
    'naver': NaverBlogHandler,
    'textcube': TextcubeHandler,
    'tistory': TistoryHandler,
}


class Blog:
    def __init__(self, url):
        self.blog_type = _get_blog_type(url)
        self.handler = HANDLER_CLASS.get(self.blog_type)
        self.url = url

    def __iter__(self):
        return PostIterator(self.url)


class PostIterator:
    def __init__(self, url, handler=None):
        self.url = url
        if not handler:
            self.handler = _get_handler_class(url)
        self.iterable = self.handler.find_entry(url)

    def __iter__(self):
        return self

    def next(self):
        """블로그 역주행"""
        try:
            entry = next(self.iterable)
        except StopIteration:
            self.url = self.handler.next(self.url)
            if not self.url:
                raise StopIteration
            self.iterable = self.handler.find_entry(self.url)
            entry = next(self.iterable)
        href = urljoin(self.url, entry['href'])
        return Post(href, title=entry.get('title'))


class Post:
    def __init__(self, url, handler=None, title=None):
        if not handler:
            self.handler = _get_handler_class(url)
        self.url = self.handler.canonical_url(url)
        self.fetchable_url = self.handler.fetchable_url(url)
        info = self.handler.get_post(self.fetchable_url)
        self.title = title or info.get('title')
        self.content = info.get('content')

    def __repr__(self):
        return "<Post {} {}>".format(self.url, repr(self.title))



def _get_handler_class(url):
    return HANDLER_CLASS.get(_get_blog_type(url))


def _get_blog_type(url):
    if url.startswith('http://blog.daum.net'):
        return 'daum'
    html = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read()
    encoding = 'utf-8'
    try:
        html.decode('cp949')
        encoding = 'cp949'
    except UnicodeDecodeError:
        pass
    tree = _util._parser.parse(html, encoding=encoding)
    if any('blog.naver.com' in _.get('src', '') for _ in
            tree.xpath('//frame')):
        return 'naver'
    if any('blog.naver.com' in _.get('href', '') for _ in
            tree.xpath('//link[@rel="wlwmanifest"]')):
        return 'naver'
    css = [_.get('href', '') for _ in tree.xpath('//link[@rel="stylesheet"]')]
    if not css:
        return None
    if any('daumcdn.net/' in _ for _ in css):
        return 'tistory'
    if any('/tc/skin/' in _ for _ in css):
        return 'textcube'
    if any('/tc/style/' in _ for _ in css):
        return 'textcube'
    if any('//md.egloos.com/' in _ for _ in css):
        return 'egloos'
    if any('/nversioning/' in _ for _ in css):
        return 'naver'
    raise Exception('Unknown type of blog')
    return None
