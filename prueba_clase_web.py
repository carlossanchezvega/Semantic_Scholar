import io
import itertools
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
import seaborn as sns; sns.set()
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pylab
from sklearn import linear_model, manifold, decomposition, datasets
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial import distance

colors = ['r', 'g', 'b', 'c','m','y','k']
markers = ['o', 6, '*', '^', 'h', 's']
import numpy as np
from sklearn import datasets,manifold
from sklearn.metrics.pairwise import linear_kernel
from scipy import spatial
from sklearn.metrics import pairwise_distances
import matplotlib as mpl
import io

try:
    import tornado
except ImportError:
    raise RuntimeError("This example requires tornado.")
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.websocket

class prueba_clase_web:



    def create_figure(self):
        """
        Creates a simple example figure.
        """
        fig = Figure(figsize=(20, 8))
        #a = fig.add_subplot(111)
        #t = np.arange(0.0, 3.0, 0.01)
        #s = np.sin(2 * np.pi * t)

        self.fill_information(fig)
        #a.plot(t, s)


        return fig


    # The following is the content of the web page.  You would normally
    # generate this using some sort of template facility in your web
    # framework, but here we just use Python string formatting.
    html_content = """
    <html>
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


    class MyApplication(tornado.web.Application):
        class MainPage(tornado.web.RequestHandler):

            # The following is the content of the web page.  You would normally
            # generate this using some sort of template facility in your web
            # framework, but here we just use Python string formatting.
            def __init__(self, *args, **kwargs):

                super().__init__(*args, **kwargs)
                self.html_content ="""<html>
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
                # html_content ="""<html>
                #                           <head>
                #                             <!-- TODO: There should be a way to include all of the required javascript
                #                                        and CSS so matplotlib can add to the set in the future if it
                #                                        needs to. -->
                #                             <link rel="stylesheet" href="_static/css/page.css" type="text/css">
                #                             <link rel="stylesheet" href="_static/css/boilerplate.css" type="text/css" />
                #                             <link rel="stylesheet" href="_static/css/fbm.css" type="text/css" />
                #                             <link rel="stylesheet" href="_static/jquery-ui-1.12.1/jquery-ui.min.css" >
                #                             <script src="_static/jquery-ui-1.12.1/external/jquery/jquery.js"></script>
                #                             <script src="_static/jquery-ui-1.12.1/jquery-ui.min.js"></script>
                #                             <script src="mpl.js"></script>
                #
                #                             <script>
                #                               /* This is a callback that is called when the user saves
                #                                  (downloads) a file.  Its purpose is really to map from a
                #                                  figure and file format to a url in the application. */
                #                               function ondownload(figure, format) {
                #                                 window.open('download.' + format, '_blank');
                #                               };
                #
                #                               $(document).ready(
                #                                 function() {
                #                                   /* It is up to the application to provide a websocket that the figure
                #                                      will use to communicate to the server.  This websocket object can
                #                                      also be a "fake" websocket that underneath multiplexes messages
                #                                      from multiple figures, if necessary. */
                #                                   var websocket_type = mpl.get_websocket_type();
                #                                   var websocket = new websocket_type("%(ws_uri)sws");
                #
                #                                   // mpl.figure creates a new figure on the webpage.
                #                                   var fig = new mpl.figure(
                #                                       // A unique numeric identifier for the figure
                #                                       %(fig_id)s,
                #                                       // A websocket object (or something that behaves like one)
                #                                       websocket,
                #                                       // A function called when a file type is selected for download
                #                                       ondownload,
                #                                       // The HTML element in which to place the figure
                #                                       $('div#figure'));
                #                                 }
                #                               );
                #                             </script>
                #
                #                             <title>matplotlib</title>
                #                           </head>
                #
                #                           <body>
                #                             <div id="figure">
                #                             </div>
                #                           </body>
                #                         </html>
                #                         """
                #
                #
                #
                # """
                # Serves the main HTML page.
                # """




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

        #
        # def find_similar(tfidf_matrix, index, top_n = 5):
        #     # we calculare cosine similarity to know similarities between documents
        #     cosine_similarities = linear_kernel(tfidf_matrix[index:index+1], tfidf_matrix).flatten()
        #
        #     # we order similarities in desc way (we do not include similarity corresponding to each sentence
        #     # since its similarity is equal to "1"
        #     related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]zº
        #     # we return that order
        #     return [(index, cosine_similarities[index]) for index in related_docs_indices][0:top_n]


    def find_similar(self, tfidf_matrix, index, top_n = 5):
        cosine_similarities = linear_kernel(tfidf_matrix[index:index+1], tfidf_matrix).flatten()
        related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]
        return [(index, cosine_similarities[index]) for index in related_docs_indices][0:top_n]
    # if we want to show
    # def find_similar(tfidf_matrix, index, top_n = 5):
    #
    #
    #
    #         # we calculare cosine similarity to know similarities between documents
    #         cosine_similarities = linear_kernel(tfidf_matrix[index:index+1], tfidf_matrix).flatten()
    #
    #         # we order similarities in desc way (we do not include similarity corresponding to each sentence
    #         # since its similarity is equal to "1"
    #         related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]

    #         related_docs_indices = [i for i in cosine_similarities.argsort()[::-1]]
    #
    #     # we return that order
    #     return [(index, cosine_similarities[index]) for index in related_docs_indices][0:top_n]


    # def find_similar(tfidf_matrix, index):
    #     top_n=5
    #     cosine_similarities = linear_kernel(tfidf_matrix[index:index+1], tfidf_matrix).flatten()
    #     related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]
    #     return [(index, cosine_similarities[index]) for index in related_docs_indices][0:top_n]
    #


    def n_most_similar_for_each(self, corpus, tfidf_matrix):
        string_auxiliar=''
        for me_index, item in enumerate(corpus):
            similar_documents =  [(corpus[index], score) for index, score in self.find_similar(tfidf_matrix, me_index, top_n=1)]
            me = corpus[me_index]

            document_id = me[0]
            for ((raw_similar_document_id, title), score) in similar_documents:
                similar_document_id = raw_similar_document_id
                print([document_id, me[1], similar_document_id, title, score])
                print(str(([document_id, me[1], similar_document_id, title, score])))
                string_auxiliar = string_auxiliar + str([document_id, similar_document_id, score])[0:45] + '\n'
                if string_auxiliar.count('\n')==5:
                    return string_auxiliar
        return string_auxiliar


    def most_similar(self, corpus, tfidf_matrix, param):
        string_auxiliar=''
        for index, score in self.find_similar(tfidf_matrix, param,top_n=1):
            #string_auxiliar = string_auxiliar + str(score) + ':' + corpus[index][1] + '\n'
            string_auxiliar = string_auxiliar + str(score) + ':' + corpus[index][0] + '\n'
        return string_auxiliar


    def plot(self, distance_matrix, corpus, tfidf_matrix, fig):

        # -----------------------------     RANKING       -----------------------------
        ax = fig.add_subplot(221)

        similarities = self.n_most_similar_for_each(corpus, tfidf_matrix)
        print(similarities)


        ax.axis('off')
        ax.set_title("Ranking of the most similar document to each one")
        left, width = .25, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height

        #ax.title.set_text('Masked line demo')
        ax.text(0.5 * (left + right), 0.5 * (bottom + top), similarities,horizontalalignment='center',
                verticalalignment='center',color='green', fontsize=15)
        y = np.arange(len(distance_matrix))


        # -----------------------------     MDS ON 3D       -----------------------------
        # ax = fig.add_subplot(222, projection='3d')
        # ax.set_facecolor('white')
        #
        # # using the precomputed dissimilarity to specify that we are passing a distance matrix:
        # mds = manifold.MDS(n_components=3, dissimilarity='precomputed', random_state=1)
        #
        # # With the distance between every pair of points is preserved
        # Xtrans = mds.fit_transform(distance_matrix)
        #
        # for label ,color, marker, document in zip( np.unique(y),colors, markers,corpus):
        #     position=y==label
        #     ax.scatter(Xtrans[position,0],Xtrans[position,1], Xtrans[position,2],label="target= {0}".format(document[0]),color=color, marker=marker, edgecolor='black')
        #
        #
        # pylab.title("MDS on example data set in 3 dimensions")
        # ax.view_init(10, -15)


        # -----------------------------     MDS ON 2D       -----------------------------

        mds = manifold.MDS(n_components=2, dissimilarity='precomputed', random_state=1)
        Xtrans = mds.fit_transform(distance_matrix)

        ax = fig.add_subplot(223)

        for label ,color, marker, document in zip( np.unique(y),colors, markers,corpus):
            position=y==label
            ax.scatter(Xtrans[position,0],Xtrans[position,1],label=document[0],color=color, marker=marker, edgecolor='black')

        #    ax.legend(loc="best")
        #ax.legend(loc=4)
        #ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

        ax.set_title("Similarity representation by MDS dimensionality reduction")


        # -----------------------------     TSNE       -----------------------------
        model =manifold.TSNE(metric="precomputed")
        Xtrans = model.fit_transform(distance_matrix)
        ax = fig.add_subplot(224)
        for label ,color, marker, document in zip( np.unique(y),colors, markers,corpus):
            position=y==label
            ax.scatter(Xtrans[position,0],Xtrans[position,1],label=document[0],color=color, marker=marker, edgecolor='black')
        ax.legend(loc=9, bbox_to_anchor=(0.5, 2))

        ax.set_title("Similarity representation by TSNE dimensionality reduction")

        filename = "distances.png"
        pylab.savefig(os.path.join('/home/csanchez/IdeaProjects/Semantic_Scholar', filename), bbox_inches="tight")

    def fill_information(self, fig):

        start_time = time.time()

        url_connection = "mongodb://localhost"
        connection = pymongo.MongoClient(url_connection)
        db = connection.authorAndPublicationData
        collection_authors = db.authors
        collection_publications= db.publications


        #########################################

        author = collection_authors.find_one({"_id": '3018657'})

        ids_coauthors = list(set(list(itertools.chain.from_iterable([coauthor['author_ids'] for coauthor in
                                                                     (collection_publications.find({"_id": {"$in": author['publications']}},{'author_ids'}))]))))

        corpus = []
        for id in ids_coauthors:
            author = collection_authors.find_one({"_id": id})
            for pub in author['publications']:
                publication = collection_publications.find_one({"_id": pub},
                                                               {'_id':False,'title':True,'topicsId':True})
                if len(publication['topicsId'])>0 :
                    corpus.append(((author['name']+': "'+publication['title']+'"')[0:65], ' '.join(publication['topicsId'])))





        #ids_publications = collection_authors.find_one ({"name": 'Alberto Fernández-Isabel'},{'_id':False,'publications':True})['publications']
        #publications = list((collection_publications.find({"_id": {"$in": ids_publications}},{'_id':False,'title':True,'topicsId':True})))
        #twenty = [['documento1',['this', 'is', 'the', 'documento1', 'sentence']],
        #          ['documento2',['this', 'is', 'the', 'documento2', 'sentence']],
        #          ['documento3',['this', 'is', 'the', 'documento3', 'sentence']],
        #          #              ['yet', 'another', 'sentence'],
        #          ['documento4',['this', 'is', 'the', 'documento4', 'sentence']],
        #          ['documento5',['this', 'is', 'the', 'documento5', 'sentence']],
        #          ['documento6',['this', 'is', 'the', 'documento6', 'sentence']]]




        #corpus = []
        #for file, content in twenty:
        #    sentence = ' '.join(content)
        #    corpus.append((file,sentence))


        # fit() function in order to learn a vocabulary from one or more documents
        # transform() function on one or more documents as needed to encode each as a vector.
        #if you want to extract count features and apply TF-IDF normalization and row-wise euclidean normalization you can do it in one operation

        tfidf_matrix = TfidfVectorizer().fit_transform([content for file, content in corpus])

        #Get the pairwise similarity matrix (n by n) (The result is the similarity matrix)
        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
        print(cosine_similarities)

        # TSNE needs distances in order to plot the points
        distance_matrix = pairwise_distances(tfidf_matrix, tfidf_matrix, metric='cosine', n_jobs=-1)
        self.plot(distance_matrix, corpus,tfidf_matrix, fig)



    def create_similarity_plot(self):
        start_time = time.time()

        figure = self.create_figure()
        application = self.MyApplication(figure)

        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(8080)
        webbrowser.open('http://127.0.0.1:8080/', new=2)

        print("http://127.0.0.1:8080/")
        print("Press Ctrl+C to quit")
        print("The execution took: {0:0.2f} seconds".format(time.time() - start_time))
        tornado.ioloop.IOLoop.instance().start()
