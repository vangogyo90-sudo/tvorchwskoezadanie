import urllib.request

urls = [
    'http://127.0.0.1:8000/',
    'http://127.0.0.1:8000/cats/',
    'http://127.0.0.1:8000/api/cats/',
    'http://127.0.0.1:8000/api/cats/?page=2',
]
for u in urls:
    try:
        with urllib.request.urlopen(u, timeout=10) as r:
            print(u, '->', r.getcode())
    except Exception as e:
        print(u, 'ERROR', repr(e))
