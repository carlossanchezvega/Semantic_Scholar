import json
import pymongo
import time


""" Inserts all records of the file of the path """
def insert_collection (collection,json_path):
    page = open(json_path, 'r')
    parsed = json.loads(page.read())
    for item in parsed:
        collection.insert(item)

""" Connects to the database and manage the collections to be stored """
def insert_all_records(url_connection,json_input_path_authors, json_input_path_publications ):
    connection = pymongo.MongoClient(url_connection)
    db=connection.authorAndPublicationData
    collection_authors = db.authors
    insert_collection(collection_authors, json_input_path_authors)
    collection_publications = db.publications
    insert_collection(collection_publications, json_input_path_publications)

if __name__ == "__main__":
    url_connection = "mongodb://localhost"
    json_input_path_authors = "./FicherosBBDD/JSON/authors.json"
    json_input_path_publications = "./FicherosBBDD/JSON/publications.json"
    start_time = time.time(url_connection,json_input_path_authors,json_input_path_publications)
    insert_all_records(url_connection,json_input_path_authors, json_input_path_publications )
    print("The import to Mongo took: {0:0.2f} seconds".format(time.time() - start_time))