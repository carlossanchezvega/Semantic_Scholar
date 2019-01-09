import pdfx
import requests
from bs4 import BeautifulSoup
import urllib.request
import requests
from re import search


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
    print('Hola')


# end of problem


def main():
    get_paper2()
    get_teachers()
    #probar_extraccion()

# this is the standard boilerplate that calls the main() function
if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()