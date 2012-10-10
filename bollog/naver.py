from __future__ import unicode_literals

import json
import re

from . import _util
from ._base import BlogHandler
from ._compat import parse_qs, unquote_plus, urljoin, urlopen, urlparse

class NaverBlogHandler(BlogHandler):
    encoding = 'cp949'

    @classmethod
    def canonical_url(cls, url):
        return url  # FIXME
        query = parse_qs(urlparse(url).query)
        return 'http://blog.naver.com/{}/{}'.format(
            query['blogId'][-1], query['logNo'][-1])

    @classmethod
    def fetchable_url(cls, url):
        if 'PostView.nhn' in url:
            return url
        for regex in [
            r'http://(?P<id>\w+)\.blog\.me/(?P<num>\d+)',
            r'http://blog\.naver\.com/(?P<id>\w+)/(?P<num>\d+)',
        ]:
            m = re.match(regex, url)
            if m is None:
                continue
            return 'http://blog.naver.com/PostView.nhn?blogId={}&logNo={}'\
                .format(m.group('id'), m.group('num'))
        tree = _util.fetch_tree(url, encoding=cls.encoding)
        url = tree.xpath('//frame[@id="screenFrame"]')[0].get('src')
        return cls.fetchable_url(url)

    @classmethod
    def get_post(cls, url):
        tree = _util.fetch_tree(url, encoding=cls.encoding)
        content = tree.xpath('//table[@class="post-body"]//td[@class="bcc"]/div')[0]
        content = _util.tree_to_string(content)
        # TODO: title
        return dict(content=content)

    @classmethod
    def find_entry(cls, url):
        js = urlopen(url).read()
        js = js.decode('cp949').replace(r"\'", "'")
        data = json.loads(js)
        for entry in data['postList']:
            # Surprise: Naver Blog using UTF-8!
            title = unquote_plus(entry['title'], encoding='utf8')
            href = 'http://blog.naver.com/PostView.nhn?blogId={}&logNo={}'\
                .format(data['blog']['blogId'], entry['logNo'])
            yield dict(title=title, href=href)

    @classmethod
    def next(cls, uri):
        if 'currentPage=' not in uri:
            return None
        uri, _, n = uri.rpartition('currentPage=')
        n = int(n)
        if n <= 1:
            return None
        return uri + 'currentPage={}'.format(n - 1)

    @classmethod
    def get_attachment_urls(cls, url):
        try:
            tree = _util.fetch_tree(url, encoding='cp949')
            frame = tree.xpath('//*[@id="screenFrame"]')[0]
            src = frame.get('src')
            if not src:
                return []
            url = urljoin('http://blog.naver.com/', src)
        except IndexError:
            pass
        try:
            tree = _util.fetch_tree(url, encoding='cp949')
            frame = tree.xpath('//*[@id="mainFrame"]')[0]
            src = frame.get('src')
            if not src:
                return []
            url = urljoin('http://blog.naver.com/', src)
        except IndexError:
            pass
        html = urlopen(url).read().decode('cp949')
        m = re.search(r'aPostFiles\[1\] = (.*?);\r\n', html)
        data = json.loads(m.group(1).replace("'", '"'))
        result = [_['encodedAttachFileUrl'] for _ in data]
        tree = _util._parser.parse(html)
        for a in tree.xpath(
                '//table[@class="post-body"]//td[@class="bcc"]/div//a'):
            if a.find('img') is None:
                continue
            href = a.get('href', '')
            if not href:
                continue
            href = href.replace(' ', '%20')
            result.append(href)
        return result
