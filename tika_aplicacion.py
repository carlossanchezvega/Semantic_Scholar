import pymongo
import sys, requests
import time
from bs4 import BeautifulSoup
from re import search
import unidecode
import os
import itertools
from threading import Thread
#from threading import Thread
#import bson
import logging
from datetime import datetime
import statistics


import nltk

# TENGO QUE EJECUTAR ESTA

from CheckBestAuthorSimilarity import CheckBestAuthorSimilarity

def MAX_NUMBER_OF_ARTICLES():
    return 5

def SUCCESS():
    return 200

def COEF_NUM_PAPERS():
    return 0.4

def COEF_INFLUENCIAL_CITATIONS():
    return 0.1

def COEF_SENIORITY():
    return 0.2

def COEF_CITATIONS():
    return 0.3

def COEF_AVG_REPUTATION_AUTHOR():
    return 0.5

def COEF_CITATIONS_ARTICLE_REPUTATION():
    return 0.5


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


def get_paperIds(authorId, author_dict):
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
    url_semantic_by_author = 'https://api.semanticscholar.org/v1/author/'+authorId
    response = requests.get(url_semantic_by_author)
    print('STATUS CODE --->' + str(response.status_code) + "\n")
    data = response.json()
    author_dict['name'] =  data['name']
    return [paper['paperId'] for paper in data['papers']]

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
            publication_dict['year'] = data['year']
            publication_dict['citations'] = len(data['citations'])
            publication_dict['influentialCitationCount'] = data['influentialCitationCount']
            publication_dict['author_ids'] = [author['authorId'] for author in data['authors']]
            topics = [topic['topic'] for topic in data['topics']]
            publication_dict['topics'] = topics
            publication_dict_list.append(publication_dict)
            author_dict['topics'] = list(set(author_dict['topics']) | set(topics))

    return

##TODO aqui es donde tengo que controlar la seniority
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
    list_of_titles=[]


    list_of_dois_from_articles = []
    list_of_titles = []
    tidy_info_from_author = {}
        # we take the first title of that author
    if data['result']['hits']['@total'] != '0':
        for author in data['result']['hits']['hit']:
            if best_coincidence in author['info']['authors']['author']:

                if 'doi' in author['info'].keys():
                    list_of_dois_from_articles.append(author['info']['doi'])
                if 'ee' in author['info'].keys():
                    list_of_articles.append(author['info']['ee'])
                    list_of_titles.append(author['info']['title'])

        tidy_info_from_author['articles'] = list_of_articles
        tidy_info_from_author['pdf_articles'] = list_of_pdf_articles
        tidy_info_from_author['titles'] = list_of_titles
        tidy_info_from_author['dois'] = list_of_dois_from_articles
    return tidy_info_from_author



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
    return list(set([paper['paperId'] for paper in data['papers']]))



def set_info_from_author(isAuthor,tidy_info, author_dict, author_id, best_coincidence):
    author_dict['_id'] = author_id
    ids = get_paperIds(author_id, author_dict)
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



def set_total_author_info(isAuthor,best_coincidence, tidy_info,author_dict,publications, collection_authors):
    #LLamamos a la api de semantic scholar con el DOI del título
    if isAuthor:
        author_id = get_author_id(best_coincidence,tidy_info)
    else:
        author_id = best_coincidence

    if author_id:
        # buscar por cada uno de esos Ids
        set_info_from_author(isAuthor,tidy_info, author_dict, author_id, best_coincidence)
        publication_dict_list=[]
        set_topics_from_author(author_dict['publications'], author_dict, publication_dict_list)
        list_of_publications = publications + publication_dict_list
        collection_authors.insert(author_dict)
        return list_of_publications

def get_seniority(years):
    return datetime.now().year - years.sort()[:1]



def get_author_reputation (name,collection_authors):

    author = collection_authors.find_one({"name":  name})

    return COEF_NUM_PAPERS()*author['publications'] + COEF_INFLUENCIAL_CITATIONS() * author['citations'] + \
           COEF_INFLUENCIAL_CITATIONS()*author['influentialCitationCount'] + COEF_SENIORITY()*get_seniority()

def get_paper_reputation(id, collection_authors, collection_publications):
    paper = collection_publications.find_one({"_id": id})
    paper_reputations=[]
    for author in paper['authorIds']:
        paper_reputations.append(get_author_reputation(id,collection_authors))
    statistics.mean(paper_reputations)
    paper_reputation = COEF_CITATIONS_ARTICLE_REPUTATION() * paper['citations'] + \
                       COEF_AVG_REPUTATION_AUTHOR() * statistics.mean(paper_reputations)
    return paper_reputation

def main():


    start_time = time.time()

    url_connection = "mongodb://localhost"
    connection = pymongo.MongoClient(url_connection)
    db = connection.authorAndPublicationData
    collection_authors = db.authors
    collection_publications = db.publications
    #db.collection_authors.drop()
    #db.publications.drop()
    # db.authors.drop()

    #teachers = get_teachers()
    teacher = "Felipe Ortega"
    #teachers = ['Belén Vela Sánchez', 'Felipe Ortega', 'Isaac Martín de Diego']
    best_coincidence = get_coincidence_from_dblp(teacher)

    if collection_authors.find_one({"name": 'perp'}):
        print('EXISTEEEEEEEEE\n')
    else:
        print('NO EXISTEEEEEE\n')

        set_of_ids =  set()
        first_iteration = True
        publication_dict_list = []
        print('PROCESSINB AUTHOR----------->  '+teacher+ "\n")
        author_dict = {}
        tidy_info=tidy_info_from_teacher(best_coincidence)
        publication_dict_list= set_total_author_info(True,teacher, tidy_info,author_dict,publication_dict_list, collection_authors)

    ###        #ids_coauthors = [coauthor['author_ids'] for coauthor in publication_dict_list]
        ids_coauthors = list(set(list(itertools.chain.from_iterable([coauthor['author_ids']
                                                                            for coauthor in publication_dict_list if teacher != coauthor['author_ids']]))))
        ids_coauthors = ['1800967']
        for teacher in ids_coauthors:
            publication_dict_list= set_total_author_info(False,teacher, tidy_info,author_dict, publication_dict_list, collection_authors)
            print('Hola')

        if len(publication_dict_list) > 0:
            publication_dict_list = removeDuplicates(publication_dict_list)
            collection_publications.insert(publication_dict_list)

    print("The execution took: {0:0.2f} seconds".format(time.time() - start_time))
# this is the standard boilerplate that calls the main() function
if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()