#### git config ignore verify ssl  (necessary)
1. git ignore verify ssl
```
git config --global http.sslVerify false
```

#### usage
1. run as proxy server, running on http://127.0.0.1:1088
```
python main.py -l 127.0.0.1 -p 1088
```

2. run as mitmproxy addon
```
mitmdump -s ghproxy_addon.py
```

####  git proxy config
1. git global proxy setting
```
git config --global http.proxy http://127.0.0.1:1088


# unset proxy
git config --global --unset http.proxy

```

2. git proxy setting for github.com
```
git config --global http.https://github.com.proxy http://127.0.0.1:1080
# unset proxy
git config --global --unset http.https://github.com.proxy
```

3. git proxy setting when clone
```
git clone https://github.com/linw1995/lightsocks-python.git --config http.proxy=http://127.0.0.1:1088 -v --progress
``` 


#### test
```
curl -k -x http://127.0.0.1:1088 https://www.baidu.com

curl -k -x http://127.0.0.1:1088 https://raw.githubusercontent.com/stilleshan/ServerStatus/master/Dockerfile
curl -k -x http://127.0.0.1:1088 https://github.com/mitmproxy/mitmproxy/archive/refs/tags/10.1.1.tar.gz --output mitmproxy-10.1.1.tar.gz

git clone https://github.com/mitmproxy/mitmproxy_rs --config http.proxy=127.0.0.1:1088 -v --progress
```


#### ref
```
https://ghproxy.com/
https://github.com/hunshcn/gh-proxy
https://github.com/mitmproxy/mitmproxy
```