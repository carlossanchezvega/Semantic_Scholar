import pymongo
import sys, requests
import time
from bs4 import BeautifulSoup
from re import search
import unidecode
import os
from threading import Thread
#from threading import Thread
#import bson
import logging


import nltk

# TENGO QUE EJECUTAR ESTA

from CheckBestAuthorSimilarity import CheckBestAuthorSimilarity

def MAX_NUMBER_OF_ARTICLES():
    return 5

def SUCCESS():
    return 200


def get_best_coincidence(data):
    """
        We try to find the best coincidence to the author introduced by the user
        (we may not introduce exactly the name of the author (say abbreviations,
        misspellings ...)

        Args:
            data (dict): dictionnary containing all the info recovered from the request

        Returns:
            best_coincidence: The name of the author, in the database of dblp, that fits
            the best with the name of the author introduced by the user
    """

    best_similarity = 0

    # in caso we do not find any coincidence corresponding to that name
    if data['result']['hits']['@total']=='0':
        return data['result']['query']
    else:
        #best_concidence = data['result']['hits']['hit'][0]['info']['author']
        best_concidence = data['result']['query']

        # we go over the author list from the second author on, calculating best similarity
        for x in range(0, len(data['result']['hits']['hit'])):
            check_similarity = CheckBestAuthorSimilarity(data['result']['query'], data['result']['hits']['hit'][x]['info']['author'])
            new_similarity = check_similarity.getSimilarity()

            # in case the name of the new author has better similarity
            if best_similarity < new_similarity:
                best_concidence = data['result']['hits']['hit'][x]['info']['author']
                best_similarity = new_similarity
        return best_concidence



def get_coincidence_from_dblp(teacher):
    """
        We request the dblp api in search of the exact name of the author in dblp, based
        on the author introduced by the user

        Args:

        Returns:
            best_coincidence: The name of the author, in the database of dblp, which fits
            the best with the name introduced by the user
    """

    url = 'http://dblp.org/search/author/api'
    #response = requests.get(url, params={'q':'Anastassiou', 'format': 'json'})
    response = requests.get(url, params={'q': teacher, 'format': 'json'})
    data = response.json()
    best_coincidence = get_best_coincidence(data)
    return best_coincidence


def get_author_id(author_from_dblp, tidy_info):
    """
        We request, the Semantic Scholar api, the article with the "doi" received.
        Once received, we compare the name of the author to the authors of that article
        (the author ID we are looking for is by the author name)

        Args:
            author_from_dblp (string): name of the author we are looking for
            doi (string: identifier of the article in the Semantic Scholar Api
get_author_id
        Returns:
            author_id: The author id in the Semantic Scholar database corresponding to
            the argument of "author_from_dblp"
    """

    if len(tidy_info)==0:
        return
    else:
        dois = tidy_info['dois']
        for doi in dois:
            url_semantic = 'https://api.semanticscholar.org/v1/paper/' + doi
            response_titles = requests.get(url_semantic)
            data = response_titles.json()

            #it is possible we cannot find a paper with the doi provided
            if 'error' not in data:

                for author in data['authors']:
                    if author_from_dblp == author['name']:
                        # we set the author  ID
                        return author['authorId']


def get_paperIds(authorId):
    """
        We request the Semantic Scholar API, based on the authorId, in search
         of all the paper Ids

        Args:
            authorId (string): identifier of the author id in the Semantic Scholar API

        Returns:
            set_of_ids_of_papers (set): we return a set of identifiers of all the papers
            of the author in the Semantic Scholar database
    """
    print('--------------------------------\n')
    print('authorId===> ' + str(authorId))
    print('--------------------------------\n')


    paperIds=[]
    url_semantic_by_author = 'https://api.semanticscholar.org/v1/author/'+authorId
    response = requests.get(url_semantic_by_author)
    print('STATUS CODE --->' + str(response.status_code) + "\n")

    data = response.json()
    paperIds.extend([paper['paperId'] for paper in data['papers']])
    return paperIds


def set_topics_from_author(paperIds, author_dict, publication_dict_list):
    """
        We request the Semantic Scholar API ,taking into account all the papersIds.
        For each of those papers we its topics.

        Args:
            paperIds (set): identifiers of all the papers in the Semantic Scholar database

        Returns:
            set_of_topics (set):  we return the set of idientifiers of each topic
    """
    topics = set()
    author_dict['topics'] = []

    cont =   0
    #papeIds2 = []
    #papeIds2.append('fa9a46fca1398da02735097e899f70460d240044')
    #papeIds2.append('ee556bf1cb23e300e723386b93351                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             007e1a50594')
    #papeIds2.append('56d04117a9a441e9a95d9a825782a41900247b6b')

    #we iterate over each paperId
    for paperId in paperIds:

        urlPaper = 'https://api.semanticscholar.org/v1/paper/'+paperId
        response = requests.get(urlPaper)

        # We might not find the paper corresponding to the code provided
        if response.status_code == SUCCESS():
            data = response.json()
            publication_dict={}
            publication_dict['_id'] = data['paperId']
            publication_dict['title'] = data['title']

            author_ids = []
            # for each paperId, we get its authorsId
            for author in data['authors']:
                author_ids.append(author['authorId'])
            publication_dict['author_ids'] = author_ids

            #for each paper we get its topics taking into account it may be repeated
            for topic in data['topics']:
                topics.add(topic['topic'])
            publication_dict['topics'] = list(topics)
            publication_dict_list.append(publication_dict)
            author_dict['topics'] = list(set(author_dict['topics']) | topics)
        cont = cont + 1
    return



