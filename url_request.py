#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import urllib.error
from urllib.parse import urlparse

class URLRequest(object):
    def get(self, url_request, proxy_address):
        try:
            parsed = urlparse(proxy_address)
            scheme = parsed.scheme
            proxy = f"{parsed.hostname}:{parsed.port}"

            proxy_handler = urllib.request.ProxyHandler({scheme: proxy})
            opener = urllib.request.build_opener(proxy_handler)
            urllib.request.install_opener(opener)

            req = urllib.request.Request(url_request)
            response = urllib.request.urlopen(req, timeout=3)
            return response
        except urllib.error.HTTPError as e:
            return e  # Still return the error to allow inspection
        except urllib.error.URLError as e:
            return None
        except Exception as e:
            # Uncomment this for debugging
            # print(f"[!] Exception during URLRequest: {e}")
            return None
