from __future__ import unicode_literals

class BlogHandler:
    encoding = 'utf-8'

    @classmethod
    def canonical_url(cls, url):
        return url

    @classmethod
    def fetchable_url(cls, url):
        return url

    @classmethod
    def get_post(cls, url):
        raise NotImplementedError

    @classmethod
    def find_entry(cls, url):
        raise NotImplementedError

    @classmethod
    def next(cls, uri):
        return None