def is_pdf_file(file):
    """
        We chech the name of the file to know whether a paper is a pdf file

        Args:
            file (string): the url of the file

        Returns:
            (boolean):  we return whether the file is a pdf file
    """
    return (file[len(file)-4:(len(file))])=='.pdf'


def tidy_info_from_teacher(best_coincidence):
    """
        We request the DBLP api, in search of the doi of the first title found, based on
        the name of the author od the argument

        Args:
            best_coincidence (string): name of the author

        Returns:
            tidy_info_from_author(map): we fulfill the map structure with necessary information:

    """

    url = 'http://dblp.org/search/publ/api'
    response = requests.get(url, params={'q': best_coincidence, 'format': 'json'})
    data = response.json()

    list_of_pdf_articles=[]
    list_of_articles=[]

    list_of_dois_from_articles = []
    list_of_titles = {}
    tidy_info_from_author = {}
    # we take the first title of that author
    if data['result']['hits']['@total'] != '0':
        for author in data['result']['hits']['hit']:
            if best_coincidence in author['info']['authors']['author']:
                if 'doi' in author['info'].keys():
                    list_of_dois_from_articles.append(author['info']['doi'])
                if 'ee' in author['info'].keys():

                    if is_pdf_file(author['info']['ee']) and not len(list_of_pdf_articles)>MAX_NUMBER_OF_ARTICLES():
                        list_of_pdf_articles.append(author['info']['ee'])
                        list_of_titles[author['info']['ee']]= author['info']['title'].replace(' ','-').replace('.','')
                    else:
                        list_of_articles.append(author['info']['ee'])

        tidy_info_from_author['articles'] = list_of_articles
        tidy_info_from_author['pdf_articles'] = list_of_pdf_articles
        tidy_info_from_author['titles'] = list_of_titles
        tidy_info_from_author['dois'] = list_of_dois_from_articles
    return tidy_info_from_author

def get_teachers():
    """
        We request the name of the teachers shown in the master's degree website

        Args:

        Returns:
            nombres(list): name of the teachers

    """
    page = requests.get("http://www.masterdatascience.es/equipo/")
    soup = BeautifulSoup(page.content, 'html.parser')
    nombres = [directors.text.split('-')[0].rstrip() for directors in soup.findAll(attrs={"class": "title margin-clear"})] \
              + [teacher.text for teacher in soup.findAll(attrs={"class": "small_white"})]
    return nombres


def get_file_name(url):

    value = search('https://www.semanticscholar.org/paper/(.+)/', url)
    if value is not None:
        value = value.group(1)
    return value

def get_papers(teacher, tidy_info):
    directorio = './' + unidecode.unidecode(teacher).replace(" ", "") + "/"

    if not os.path.exists(directorio):
        os.makedirs(directorio)

    for pdf in tidy_info['pdf_articles']:
        r = requests.get(pdf)
        directorio = './'+unidecode.unidecode(teacher).replace(" " ,"")+ "/"
        titulo = tidy_info['titles'][pdf]+".pdf"


        with open(directorio+titulo, "wb") as code:
            code.write(r.content)






def get_papers1(teacher, tidy_info, authorId):
    directorio = './' + unidecode.unidecode(teacher).replace(" ", "") + "/"

    if not os.path.exists(directorio):
        os.makedirs(directorio)

    url_semantic_by_author = 'https://api.semanticscholar.org/v1/author/'+authorId
    response = requests.get(url_semantic_by_author)
    print('STATUS CODE --->' + str(response.status_code) + "\n")

    data = response.json()
    #for article in tidy_info['articles']:
    for article in data['papers']:

        page = requests.get(article['url'])
        soup = BeautifulSoup(page.content, 'html.parser')

        """recogemmos el contenido de ese pdf en concreto"""
        try:
            pdf_url = soup.find(attrs={"name": "citation_pdf_url"})['content']
            if is_pdf_file(pdf_url):
                # Copy a network object to a local file
                # urllib.request.urlretrieve(pdf_url, "./papers2/fichero_prueba.pdf")
                titulo = unidecode.unidecode(article['title']).replace(" ", "")+".pdf"
                r = requests.get(pdf_url)
                with open(directorio + titulo, "wb") as code:
                    code.write(r.content)
        except:
            pass


