import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
import string
from CheckBestAuthorSimilarity import CheckBestAuthorSimilarity
import pymongo
import sys, requests
import time
from bs4 import BeautifulSoup
from re import search
import unidecode
import os
import itertools
from threading import Thread
# from threading import Thread
# import bson
import logging
from datetime import datetime
import statistics
from bson.objectid import ObjectId
import pandas as pd
from bson import CodecOptions
from bson.raw_bson import RawBSONDocument
import six

import nltk

class GetInfo:
    def __init__(self, url_connection,teacher, collection_authors, collection_publications):
        self.url_connection = url_connection
        self.teacher = teacher
        self.collection_authors = collection_authors
        self.collection_publications = collection_publications


    def MAX_NUMBER_OF_ARTICLES(self):
        return 5


    def SUCCESS(self):
        return 200


    def FAILURE(code):
        return code!=200


    def COEF_NUM_PAPERS(self):
        return 0.4


    def COEF_INFLUENTIAL_CITATIONS(self):
        return 0.1


    def COEF_SENIORITY(self):
        return 0.2


    def COEF_CITATIONS(self):
        return 0.3


    def COEF_AVG_REPUTATION_AUTHOR(self):
        return 0.5


    def COEF_CITATIONS_ARTICLE_REPUTATION(self):
        return 0.5


    def get_best_coincidence(self, data):
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
        if data['result']['hits']['@total'] == '0':
            return data['result']['query']
        else:
            # best_concidence = data['result']['hits']['hit'][0]['info']['author']
            best_concidence = data['result']['query']

            # we go over the author list from the second author on, calculating best similarity
            for x in range(0, len(data['result']['hits']['hit'])):
                check_similarity = CheckBestAuthorSimilarity(data['result']['query'],
                                                             data['result']['hits']['hit'][x]['info']['author'])
                new_similarity = check_similarity.getSimilarity()

                # in case the name of the new author has better similarity
                if best_similarity < new_similarity:
                    best_concidence = data['result']['hits']['hit'][x]['info']['author']
                    best_similarity = new_similarity
            return best_concidence


    def get_coincidence_from_dblp(self, teacher):
        """
            We request the dblp api in search of the exact name of the author in dblp, based
            on the author introduced by the user

            Args:

            Returns:
                best_coincidence: The name of the author, in the database of dblp, which fits
                the best with the name introduced by the user
        """

        url = 'http://dblp.org/search/author/api'
        response = requests.get(url, params={'q': teacher, 'format': 'json'})
        data = response.json()
        best_coincidence = self.get_best_coincidence(data)
        return best_coincidence


    def get_author_id(self, author_from_dblp, tidy_info):
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

        if len(tidy_info) == 0:
            return
        else:
            dois = tidy_info['dois']
        for doi in dois:
            url_semantic = 'https://api.semanticscholar.org/v1/paper/' + doi
            response_titles = requests.get(url_semantic)
            data = response_titles.json()

            # it is possible we cannot find a paper with the doi provided
            if 'error' not in data:

                for author in data['authors']:
                    if author_from_dblp == author['name']:
                        # we set the author  ID
                        return author['authorId']


    def get_paperIds(self, authorId, author_dict):
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


        url_semantic_by_author = 'https://api.semanticscholar.org/v1/author/' + authorId


        response = requests.get(url_semantic_by_author)
        if response.status_code == self.SUCCESS():
            print('STATUS CODE --->' + str(response.status_code) + "\n")
            data = response.json()
            author_dict['name'] = data['name']
            author_dict['_id'] = data['authorId']
            author_dict['titles'] = [paper['title'] for paper in data['papers']]
        else:
            return

    def set_topics_from_author(self, paperIds, author_dict, collection_publications):
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
        author_dict['topicsId'] = []

        # we iterate over each paperId
        for paperId in paperIds:

            urlPaper = 'https://api.semanticscholar.org/v1/paper/' + paperId
            response = requests.get(urlPaper)

            # We might not find the paper corresponding to the code provided
            if response.status_code == self.SUCCESS():
                data = response.json()
                publication_dict = {}
                publication_dict['_id'] = data['paperId']
                publication_dict['title'] = data['title']
                publication_dict['year'] = data['year']
                publication_dict['citations'] = len(data['citations'])
                publication_dict['influentialCitationCount'] = data['influentialCitationCount']
                publication_dict['author_ids'] = [author['authorId'] for author in data['authors']]
                topics = [topic['topic'] for topic in data['topics']]
                topicsId = [topic['topicId'] for topic in data['topics']]
                publication_dict['topics'] = topics
                publication_dict['topicsId'] = topicsId
                collection_publications.replace_one ({"_id":publication_dict['_id']}, publication_dict, upsert=True)
                author_dict['topics'] = list(set(author_dict['topics']) | set(topics))
                author_dict['topicsId'] = list(set(author_dict['topicsId']) | set(topicsId))
        return


    def get_dois_from_dblp(self, best_coincidence):
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
        list_of_dois_from_articles = []
        tidy_info_from_author = {}
        # we take the first title of that author
        if data['result']['hits']['@total'] != '0':
            for author in data['result']['hits']['hit']:
                if best_coincidence in author['info']['authors']['author']:
                    if 'doi' in author['info'].keys():
                        list_of_dois_from_articles.append(author['info']['doi'])
            tidy_info_from_author['dois'] = list_of_dois_from_articles
        return tidy_info_from_author


    def get_all_paperIds(self, authorId):
        """
            We request the Semantic Scholar API, based on the authorId, in search
             of all the paper Ids

            Args:
                authorId (string): identifier of the author id in the Semantic Scholar API

            Returns:
                set_of_ids_of_papers (set): we return a set of identifiers of all the papers
                of the author in the Semantic Scholar database
        """
        url_semantic_by_author = 'https://api.semanticscholar.org/v1/author/' + authorId
        response = requests.get(url_semantic_by_author)
        data = response.json()
        return list(set([paper['paperId'] for paper in data['papers']]))


    def set_info_from_author(self, author_dict, author_id, collection_publications):
        """
            We set important information from a auhot

            Args:
                tidy_info (dict): variable where we get relevant information from
                author_dict (dict):variable where we set important information from "tidy_info"
                authorId (string): identifier of the author id in the Semantic Scholar API

            Returns:
                author_dict (set): variable containing relevant information for next steps in our calculations
        """
        print('--------------------------------\n')
        print('authorId===> ' + str(author_id))
        print('--------------------------------\n')


        url_semantic_by_author = 'https://api.semanticscholar.org/v1/author/' + author_id


        response = requests.get(url_semantic_by_author)
        if response.status_code == self.SUCCESS():
            print('STATUS CODE --->' + str(response.status_code) + "\n")
            data = response.json()
            author_dict['name'] = data['name']
            author_dict['_id'] = data['authorId']
            author_dict['publications'] = [paper['paperId'] for paper in data['papers']]
            author_dict['titles'] = [paper['title'] for paper in data['papers']]
            self.set_topics_from_author(author_dict['publications'], author_dict, collection_publications)
        return

    def removeDuplicates(self, listofElements):
        """
            Remove duplicate elements from list
            This method is necessay since the API returns repeated publications in the same request
            Args:

                listofElements (list): list of elements ready to be inserted in database

            Returns:
                uniqueList (lit): same list from argument but for duplicate values
        """

        # Create an empty list to store unique elements
        uniqueList = []
        set_of_ids = set()

        # Iterate over the original list and for each element
        # add it to uniqueList, if its not already there.
        for elem in listofElements:
            if elem['_id'] not in set_of_ids:
                uniqueList.append(elem)
                set_of_ids.add(elem['_id'])
                # Return the list of unique elements
            else:
                print('****** ELEMENTO QUE SE REPITE ************\n')
                print('id ----> ' + elem['_id'])
        return uniqueList


    def set_total_author_info(self, isAuthor, best_coincidence, dois, author_dict,  collection_authors, collection_publications):
        """
            Sets important information about and author and returns publications from that author
            Args:
                isAuthor (bool): variable to check whether we have to check author or coathor information
                best_coincidence (String): best coincidence according to the author requested
                tidy_info (dict): relevant information about our future calculation related with an author
                publications (list): list of all publications requested from all authors
                collection_authors (collection): where we store authors once processed to set important info
            Returns:
                list_of_publications (list):  returns a list of important information about an author
        """

        # LLamamos a la api de semantic scholar con el DOI del título
        if isAuthor:
            author_id = self.get_author_id(best_coincidence, dois)
        else:
            author_id = best_coincidence

        # if that author existed previously
        if author_id:
            # buscar por cada uno de esos Ids
            self.set_info_from_author(author_dict, author_id, collection_publications)
            collection_authors.replace_one ({"_id":author_dict['_id']}, author_dict, upsert=True)
            return


    def get_seniority(self, first_year_of_publication):
        """
            Gets the seniority corresponding to an author
            Args:
                first_year_of_publication (int): year when the author published the fist paper
            Returns:
                int: years from first paper
        """
        return datetime.now().year - first_year_of_publication


    def get_influencial_citation_count(self, publications):
        """
            Get the total sum of the influential citations count from the publications argument
            Args:
                publications (list): list of all the publications of an author
            Returns:
                int: total sum of the influential citations count from the publications argument
        """
        return sum([publication['influentialCitationCount'] for publication in publications])


    def get_citations(self, publications):
        """
            Get the number of citations of a publication
            Args:
                publications (list): list of all the publications of a paper
            Returns:
                int: total sum of the citations count from the publications argument
        """
        return sum([publication['citations'] for publication in publications])


    def get_author_reputation(self, author, collection_publications):
        """
            Gets an author reputations
            Args:
                author (dict): author whom we want to take reputation from
                collection_publications (collection): all the publications processed

            Returns:
                int: author reputation calculation
        """
        if author['_id']=='1895694':
            print('HOLA')
        publications = list(collection_publications.find({"_id": {"$in": author['publications']}}))
        return self.COEF_NUM_PAPERS() * len(author['publications']) + self.COEF_CITATIONS() * \
               self.get_citations(publications) + \
               self.COEF_INFLUENTIAL_CITATIONS() * self.get_influencial_citation_count(publications) + \
               self.COEF_SENIORITY() * self.get_seniority(sorted ([publication['year']
                                                for publication in publications if publication['year']])[0])


    def get_paper_reputation(self, publication, collection_authors):
        """
            Gets a paper reputation
            Args:
                publication (dict): publication whom we want to get reputation calculation from
                collection_authors (collection): all the authors processed

            Returns:
                int: publications reputation calculation
        """
        paper_reputations = []
        for author_id in publication['author_ids']:
            author = collection_authors.find_one({"_id": author_id})
            try:
                paper_reputations.append(author['reputation'])
            except:
                pass
            # paper_reputations.append(get_author_reputation(author,collection_authors))
        paper_reputation = self.COEF_CITATIONS_ARTICLE_REPUTATION() * publication['citations'] \
                           + self.COEF_AVG_REPUTATION_AUTHOR() * statistics.mean(paper_reputations)
        return paper_reputation


    def set_reputations(self, collection_authors, collection_publications):
        """
            Sets author and his/her paper reputations
            Args:
                collection_authors (dict): collection of all authors that has been processed and to be updated once
                                           reputation has been calculated
                collection_authors (collection): collection of all authors that has been processed and to be updated once
                                           reputation has been calculated

            Returns:
                int: publications reputation calculation
        """

        for author in list(collection_authors.find()):
            author_reputation = self.get_author_reputation(author, collection_publications)
            collection_authors.update_one({"_id": author['_id']}, {"$set": {"reputation": author_reputation}}, upsert=False)

        for publication in list(collection_publications.find()):
            publication_reputation = self.get_paper_reputation(publication, collection_authors)
            collection_publications.update_one({"_id": publication['_id']}, {"$set": {"reputation": publication_reputation}},
                                               upsert=False)


    def requestInfo(self):
        start_time = time.time()
        best_coincidence = self.get_coincidence_from_dblp(self.teacher.strip())

        if best_coincidence:
            # result = collection_authors.update({"_id": "37318854"}, {"$set": {"patatas": "fritas"}})

            if self.collection_authors.find_one({"name": best_coincidence}):
                print('EXISTEEEEEEEEE\n')
            else:
                print('NO EXISTEEEEEE\n')
                print('PROCESSINB AUTHOR----------->  ' + self.teacher + "\n")
                author_dict = {}
                dois = self.get_dois_from_dblp(best_coincidence)
                self.set_total_author_info(True, self.teacher, dois, author_dict,self.collection_authors, self.collection_publications)

                ids_coauthors = list(set(list(itertools.chain.from_iterable([coauthor['author_ids'] for coauthor in
                        (self.collection_publications.find({"_id": {"$in": author_dict['publications']}},{'author_ids'}))]))))

                #ids_coauthors = ['1800967']
                for teacher in ids_coauthors:
                    self.set_total_author_info(False, teacher, dois, author_dict,self.collection_authors, self.collection_publications)

                    self.set_reputations(self.collection_authors, self.collection_publications)

                print("The execution took: {0:0.2f} seconds".format(time.time() - start_time))
            return 0
        else:
            return 1


