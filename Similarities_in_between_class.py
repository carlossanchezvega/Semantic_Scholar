import io
import sys
import time

import pymongo

try:
    import tornado
except ImportError:
    raise RuntimeError("This example requires tornado.")
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.websocket
import itertools
import threading
import asyncio
import logging


from operator import itemgetter

from matplotlib.backends.backend_webagg_core import (
    FigureManagerWebAgg, new_figure_manager_given_figure)
from matplotlib.figure import Figure
import webbrowser

import numpy as np

import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import fetch_20newsgroups

twenty = fetch_20newsgroups()
from matplotlib import pyplot
import pylab
import os
import seaborn as sns;

sns.set()
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pylab
from sklearn import linear_model, manifold, decomposition, datasets
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial import distance


import numpy as np
from sklearn import datasets, manifold
from sklearn.metrics.pairwise import linear_kernel
from scipy import spatial
from sklearn.metrics import pairwise_distances
import matplotlib as mpl
import io
import logging

try:
    import tornado
except ImportError:
    raise RuntimeError("This example requires tornado.")
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.websocket
import logging
from colorlog import ColoredFormatter


class myThread(threading.Thread):
    def __init__(self,  option_selected, teacher, id, collection_authors, collection_publications,
                 max_number_to_plot):
        threading.Thread.__init__(self)

        self.option_selected = option_selected
        self.teacher = teacher
        self.collection_authors = collection_authors
        self.collection_publications = collection_publications
        self.max_number_to_plot = max_number_to_plot

        # We will be able to represent, at maximum, elements
        self.colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'r', 'g', 'b', 'c', 'm', 'y', 'k', 'r']
        self.markers = ['o', 'v', '^', '4', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X', '>']
        self.id = id
        logging.basicConfig(level=logging.DEBUG)
        self.log=logging


    def create_figure(self):
        """
        Creates a simple example figure.
        """

        fig = Figure(figsize=(20, 8))
        self.plot_figure(fig)
        return fig


    class MyApplication(tornado.web.Application):
        class MainPage(tornado.web.RequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                # The following is the content of the web page.  You would normally
                # generate this using some sort of template facility in your web
                # framework, but here we just use Python string formatting.

                self.html_content = """<html>
                                                  <head>
                                                    <!-- TODO: There should be a way to include all of the required javascript
                                                               and CSS so matplotlib can add to the set in the future if it
                                                               needs to. -->
                                                    <link rel="stylesheet" href="_static/css/page.css" type="text/css">
                                                    <link rel="stylesheet" href="_static/css/boilerplate.css" type="text/css" />
                                                    <link rel="stylesheet" href="_static/css/fbm.css" type="text/css" />
                                                    <link rel="stylesheet" href="_static/jquery-ui-1.12.1/jquery-ui.min.css" >
                                                    <script src="_static/jquery-ui-1.12.1/external/jquery/jquery.js"></script>
                                                    <script src="_static/jquery-ui-1.12.1/jquery-ui.min.js"></script>
                                                    <script src="mpl.js"></script>
    
                                                    <script>
                                                      /* This is a callback that is called when the user saves
                                                         (downloads) a file.  Its purpose is really to map from a
                                                         figure and file format to a url in the application. */
                                                      function ondownload(figure, format) {
                                                        window.open('download.' + format, '_blank');
                                                      };
    
                                                      $(document).ready(
                                                        function() {
                                                          /* It is up to the application to provide a websocket that the figure
                                                             will use to communicate to the server.  This websocket object can
                                                             also be a "fake" websocket that underneath multiplexes messages
                                                             from multiple figures, if necessary. */
                                                          var websocket_type = mpl.get_websocket_type();
                                                          var websocket = new websocket_type("%(ws_uri)sws");
    
                                                          // mpl.figure creates a new figure on the webpage.
                                                          var fig = new mpl.figure(
                                                              // A unique numeric identifier for the figure
                                                              %(fig_id)s,
                                                              // A websocket object (or something that behaves like one)
                                                              websocket,
                                                              // A function called when a file type is selected for download
                                                              ondownload,
                                                              // The HTML element in which to place the figure
                                                              $('div#figure'));
                                                        }
                                                      );
                                                    </script>
    
                                                    <title>matplotlib</title>
                                                  </head>
    
                                                  <body>
                                                    <div id="figure">
                                                    </div>
                                                  </body>
                                                </html>
                                                """

            def get(self):
                manager = self.application.manager
                ws_uri = "ws://{req.host}/".format(req=self.request)
                content = self.html_content % {
                    "ws_uri": ws_uri, "fig_id": manager.num}
                self.write(content)

        class MplJs(tornado.web.RequestHandler):
            """
            Serves the generated matplotlib javascript file.  The content
            is dynamically generated based on which toolbar functions the
            user has defined.  Call `FigureManagerWebAgg` to get its
            content.
            """

            def get(self):
                self.set_header('Content-Type', 'application/javascript')
                js_content = FigureManagerWebAgg.get_javascript()

                self.write(js_content)

        class Download(tornado.web.RequestHandler):
            """
            Handles downloading of the figure in various file formats.
            """

            def get(self, fmt):
                manager = self.application.manager

                mimetypes = {
                    'ps': 'application/postscript',
                    'eps': 'application/postscript',
                    'pdf': 'application/pdf',
                    'svg': 'image/svg+xml',
                    'png': 'image/png',
                    'jpeg': 'image/jpeg',
                    'tif': 'image/tiff',
                    'emf': 'application/emf'
                }

                self.set_header('Content-Type', mimetypes.get(fmt, 'binary'))

                buff = io.BytesIO()
                manager.canvas.figure.savefig(buff, format=fmt)
                self.write(buff.getvalue())

        class WebSocket(tornado.websocket.WebSocketHandler):
            """
            A websocket for interactive communication between the plot in
            the browser and the server.

            In addition to the methods required by tornado, it is required to
            have two callback methods:

                - ``send_json(json_content)`` is called by matplotlib when
                  it needs to send json to the browser.  `json_content` is
                  a JSON tree (Python dictionary), and it is the responsibility
                  of this implementation to encode it as a string to send over
                  the socket.

                - ``send_binary(blob)`` is called to send binary image data
                  to the browser.
            """
            supports_binary = True

            def open(self):
                # Register the websocket with the FigureManager.
                manager = self.application.manager
                manager.add_web_socket(self)
                if hasattr(self, 'set_nodelay'):
                    self.set_nodelay(True)

            def on_close(self):
                # When the socket is closed, deregister the websocket with
                # the FigureManager.
                manager = self.application.manager
                manager.remove_web_socket(self)

            def on_message(self, message):
                # The 'supports_binary' message is relevant to the
                # websocket itself.  The other messages get passed along
                # to matplotlib as-is.

                # Every message has a "type" and a "figure_id".
                message = json.loads(message)
                if message['type'] == 'supports_binary':
                    self.supports_binary = message['value']
                else:
                    manager = self.application.manager
                    manager.handle_json(message)

            def send_json(self, content):
                self.write_message(json.dumps(content))

            def send_binary(self, blob):
                if self.supports_binary:
                    self.write_message(blob, binary=True)
                else:
                    data_uri = "data:image/png;base64,{0}".format(
                        blob.encode('base64').replace('\n', ''))
                    self.write_message(data_uri)

        def __init__(self, figure):
            self.figure = figure
            self.manager = new_figure_manager_given_figure(id(figure), figure)

            super().__init__([
                # Static files for the CSS and JS
                (r'/_static/(.*)',
                 tornado.web.StaticFileHandler,
                 {'path': FigureManagerWebAgg.get_static_file_path()}),

                # The page that contains all of the pieces
                ('/', self.MainPage),

                ('/mpl.js', self.MplJs),

                # Sends images and events to the browser, and receives
                # events from the browser
                ('/ws', self.WebSocket),

                # Handles the downloading (i.e., saving) of static images
                (r'/download.([a-z0-9.]+)', self.Download),
            ])

    def find_similar(self, tfidf_matrix, index, top_n=5):

        """
            Find the "top_n" documents more similar to the document provided by the element in the "index" element
            in the tfidf_matrix
            Args:
                tfidf_matrix (matrix): tf_idf matrix
                index (int): element searched the similarity from
                top_n (int): number of similar elements seached
            Returns:
                list(matrix): list of the similarity to the element in the "index" position in the tfidfmatrix
        """
        cosine_similarities = linear_kernel(tfidf_matrix[index:index + 1], tfidf_matrix).flatten()
        related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]
        return [(index, cosine_similarities[index]) for index in related_docs_indices][0:top_n]

    def n_most_similar_for_each(self, corpus, tfidf_matrix):
        """
            Find the "top_n" documents more similar to the document provided by the element in the "index" element
            in the tfidf_matrix
            Args:
                tfidf_matrix (matrix): tf_idf matrix
                index (int): element searched the similarity from
                top_n (int): number of similar elements seached
            Returns:
                list(matrix): list of the similarity to the element in the "index" position in the tfidfmatrix
        """
        string_auxiliar = ''
        for me_index, item in enumerate(corpus):
            similar_documents = [(corpus[index], score) for index, score in
                                 self.find_similar(tfidf_matrix, me_index, top_n=1)]
            me = corpus[me_index]

            document_id = me[0]
            for ((raw_similar_document_id, title), score) in similar_documents:
                similar_document_id = raw_similar_document_id
                string_auxiliar = string_auxiliar + str(
                    [(document_id)[0:40], (similar_document_id)[0:40], "%.4f" % round(score, 4)]) + '\n'
                if string_auxiliar.count('\n') == self.max_number_to_plot: return string_auxiliar
        return string_auxiliar


    def most_similar(self, corpus, tfidf_matrix, param):
        """
            Find the most similar documents to the one provided by the element in the "index" element
            in the tfidf_matrix
            Args:
                tfidf_matrix (matrix): tf_idf matrix
                param (int): element searched the similarity from
                corpus: list of terms
            Returns:
                str: string with the similarity scores to be represented in the plot
        """


        string_auxiliar = ''
        for index, score in self.find_similar(tfidf_matrix, param, top_n=1):
            string_auxiliar = string_auxiliar + str(score) + ':' + corpus[index][0] + '\n'
        return string_auxiliar


    def plot(self, distance_matrix, corpus, tfidf_matrix, fig):
        """
            plot the similarity between documents
            Args:
                distance_matrix: matrix of the similarities betrween documents
                corpus: corpus of the terms of the documents
                tfidf_matrix (matrix): matrix of the tf_idf
                fig: Figure object where we set the properties of the plot
            Returns:
        """

        ax = fig.add_subplot(221)

        similarities = self.n_most_similar_for_each(corpus, tfidf_matrix)
        self.log.debug(similarities)

        ax.axis('off')
        ax.set_title("Ranking of similarity")
        left, width = .25, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height

        # ax.title.set_text('Masked line demo')
        ax.text(0.5 * (left + right), 0.5 * (bottom + top), similarities, horizontalalignment='center',
                verticalalignment='center', color='green', fontsize=15)
        y = np.arange(len(distance_matrix))

        # -----------------------------     MDS ON 2D       -----------------------------

        mds = manifold.MDS(n_components=2, dissimilarity='precomputed', random_state=1)
        Xtrans = mds.fit_transform(distance_matrix)

        ax = fig.add_subplot(223)

        #we limit the number of element
        if len(corpus) > self.max_number_to_plot:

            # we limit the number of elements to show
            corpus = corpus[:self.max_number_to_plot]
            colors = self.colors[:self.max_number_to_plot]
            markers = self.markers[:self.max_number_to_plot]

        # we plot the points in the frame
        for label, color, marker, document in zip(np.unique(y), colors, markers, corpus):
            position = y == label
            ax.scatter(Xtrans[position, 0], Xtrans[position, 1], label=document[0], color=color, marker=marker,
                       edgecolor='black')

        ax.set_title("Similarity representation by MDS dimensionality reduction")

        # -----------------------------     TSNE       -----------------------------
        model = manifold.TSNE(metric="precomputed")
        Xtrans = model.fit_transform(distance_matrix)
        ax = fig.add_subplot(224)
        for label, color, marker, document in zip(np.unique(y), colors, markers, corpus):
            position = y == label
            ax.scatter(Xtrans[position, 0], Xtrans[position, 1], label=document[0], color=color, marker=marker,
                       edgecolor='black')
        ax.legend(loc=9, bbox_to_anchor=(0.5, 2))

        ax.set_title("Similarity representation by TSNE dimensionality reduction")


    def get_vocabulary_from_authors(self, author):
        """
            get the vocabulary corresponding to the abstract of all the documents from all the coauthors
            Args:
                author: author whose coathors we would like to extract the vocabulary from
            Returns:
                corpus: terms present in the vocabulary from the  author
        """
        ids_coauthors = list(set(list(itertools.chain.from_iterable([coauthor['author_ids'] for coauthor in
                                                                     (self.collection_publications.find(
                                                                         {"_id": {"$in": author['publications']}},
                                                                         {'author_ids'}))]))))
        vocabulary_from_authors = []
        for id in ids_coauthors:
            author = self.collection_authors.find_one({"_id": id})
            list_from_author = [self.collection_authors.find_one({"_id": id}, {'_id': False, 'name': True})['name'],
                                list(set(list(itertools.chain.from_iterable([topicId['topicsId'] for topicId in
                                                                             (self.collection_publications.find({
                                                                                 "_id": {
                                                                                     "$in":
                                                                                         author[
                                                                                             'publications']}},
                                                                                 {
                                                                                     '_id': False,
                                                                                     'topicsId': True}))]))))]
            # we might find publications whose abtract is empty
            if len(list_from_author[1]) > 0: vocabulary_from_authors.append(list_from_author)

        corpus = []
        for author, topics in vocabulary_from_authors:
            sentence = ' '.join(topics)
            corpus.append((author, sentence))

        return corpus


    def get_vocabulary_all_pubs_by_1_author(self, author):
        """
            get the vocabulary corresponding to the abstract of all the documents from an author
            Args:
                author: author whom publications we would like to extract the abstract from
            Returns:
                corpus: terms present in the vocabulary from the  author
        """


        vocabulary_from_author = list((self.collection_publications.find({"_id":
                                                                              {"$in": author['publications']}},
                                                                         {'_id': False, 'title': True,
                                                                          'topicsId': True})))

        corpus = []
        for publication in vocabulary_from_author:
            if len(publication['topicsId']) > 0: corpus.append(
                (publication['title'], ' '.join(publication['topicsId'])))
        return corpus


    def get_vocabulary_from_all_authors_and_pubs(self, author):
        """
            get the vocabulary corresponding to the all the coauthors and all their publications
            Args:
                author: author, whose coathors we would like to extract the vocabulary from
                (all publications from all authors)
            Returns:
                corpus: terms present in the vocabulary from the  author
        """

        ids_coauthors = list(set(list(itertools.chain.from_iterable([coauthor['author_ids'] for coauthor in
                                                                     (self.collection_publications.find(
                                                                         {"_id": {"$in": author['publications']}},
                                                                         {'author_ids'}))]))))
        corpus = []
        for id in ids_coauthors:
            author = self.collection_authors.find_one({"_id": id})
            for pub in author['publications']:
                publication = self.collection_publications.find_one({"_id": pub},
                                                                    {'_id': False, 'title': True, 'topicsId': True})
                if len(publication['topicsId']) > 0:
                    corpus.append(
                        (author['name'] + ': "' + publication['title'] + '"', ' '.join(publication['topicsId'])))
        return corpus


    def get_corpus(self, optionSelected):
        """
            Get the corpus in the proper format corresponding to the option selected by "optionSelected"
            Args:
                optionSelected(str): option selected in the combo box of the options provided by the author
            Returns:
                corpus: terms of the vocabulary depending on the option selected
        """

        author = self.collection_authors.find_one({"name": self.teacher})

        if optionSelected == 'Comparador del autor con otros coautores':
            corpus = self.get_vocabulary_from_authors(author)
        elif optionSelected == 'Comparador obras del autor':
            corpus = self.get_vocabulary_all_pubs_by_1_author(author)
        elif optionSelected == 'Comparador de obras entre autor y coautores':
            corpus = self.get_vocabulary_from_all_authors_and_pubs(author)
        return corpus


    def plot_figure(self, fig):
        """
            Plots the figure with the features of the fig argument
            Args:
                fig(Figure): Figure with the required features to represent the plot
            Returns:
                corpus: terms of the vocabulary depending on the option selected
        """
        start_time = time.time()
        corpus = self.get_corpus(self.option_selected)
        # fit() function in order to learn a vocabulary from one or more documents
        # transform() function on one or more documents as needed to encode each as a vector.
        # if you want to extract count features and apply TF-IDF normalization and row-wise euclidean normalization you can do it in one operation

        tfidf_matrix = TfidfVectorizer().fit_transform([content for file, content in corpus])

        # Get the pairwise similarity matrix (n by n) (The result is the similarity matrix)
        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
        self.log.debug('---- COSINE SIMILARITIES ------\n')
        self.log.debug(cosine_similarities)

        # TSNE needs distances in order to plot the points
        distance_matrix = pairwise_distances(tfidf_matrix, tfidf_matrix, "cosine")
        self.plot(distance_matrix, corpus, tfidf_matrix, fig)


    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())

        start_time = time.time()

        figure = self.create_figure()
        application = self.MyApplication(figure)
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.bind(port=8080, reuse_port=True)
        http_server.start()
        webbrowser.open_new('http://127.0.0.1:8080/')
        self.log.debug("http://127.0.0.1:8080/")
        self.log.debug("Press Ctrl+C to quit")
        self.log.debug("The execution took: {0:0.2f} seconds".format(time.time() - start_time))
        tornado.ioloop.IOLoop.current().start()
        figure.clear()

class Similarities_in_between:

    def __init__(self, option_selected, teacher, id, collection_authors, collection_publications,
                 max_number_to_plot):
        self.option_selected = option_selected
        self.teacher = teacher
        self.collection_authors = collection_authors
        self.collection_publications = collection_publications
        self.max_number_to_plot = max_number_to_plot
        self.id = id

    def create_similarity_plot(self):

        """
            Creates a thread every time the execution button is pressed. We do so to avoid the button to get stucked
            flatten, what makes the execution unavailable
            Args:
            Returns:
        """
        t = myThread(self.option_selected, self.teacher, self.id, self.collection_authors, self.collection_publications,
                     self.max_number_to_plot)
        t.start()
