import logging
import re
import time
from mitmproxy import http, connection, ctx
from mitmproxy import ctx as mimtproxy_ctx
from mitmproxy import flowfilter
from mitmproxy.proxy.layers import tls
from mitmproxy.utils import human

"""
Run as follows: mitmproxy -s ghproxy.py -p 1088

curl www.baidu.com -x http://127.0.0.1:1088
curl github.com/afghanistanyn/.git
"""


logging.basicConfig(
    level=logging.INFO,
    # filename='logs/ghproxy.log',
)
logger = logging.getLogger(__name__)

black_list = '''
https://github.com/grafana/tempo
'''

class GHProxyAddon:
    def __init__(self, disable_other=False):
        self.disable_other = disable_other
        self.ghproxy_domain = "ghproxy.com"
        self.github_domains = ["github.com", "githubusercontent.com", "github.io"]
        self.black_list = [url for url in list(set(black_list.splitlines())) if len(url) != 0]
        self.raw_github_host = None

    def running(self):
        # add config for tlsconfig addon
        ctx.options.ssl_insecure = True

        # add config for proxyserver addon
        ctx.options.connection_strategy = "lazy"
        ctx.options.stream_large_bodies = "2m"

    def http_connect(self, flow: http.HTTPFlow):
        mimtproxy_ctx.log(f"receive http connect: {flow.request.url}")
        use_ghproxy = False
        for github_domain in self.github_domains:
            if github_domain in flow.request.host:
                use_ghproxy = True

        # change connect server to ghproxy.com
        if use_ghproxy:
            self.raw_github_host = flow.request.host
            flow.request.scheme = "https"
            flow.request.host = "ghproxy.com"
        else:
            if self.disable_other:
                # allow direct access ghproxy.com
                if flow.request.host != 'ghproxy.com':
                    mimtproxy_ctx.log(f"find other flow, reject it: {flow.request.pretty_url}")
                    flow.kill()
            else:
                mimtproxy_ctx.log(f"find other flow, allow it: {flow.request.pretty_url}")

    # def server_connect(self, data):
    #     print("------ server_connect - client:(%s, %s) server:(%s, %s)" % (data.client.peername, data.client.sockname, data.server.sockname, data.server.peername))
    #
    # def server_connected(self, data):
    #     print("------ server_connected - client:(%s, %s) server:(%s, %s)" % (data.client.peername, data.client.sockname, data.server.sockname, data.server.peername))

    def request(self, flow: http.HTTPFlow):
        if flow.request.path in self.black_list:
            mimtproxy_ctx.log(f"find blacked flow: {flow.request.pretty_url}")
            flow.kill()

        if self.raw_github_host:
            raw_url = flow.request.url.replace("ghproxy.com", self.raw_github_host)
            mimtproxy_ctx.log(f"find github flow: {flow.request.pretty_url}")
            # change url to ghproxy.com/raw_url
            flow.request.scheme = "https"
            flow.request.host = "ghproxy.com"
            flow.request.path = f"/{raw_url}"
            logger.info(f"ghproxy change url to {flow.request.pretty_url}")

    # def response(self, flow: http.HTTPFlow):
    #     print(flow.response)


addons = [GHProxyAddon()]