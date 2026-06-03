import sys
import urllib.request

url = 'http://127.0.0.1:8000/api/docs/'
try:
    with urllib.request.urlopen(url, timeout=10) as r:
        print('STATUS', r.getcode())
        data = r.read(800)
        print(data.decode('utf-8', errors='ignore'))
except Exception as e:
    print('ERROR', repr(e))
    sys.exit(1)
