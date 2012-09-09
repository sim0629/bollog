from . import _util
from ._base import BlogHandler

class TextcubeHandler(BlogHandler):
    @classmethod
    def get_post(cls, url):
        tree = _util.fetch_tree(url)
        tree.xpath('//div[@class="article entry-content"]')
        raise NotImplementedError

    @classmethod
    def find_entry(cls, tree):
        raise NotImplementedError