"""def get_papers(teacher, tidy_info):

    for pdf in tidy_info['pdf_articles']:
        r = requests.get(pdf)
        # open method to open a file on your system and write the
        nombre  = unidecode.unidecode(teacher).replace(" " ,"")
        titulo = tidy_info['titles'][pdf]
        todo = "./"+nombre+"/"+titulo
        with open("./" + unidecode.unidecode(teacher).replace(" " ,"")+ "/" + tidy_info['titles'][pdf]+".pdf", "wb") as code:
            code.write(r.content)"""


def get_paper(teacher):

    """con la  petición de uno de los autorees"""
    page = requests.get("https://www.semanticscholar.org/paper/Identifying-Relations-for-Open-Information-Fader-Soderland/0796f6cd7f0403a854d67d525e9b32af3b277331")
    soup = BeautifulSoup(page.content, 'html.parser')

    """recogemmos el contenido de ese pdf en concreto"""
    pdf_url = soup.find(attrs={"name": "citation_pdf_url"})['content']


    # Copy a network object to a local file
    #urllib.request.urlretrieve(pdf_url, "./papers2/fichero_prueba.pdf")

    r = requests.get(pdf_url)
    # open method to open a file on your system and write the contents
    with open("./"+teacher+"/"+get_file_name(pdf_url)+".pdf", "wb") as code:
        code.write(r.content)


def get_all_paperIds(authorId,author_dict):
    """
        We request the Semantic Scholar API, based on the authorId, in search
         of all the paper Ids

        Args:
            authorId (string): identifier of the author id in the Semantic Scholar API

        Returns:
            set_of_ids_of_papers (set): we return a set of identifiers of all the papers
            of the author in the Semantic Scholar database
    """
    paperIds=[]
    url_semantic_by_author = 'https://api.semanticscholar.org/v1/author/'+authorId
    response = requests.get(url_semantic_by_author)
    data = response.json()

    for paper in data['papers']:
        paperIds.append(paper['paperId'])
    author_dict['publications'] = paperIds
    return paperIds


def set_info_from_author(tidy_info, author_dict, author_id, best_coincidence):
    author_dict['_id'] = author_id
    author_dict['name'] = best_coincidence
    ids = get_paperIds(author_id)
    author_dict['publications'] = ids
    author_dict['pdf_articles'] = tidy_info['pdf_articles']
    author_dict['articles'] = tidy_info['articles']
    return author_dict


'''
    Remove duplicate elements from list
    This method is necessay since the API returns repeated publications in the same request
'''
def removeDuplicates(listofElements):
    # Create an empty list to store unique elements
    uniqueList = []
    set_of_ids =set()

    # Iterate over the original list and for each element
    # add it to uniqueList, if its not already there.
    for elem in listofElements:
        if elem['_id'] not in set_of_ids:
            uniqueList.append(elem)
            set_of_ids.add(elem['_id'])
            # Return the list of unique elements
        else:
            print('****** ELEMENTO QUE SE REPITE ************\n')
            print('id ----> '+elem['_id'])
    return uniqueList

def main():
    start_time = time.time()
    url_connection = "mongodb://localhost"
    connection = pymongo.MongoClient(url_connection)
    db = connection.authorAndPublicationData

    # we create the collectiions of our data
    collection_authors = db.authors
    collection_publications = db.publications
    collection_authors.drop()
    collection_publications.drop()

    teachers = get_teachers()
    #teachers = ['Belén Vela Sánchez']
    set_of_ids =  set()
    first_iteration = True
    list = []
    for teacher in teachers:
        print('PROCESSINB AUTHOR----------->  '+teacher+ "\n")
        best_coincidence = get_coincidence_from_dblp(teacher)
        tidy_info = tidy_info_from_teacher(best_coincidence)
        author_dict = {}

        #LLamamos a la api de semantic scholar con el DOI del título
        author_id = get_author_id(best_coincidence,tidy_info)

        if author_id:
            # buscar por cada uno de esos Ids
            set_info_from_author(tidy_info, author_dict, author_id, best_coincidence)
            publication_dict_list=[]
            set_topics_from_author(author_dict['publications'], author_dict, publication_dict_list)
            list = list + publication_dict_list
            collection_authors.insert(author_dict)
            #get_papers1(teacher, tidy_info, author_id)
    if len(list) > 0:
        publication_dict_list = removeDuplicates(list)
        collection_publications.insert(publication_dict_list)

    print("The execution took: {0:0.2f} seconds".format(time.time() - start_time))
# this is the standard boilerplate that calls the main() function
if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()