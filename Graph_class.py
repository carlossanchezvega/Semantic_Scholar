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


class Graph_class:
    def __init__(self, output_json_name, teacher, collection_authors, collection_publications):
        self.output_json_name = output_json_name
        self.teacher = teacher
        self.collection_authors = collection_authors
        self.collection_publications = collection_publications



    def create_output_file(self, json_path, dic):
        """
            Dumps the content from "dic" to the path of "json_path"
            Args:
                json_path (str): path where we want out json to be stored
                dic: dic with all the information about the author with the proper format to be sored in a json

            Returns:
                list(dict): nodes with the relevant information about the author
        """

        with open(json_path, 'w') as outfile:
            json.dump(dic, outfile, cls=JSONEncoder, indent=4)



    def clean_authors(self, nodes):

        """
            Clean a list of nodes with information about authors
            Args:
                nodes list(dict): list of nodes of information about authors
            Returns:
                list(dict): nodes with the relevant information about the author
        """

        list_of_authors = []
        for node in nodes:
            author={}
            author['id']= node['_id']
            author['type']= 'author'
            author['name']= node['name']
            author['reputation']= node['reputation']
            author['size']= self.rescale_author(node['reputation'])
            author['url'] = 'https://www.semanticscholar.org/author/' +  author['id']
            list_of_authors.append(author)
        return list_of_authors



    def clean_publications(self, nodes):
        """
            Clean a list of nodes with information about publications
            Args:
                nodes list(dict): list of nodes of information about publications
            Returns:
                list(dict): nodes with the relevant information about the publications
        """
        list_of_publications = []
        for node in nodes:
            publication ={}
            publication['id']= node['_id']
            publication['type']= 'publication'
            publication['name']= node['title']
            publication['reputation']= node['reputation']
            publication['size']= self.rescale_publication(node['reputation'])
            publication['url'] = 'https://www.semanticscholar.org/paper/' +  publication['id']
            list_of_publications.append(publication)
        return list_of_publications


    def rescale_publication(self, value, new_min = 40, new_max = 200):
        """
            Rescale the dimensions of the nodes of the graph (we might find publications with a noticeable relevance when
            comparing to other authors since he/she might have inspired other authors
            Args:
                nodes list(dict): list of nodes of information about authors
            Returns:
                float: dimensions of the node in pixels
        """
        old_min, old_max = 1.95, 445.6
        return (new_max - new_min) / (old_max - old_min) * (value - old_min) + new_min

    def rescale_author(self, value, new_min = 40, new_max = 200):
        """
            Rescale the dimensions of the nodes of the graph (we might find authors with a noticeable relevance when
            comparing to other authors since he/she might have inspired other authors
            Args:
                nodes list(dict): list of nodes of information about authors
            Returns:
                float: dimensions of the node in pixels
        """

        old_min, old_max = 0.4, 609.2
        return (new_max - new_min) / (old_max - old_min) * (value - old_min) + new_min


    def create_links(self,dict_nodes, authors):
        """
            Create the links between nodes (the relationships between the authors and the publications)
            Args:
                nodes list(dict): list of nodes of information about authors
            Returns:
                list(dict): list of links (source, target and weigh corresponding to each link
        """
        list_of_links = []
        list_node_keys = list(dict_nodes.keys())
        for author in authors:
            for publication in author['publications'] :
                link =  {}
                link['source'] = list_node_keys.index(author['_id'])
                link['target'] = list_node_keys.index(publication)
                link['weight'] = 1
                list_of_links.append(link)
        return list_of_links

    def create_graph(self):
        """
            Represent a graph corresponding to the queried author and his/her publications
            Args:
            Returns:
        """

        author_dict = self.collection_authors.find_one({"name": self.teacher})
        ids_coauthors = list(set(list(itertools.chain.from_iterable([coauthor['author_ids'] for coauthor in
                        (self.collection_publications.find({"_id": {"$in": author_dict['publications']}},{'author_ids'}))]))))

        authors = list((self.collection_authors.find({"_id": {"$in": list(set(list(itertools.chain.from_iterable([coauthor['author_ids']
        for coauthor in (self.collection_publications.find({"_id": {"$in": author_dict['publications']}},{'author_ids'}))]))))}})))
        publications =list(self.collection_publications.find({"_id": {"$in": list(set(list(itertools.chain.from_iterable([author['publications']
                    for author in(self.collection_authors.find({"_id": {"$in": ids_coauthors}}))]))))}}))

        cleaned_authors = self.clean_authors(authors)
        cleaned_publications = self.clean_publications(publications)

        nodes = cleaned_authors + cleaned_publications
        dict_nodes  = { value["id"]: value for value in nodes }

        final_dict = {}
        final_dict["directed"] =False
        final_dict["graph"] = {}
        final_dict["nodes"] = nodes

        final_dict["links"] = self.create_links(dict_nodes,authors)
        final_dict["multigraph"] = False
        self.create_output_file(self.output_json_name, final_dict)

        webbrowser.open('http://localhost:63342/Semantic_Scholar/betweenness_all_nodes_reputation.html', new=2)


