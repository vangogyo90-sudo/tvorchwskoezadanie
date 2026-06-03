import json
import urllib.request

url = 'http://127.0.0.1:8000/api/schema/'
try:
    with urllib.request.urlopen(url, timeout=10) as r:
        raw = r.read()
        text = raw.decode('utf-8', errors='ignore')
        if not text.strip().startswith('{'):
            print('Non-JSON response start:')
            print(text[:800])
        else:
            data = json.loads(text)
            paths = data.get('paths', {})
            for p, methods in paths.items():
                if p.startswith('/api/cats') or p.startswith('/api/health-passports') or p.startswith('/api/health-records'):
                    print('\nPATH', p)
                    for m, info in methods.items():
                        print('  ', m)
                        params = info.get('parameters') or []
                        for par in params:
                            print('    -', par.get('name'), par.get('in'), par.get('schema', {}).get('type'))
except Exception as e:
    print('ERROR', repr(e))
    raise
