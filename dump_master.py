import asyncio
from mitmproxy import addons
from mitmproxy.addons import termlog, dumper, keepserving, readfile, errorcheck
from mitmproxy.options import Options
from mitmproxy.master import Master

# 高版本DumpMaster(> 7.0.4)不支持直接使用, 否则报No running event loop异常, 重写DumpMaster传入event_loop
# https://github.com/mitmproxy/mitmproxy/issues/5780


class DumpMaster(Master):
    def __init__(self, options: Options, with_termlog=True, with_dumper=True, event_loop: asyncio.AbstractEventLoop = None) -> None:
        super().__init__(options, event_loop=event_loop)
        if with_termlog:
            self.addons.add(termlog.TermLog())
        self.addons.add(*addons.default_addons())
        if with_dumper:
            self.addons.add(dumper.Dumper())
        self.addons.add(
            keepserving.KeepServing(),
            readfile.ReadFileStdin(),
            errorcheck.ErrorCheck(),
        )