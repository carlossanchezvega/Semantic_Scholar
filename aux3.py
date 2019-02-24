import requests
import os
import urllib3

def get_papers1(todo):
    pdf = 'http://ceur-ws.org/Vol-2083/paper-10.pdf'
    r = requests.get(pdf)

    filename = '1.pdf'
    dirname = os.path.dirname('BelenVelaSanchez')
    if not os.path.exists(dirname):
        os.makedirs('BelenVelaSanchez')
    with open(filename, 'wb') as code:
        code.write(r.content)






def get_papers2():

    url = 'http://www.hrecos.org//images/Data/forweb/HRTVBSH.Metadata.pdf'
    r = requests.get(url, stream=True)

    with open('/tmp/metadata.pdf', 'wb') as f:
       f.write(r.content)


def main():
    todo = './BelenVelaSanchez/1.pdf'
    get_papers2()


def get_paper3():

    """con la  petición de uno de los autorees"""
    pdf = 'http://ceur-ws.org/Vol-2083/paper-10.pdf'
    r = requests.get(pdf)
    # open method to open a file on your system and write the contents
    if not os.path.exists('./BelenVelaSanchez1/1'):
       os.makedirs('./BelenVelaSanchez1/1')
    with open("./BelenVelaSanchez1/1/pepitp.pdf", "wb") as code:
        code.write(r.content)



def get_paper4():
    pdf = 'http://ceur-ws.org/Vol-2083/paper-10.pdf'

    content = urllib3.request.urlopen(pdf)
    for line in content:
        print(line)

    filename = "pdfExample.pdf"
    fout = open(filename, "wb")
    fout.write(content)



def get_paper5():

    pdf = 'http://ceur-ws.org/Vol-2083/paper-10.pdf'

    content = urllib3.request.urlopen(pdf)
    for line in content:
        print(line)

    filename = "pdfExample.pdf"
    fout = open(filename, "wb")
    fout.write(content)



# this is the standard boilerplate that calls the main() function
if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    get_paper3()
    main()
