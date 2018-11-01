import requests
import requests as requests
from lxml import etree
from collections import namedtuple
def tidy_query_info(data):
    info={}
    hits = data['result']['hits']
    info['query'] = data['result']['query']
    info['results']= []
    for author in hits['hit']:
        info['results'].append(author['info']['url'].split('https://dblp.org/pid/',1)[1])
    return info



DBLP_BASE_URL = 'http://dblp.uni-trier.de/'
DBLP_AUTHOR_SEARCH_URL = DBLP_BASE_URL + 'search/author'
resp = requests.get(DBLP_AUTHOR_SEARCH_URL, params={'xauthor':'michael ley'})
root = etree.fromstring(resp.content)
print('Hola')

url = 'http://dblp.org/search/author/api'
response = requests.get(url, params={'q':'Anastassiou', 'format': 'json'})
data = response.json()



info = tidy_query_info(data)

url2 = 'https://dblp.org/pid/91/6231'
aux2 = url2.split('https://dblp.org/pid/',1)

print(info)


