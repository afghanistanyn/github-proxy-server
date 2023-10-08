import argparse
import asyncio
import logging
import signal

from mitmproxy import options
from ghproxy_addon import GHProxyAddon
from dump_master import DumpMaster

logging.basicConfig(
    level=logging.INFO,
    # filename='logs/ghproxy.log',
)

class GHProxyServer():
    def __init__(self, host="127.0.0.1", port=1088):
        self.proxy_host = host
        self.proxy_port = int(port)
        self.master = None

    def close(self, *args):
        if self.master:
            self.master.shutdown()
            logging.info("ghproxy server is shutdown...")

    def run(self):
        logging.info("ghproxy server is starting...")
        logging.info("Listening: {}:{}".format(self.proxy_host, self.proxy_port))
        opts = options.Options(
            listen_host="127.0.0.1",
            listen_port=self.proxy_port,
        )

        loop = asyncio.get_event_loop()
        self.master = DumpMaster(opts, with_dumper=False, with_termlog=False, event_loop=loop)
        self.master.addons.add(GHProxyAddon())
        logging.info("ghproxy server started successfully...")
        signal.signal(signal.SIGTERM, self.close)
        signal.signal(signal.SIGINT, self.close)
        loop.run_until_complete(asyncio.wait([self.master.run()]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="ghproxy server v0.1 (Proxying Github)")
    parser.add_argument("-l", "--listen", default="127.0.0.1", help="ghproxy server bind host")
    parser.add_argument("-p", "--port", default="1088", help="ghproxy server bind port")
    args = parser.parse_args()

    ghproxy = GHProxyServer(port=args.port)
    ghproxy.run()