from PyPDF2 import PdfFileReader
def text_extractor(path):
    set_text = set()
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        # get the first page
        for pageNumber in range(pdf.numPages):
            page = pdf.getPage(pageNumber)
            print(page)
            print('Page type: {}'.format(str(type(page))))
            text = page.extractText()
            print(text)
if __name__ == '__main__':
    path = './author/1.pdf'
    text_extractor(path)