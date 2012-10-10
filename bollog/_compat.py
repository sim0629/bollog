# Python 2 vs. 3 compatibility
try:
    from urllib.parse import parse_qs, unquote_plus, urljoin, urlparse
    from urllib.request import Request, urlopen
except ImportError:
    from urllib import unquote_plus
    from urllib2 import Request, urlopen
    from urlparse import parse_qs, urljoin, urlparse
