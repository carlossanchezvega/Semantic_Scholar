
from bs4 import BeautifulSoup
import requests
import urllib.request


def main():
    page = requests.get("https://www.semanticscholar.org/paper/Identifying-Relations-for-Open-Information-Fader-Soderland/0796f6cd7f0403a854d67d525e9b32af3b277331")
    soup = BeautifulSoup(page.content, 'html.parser')

    """recogemmos el contenido de ese pdf en concreto"""
        pdf_url = soup.find(attrs={"name": "citation_pdf_url"})['content']


    # Copy a network object to a local file
    #urllib.request.urlretrieve(pdf_url, "./papers2/fichero_prueba.pdf")

    r = requests.get(pdf_url)
    # open method to open a file on your system and write the contents
    with open("./"+teacher+"/"+get_file_name(pdf_url)+".pdf", "wb") as code:
        code.write(r.content)


if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()

