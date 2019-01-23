import sys
import requests
from bs4 import BeautifulSoup
from sqlitedict import SqliteDict

line = 'NOT EOF'
urlcache = SqliteDict('./urlcache.sqlite', autocommit=True)


def get_title(domain):
    title = urlcache.get(domain)
    if title is None:
        try:
            r = requests.get('http://' + domain + '/', timeout=5)
        except:
            urlcache[domain] = "noaccess"
            return "noaccess"
        if r.status_code != 200:
            urlcache[domain] = str(r.status_code)
            return str(r.status_code)
        else:
            r.encoding = 'utf-8'
            dom = BeautifulSoup(r.text, 'html.parser')
            if dom.title is not None:
                urlcache[domain] = dom.title.text
                return dom.title.text
            else:
                urlcache[domain] = "notitle"
                return "notitle"
    return title


while line != '':
    line = sys.stdin.readline()
    if line != '':
        line = line.strip()
#        print(line)
        segs = line.split('\u3000')
#        print(segs)
        if len(segs) > 1:
            domain = segs[1]
#            print('Getting',domain)
            title = get_title(domain)
            title = title.replace('\n', '')
            segs2 = segs[0].split()
            print(segs2[0], domain, "[", title, "]")

# print(get_title(sys.argv[1]))
urlcache.close()
