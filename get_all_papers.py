import pdfx
import requests
from bs4 import BeautifulSoup
import urllib.request
import requests
from re import search
from tika import parser, language
from nltk.corpus import stopwords
import nltk
import spacy
import string, time


def get_language_for_nltk(lang_request):
    listoffCodes = ['da','de','et','el','en','es','fi','fr','hu','is','it','nl','no','pl','pt','ru','sv','th']
    listofLanguages = ['danish','german','estonian','greek','english','spanish','finnish','french','hungarian','icelandic','italian','dutch','norwegian','polish','portuguese','russian','swedish','thai']
    language = dict( zip(listoffCodes,listofLanguages ))
    return language[lang_request]


def get_paper():

    """con la  petición de uno de los autorees"""
    page = requests.get("https://www.semanticscholar.org/paper/Identifying-Relations-for-Open-Information-Fader-Soderland/0796f6cd7f0403a854d67d525e9b32af3b277331")
    soup = BeautifulSoup(page.content, 'html.parser')
    """recogemmos el contenido de ese pdf en concreto"""
    pdf_url = soup.find(attrs={"name": "citation_pdf_url"})['content']
    r = requests.get(pdf_url)
    # open method to open a file on your system and write the contents
    with open("./papers2/python1.pdf", "wb") as code:
        code.write(r.content)


def get_paper2():

    """con la  petición de uno de los autorees"""
    page = requests.get("https://www.semanticscholar.org/paper/Identifying-Relations-for-Open-Information-Fader-Soderland/0796f6cd7f0403a854d67d525e9b32af3b277331")
    soup = BeautifulSoup(page.content, 'html.parser')

    """recogemmos el contenido de ese pdf en concreto"""
    pdf_url = soup.find(attrs={"name": "citation_pdf_url"})['content']


    # Copy a network object to a local file
    #urllib.request.urlretrieve(pdf_url, "./papers2/fichero_prueba.pdf")

    r = requests.get(pdf_url)
    # open method to open a file on your system and write the contents
    with open("./papers2/python1.pdf", "wb") as code:
        code.write(r.content)


def get_teachers():
    page = requests.get("http://www.masterdatascience.es/equipo/")
    soup = BeautifulSoup(page.content, 'html.parser')
    profesores = soup.findAll(attrs={"class": "title margin-clear"})
    nombres = [directors.text.split('-')[0].rstrip() for directors in soup.findAll(attrs={"class": "title margin-clear"})] \
              + [teacher.text for teacher in soup.findAll(attrs={"class": "small_white"})]
    #print('Hola')


def extract_content():
    parsedPDF = parser.from_file("./author/1.pdf")
    #print(parsedPDF['content'])
    #print(language.from_buffer(parsedPDF['content']))

    language_detected =  get_language_for_nltk(language.from_buffer(parsedPDF['content']))
    stopwords = nltk.corpus.stopwords.words(language_detected)
    stopwords.extend(string.punctuation)
    stopwords.append('')

    tokenized_text = [token.lower().strip(string.punctuation).strip() for token in nltk.word_tokenize(parsedPDF['content'])    \
                if token.lower().strip(string.punctuation) not in stopwords]

    return tokenized_text



def main():
    start = time.time();
    tokenized_text = extract_content()
    print (tokenized_text)
    end = time.time() - start
    print(end)
    get_paper2()
    get_teachers()

# this is the standard boilerplate that calls the main() function
if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()