from __future__ import unicode_literals

from . import _util
from ._base import BlogHandler
from ._compat import parse_qs, urljoin, urlparse

class DaumBlogHandler(BlogHandler):
    @classmethod
    def canonical_url(cls, url):
        return url  # FIXME

    @classmethod
    def fetchable_url(cls, url):
        if 'ArticleContentsView.do' in url:
            return url
        if 'BlogTypeView.do' in url:
            query = parse_qs(urlparse(url).query)
            return ('http://blog.daum.net/_blog/hdn/ArticleContentsView.do'
                '?blogid={}&articleno={}'.format(
                    query['blogid'][-1], query['articleno'][-1]))
        tree = _util.fetch_tree(url, encoding=cls.encoding)
        href = tree.xpath('//frame')[0].get('src')
        url = urljoin(url, href)
        return cls.fetchable_url(url)

    @classmethod
    def get_post(cls, url):
        tree = _util.fetch_tree(url, encoding=cls.encoding)
        content = tree.xpath('//div[@id="contentDiv"]')[0]
        content = _util.tree_to_string(content)
        title = tree.xpath('//title')[0].text
        return dict(title=title, content=content)
