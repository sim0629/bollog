from __future__ import unicode_literals

from . import _util
from ._base import BlogHandler

class TistoryHandler(BlogHandler):
    @classmethod
    def get_post(cls, url):
        tree = _util.fetch_tree(url)
        candidates = list(_util.merge_list(
            tree.xpath('//div[@class="article"]'),
            tree.xpath('//div[@class="entry"]'),
            tree.xpath('//div[@class="post"]'),
            tree.xpath('//div[@class="awrap"]'),
            tree.xpath('//div[@class="wrap_entry"]'),
            tree.xpath('//div[@class="article_holder"]'),
            tree.xpath('//div[@class="postCont"]'),
            tree.xpath('//div[@class="article_contents"]'),
        ))
        content = candidates[0]
        # TODO: remove tt-plugin, another_category, etc.
        content = _util.tree_to_string(content)
        # TODO: title
        return dict(content=content)

    @classmethod
    def find_entry(cls, url):
        tree = _util.fetch_tree(url)
        for entry in _util.merge_list(
#            tree.xpath('//div[@id="main"]//a'),
            tree.xpath('//div[@id="content"]//li//a'),
            tree.xpath('//div[@id="contents"]//li//a'),
            tree.xpath('//div[@id="searchList"]//li//a'),
            tree.xpath('//div[@class="searchList"]//li/a'),
            tree.xpath('//div[@class="awrap"]//li/a'),
            tree.xpath('//div[@class="wrap_search"]//li/a'),
            tree.xpath('//td[@class="textarea2"]/a'),
            tree.xpath('//ul[@class="r_list"]/li/a'),
            tree.xpath('//td[@class="memo_style"]/a'),
            tree.xpath('//div[@class="post"]/a'),
        ):
            if '#' in entry.get('href', ''):
                continue
            if entry.get('onclick'):
                continue
            yield dict(href=entry.get('href'), title=entry.text)

    @classmethod
    def next(cls, url):
        if 'page=' in url:
            url, _, n = url.partition('page=')
            n = int(n)
        else:
            n = 1
        return url + 'page={}'.format(n + 1)
