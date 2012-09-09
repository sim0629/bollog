from . import _util
from ._base import BlogHandler

class EgloosHandler(BlogHandler):
    @classmethod
    def get_post(cls, url):
        tree = _util.fetch_tree(url)
        candidates = list(_util.merge_list(
            tree.xpath('//div[@class="post_title"]/h2/a'),
            tree.xpath('//div[@class="post_subject"]/a'),
            tree.xpath('//div[@class="POST_TTL"]/a'),
            tree.xpath('//h3[@class="posttitle"]/a'),
            tree.xpath('//div[@class="titleWrap"]/h2/a'),
        ))
        title = candidates[0].text.strip()
        content = tree.xpath('//div[@class="hentry"]')[0]
        content = _util.tree_to_string(content)
        return dict(title=title, content=content)

    @classmethod
    def find_entry(cls, url):
        tree = _util.fetch_tree(url)
        for entry in _util.merge_list(
            tree.xpath('//div[@id="titlelist_list"]//li/a'),
#            tree.xpath('//div[@class="content"]/a'),
            tree.xpath('//div[@class="POST_BODY"]/a'),
        ):
            yield dict(href=entry.get('href'), title=entry.text)
        for entry in tree.xpath('//div[@class="hentry"]'):
            container = entry.getparent().getparent()
            a = container.xpath('.//*[@class="post_title"]//a')[0]
            yield dict(href=a.get('href'), title=a.get('title'))

    @classmethod
    def next(cls, url):
        if 'page/' in url:
            url, _, n = url.partition('page/')
            n = int(n)
        else:
            n = 1
        return url + 'page/{}'.format(n + 1)
