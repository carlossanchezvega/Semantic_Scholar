import pymongo
import sys, requests
import time
from bs4 import BeautifulSoup
import urllib3


def get_paper():
    page = requests.get("https://www.semanticscholar.org/paper/Identifying-Relations-for-Open-Information-Fader-Soderland/0796f6cd7f0403a854d67d525e9b32af3b277331")
    soup = BeautifulSoup(page.content, 'html.parser')
    pdf = soup.find(attrs={"name": "citation_pdf_url"})['content']

    content = urllib3.request.urlopen(pdf)
    for line in content:
        print(line)

    filename = "pdfExample.pdf"
    fout = open(filename, "wb")
    fout.write(content)




    # region Description
    """ pdf_file = open(pdf)
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    page = read_pdf.getPage(0)
    page_content = page.extractText()
    print(page_content) **/
    # endregion"""


def get_teachers():
    page = requests.get("http://www.masterdatascience.es/equipo/")
    soup = BeautifulSoup(page.content, 'html.parser')
    profesores = soup.findAll(attrs={"class": "title margin-clear"})
    nombres = [directors.text.split('-')[0].rstrip() for directors in soup.findAll(attrs={"class": "title margin-clear"})] \
              + [teacher.text for teacher in soup.findAll(attrs={"class": "small_white"})]
    print('Hola')


# end of problem


def main():
    get_paper()
    get_teachers()


# this is the standard boilerplate that calls the main() function
if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()