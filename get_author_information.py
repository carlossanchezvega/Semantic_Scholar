import sys, requests
from nltk.tokenize import sent_tokenize, word_tokenize


def tidy_query_info(data):
    info={}
    hits = data['result']['hits']
    info['query'] = data['result']['query']
    info['results']= []
    for author in hits['hit']:
        info['results'].append(author['info']['url'].split('https://dblp.org/pid/',1)[1])
    return info


def get_titles_from_author_dblp():
    url = 'http://dblp.org/search/author/api'
    response = requests.get(url, params={'q':'Anastassiou', 'format': 'json'})
    data = response.json()
    info = tidy_query_info(data)
    return info



def main():
    try:
        info = get_titles_from_author_dblp()
    except Exception as ex:
        print (ex.message)
        return 1 # indicates error, but not necessary
    else:
        return 0 # return 0 # indicates errorlessly exit, but not necessary

# this is the standard boilerplate that calls the main() function
if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()