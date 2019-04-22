import webbrowser

import pymongo
import time
import json
from bson import ObjectId
import itertools

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


"""
Dumps the content from "dic" to the path of "json_path"
"""
def create_output_file(json_path, dic):
    with open(json_path, 'w') as outfile:
        json.dump(dic, outfile, cls=JSONEncoder, indent=4)



def clean_authors(nodes):
    list_of_authors = []
    for node in nodes:
        author={}
        author['id']= node['_id']
        author['type']= 'author'
        author['name']= node['name']
        author['reputation']= node['reputation']
        author['size']= rescale_author(node['reputation'])
        author['url'] = 'https://www.semanticscholar.org/author/' +  author['id']
        list_of_authors.append(author)
    return list_of_authors

def rescale_publication(value, new_min = 40, new_max = 200):

    #old_min, old_max = min(values), max(values)
    old_min, old_max = 1.95, 445.6
    return (new_max - new_min) / (old_max - old_min) * (value - old_min) + new_min

def rescale_author(value, new_min = 40, new_max = 200):

    #old_min, old_max = min(values), max(values)
    old_min, old_max = 0.4, 609.2
    return (new_max - new_min) / (old_max - old_min) * (value - old_min) + new_min

def clean_publications(nodes):
    list_of_publications = []
    for node in nodes:
        publication ={}
        publication['id']= node['_id']
        publication['type']= 'publication'
        publication['name']= node['title']
        publication['reputation']= node['reputation']
        publication['size']= rescale_publication(node['reputation'])
        publication['url'] = 'https://www.semanticscholar.org/paper/' +  publication['id']
        list_of_publications.append(publication)
    return list_of_publications

#def create_links(authors, publications):
#    for
def create_links(dict_nodes, authors):
    list_of_links = []
    list_node_keys = list(dict_nodes.keys())
    list(dict_nodes.keys()).index("1697222")
    for author in authors:
        for publication in author['publications'] :
            link =  {}
            link['source'] = list_node_keys.index(author['_id'])
            link['target'] = list_node_keys.index(publication)
            link['weight'] = 1
            list_of_links.append(link)
    return list_of_links

def main():

    url_connection = "mongodb://localhost"
    connection = pymongo.MongoClient(url_connection)
    db = connection.authorAndPublicationData
    collection_authors = db.authors
    collection_publications = db.publications


    teacher = "Alberto Fernández-Isabel"
    #best_coincidence = get_coincidence_from_dblp(teacher.strip())
    # result = collection_authors.update({"_id": "37318854"}, {"$set": {"patatas": "fritas"}})

    author_dict = collection_authors.find_one({"name": 'Alberto Fernández-Isabel'})
    ids_coauthors = list(set(list(itertools.chain.from_iterable([coauthor['author_ids'] for coauthor in
                    (collection_publications.find({"_id": {"$in": author_dict['publications']}},{'author_ids'}))]))))
    authors = list((collection_authors.find({"_id": {"$in": ids_coauthors}})))

    authors = list((collection_authors.find({"_id": {"$in": list(set(list(itertools.chain.from_iterable([coauthor['author_ids']
    for coauthor in (collection_publications.find({"_id": {"$in": author_dict['publications']}},{'author_ids'}))]))))}})))

    ids_publications = list(set(list(itertools.chain.from_iterable([author['publications'] for author in
                        (collection_authors.find({"_id": {"$in": ids_coauthors}}))]))))

    publications =list(collection_publications.find({"_id": {"$in": ids_publications}}))
    publications =list(collection_publications.find({"_id": {"$in": list(set(list(itertools.chain.from_iterable([author['publications']
                for author in(collection_authors.find({"_id": {"$in": ids_coauthors}}))]))))}}))

    cleaned_authors = clean_authors(authors)
    cleaned_publications = clean_publications(publications)

    nodes = cleaned_authors + cleaned_publications
    dict_nodes  = { value["id"]: value for value in nodes }

    final_dict = {}
    final_dict["directed"] =False
    final_dict["graph"] = {}
    final_dict["nodes"] = nodes

    final_dict["links"] = create_links(dict_nodes,authors)
    final_dict["multigraph"] = False
    create_output_file(json_all_info, final_dict)

    webbrowser.open('http://localhost:63342/Semantic_Scholar/betweenness_all_nodes_reputation.html', new=2)

    #create_output_file(json_all_info, list(collection_authors.find()))
    print('HOLA')

if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    json_all_info = "data/allInfo.json"
    main()
