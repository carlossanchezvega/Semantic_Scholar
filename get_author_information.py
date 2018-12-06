import pymongo
import sys, requests
import time

import nltk
from CheckBestAuthorSimilarity import CheckBestAuthorSimilarity


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
    if len(data['result']['hits'])==0:
        return data['result']['hits']['hit'][0]['info']['author']
    else:
        #best_concidence = data['result']['hits']['hit'][0]['info']['author']
        best_concidence = data['result']['query']

        count = 1;

        # we go over the author list from the second author on, calculating best similarity
        for x in range(1, len(data['result']['hits']['hit'])):
            check_similarity = CheckBestAuthorSimilarity(best_concidence, data['result']['hits']['hit'][x]['info']['author'])
            new_similarity = check_similarity.getSimilarity()

            # in case the name of the new author has better similarity
            if best_similarity < new_similarity:
                best_concidence = data['result']['hits']['hit'][x]['info']['author']
                best_similarity = new_similarity
        return best_concidence



def get_author_from_dblp():
    """
        We request the dblp api in search of the exact name of the author in dblp, based
        on the author introduced by the user

        Args:

        Returns:
            best_coincidence: The name of the author, in the database of dblp, which fits
            the best with the name introduced by the user
    """

    url = 'http://dblp.org/search/author/api'
    response = requests.get(url, params={'q':'Anastassiou', 'format': 'json'})
    data = response.json()
    best_coincidence = get_best_coincidence(data)
    return best_coincidence


def get_author_id(author_from_dblp, title_doi):
    """
        We request, the Semantic Scholar api, the article with the "doi" received.
        Once received, we compare the name of the author to the authors of that article
        (the author ID we are looking for is by the author name)

        Args:
            author_from_dblp (string): name of the author we are looking for
            doi (string: identifier of the article in the Semantic Scholar Api

        Returns:
            author_id: The author id in the Semantic Scholar database corresponding to
            the argument of "author_from_dblp"
    """

    url_semantic = 'https://api.semanticscholar.org/v1/paper/' + title_doi
    response_titles = requests.get(url_semantic)
    data = response_titles.json()

    for author in data['authors']:
        if author_from_dblp == author['name']:
            return author['authorId']


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
    author_dict['_id'] = data['authorId']
    author_dict['name'] = data['name']

    for paper in data['papers']:
        paperIds.append(paper['paperId'])
    author_dict['publications'] = paperIds
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

    #we iterate over each paperId
    for paperId in paperIds:

        urlPaper = 'https://api.semanticscholar.org/v1/paper/'+paperId
        response = requests.get(urlPaper)
        data = response.json()
        publication_dict={}
        publication_dict['_id'] = data['paperId']
        publication_dict['title'] = data['title']

        author_ids = []
        # for each paperId, we get its authorsId
        for author in data['authors']:
            author_ids.append(author['authorId'])
        publication_dict['author_ids'] = author_ids

        #for each paper we get its topics taking into account that the may be repeated
        for topic in data['topics']:
            topics.add(topic['topic'])
        publication_dict['topics'] = list(topics)
        publication_dict_list.append(publication_dict)
        author_dict['topics'] = list(set(author_dict['topics']) | topics)

    return

def get_doi_from_publi_dblp(best_coincidence):
    """
        We request the DBLP api, in search of the doi of the first title found, based on
        the name of the author od the argument

        Args:
            best_coincidence (string): name of the author

        Returns:
            strimg: we return the doi of the title
    """

    url = 'http://dblp.org/search/publ/api'
    #Hacemos una busqueda por ese autor
    response = requests.get(url, params={'q': best_coincidence, 'format': 'json'})
    data = response.json()

    # cogemos el primer título que encontremos para ese autor
    return data['result']['hits']['hit'][0]['info']['doi']


def main():
    start_time = time.time()
    best_coincidence = get_author_from_dblp()

    # cogemos el primer título que encontremos para ese autor
    title_doi = get_doi_from_publi_dblp(best_coincidence)

    #LLamamos a la api de semantic scholar con el DOI del título
    author_id = get_author_id(best_coincidence,title_doi )

    author_dict = {}
    # recogemos los identificadores de los paper en Semantic Scholar, para
    # buscar por cada uno de esos Ids
    paperIds = get_all_paperIds(author_id, author_dict)

    publication_dict_list=[]
    set_topics_from_author(paperIds, author_dict, publication_dict_list)

    url_connection = "mongodb://localhost"
    connection = pymongo.MongoClient(url_connection)
    db = connection.authorAndPublicationData
    collection_authors = db.authors
    collection_authors.insert(author_dict)

    collection_publications = db.publications
    collection_publications.insert(publication_dict_list)




    print("The execution took: {0:0.2f} seconds".format(time.time() - start_time))
# this is the standard boilerplate that calls the main() function
if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()