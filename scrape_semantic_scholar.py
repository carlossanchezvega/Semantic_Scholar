import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver

siteUrl= 'https://www.semanticscholar.org/search?q=%22Krzysztof-Chylinski%22&sort=relevance'

def getInternalLinks(bsObj, includeUrl):
    internalLinks = []
    for link in bsObj.findAll("a", href=re.compile("^(/|.*"+includeUrl+")")):
        if "href" in link.attrs:
            if link.attrs["href"] not in internalLinks:
                internalLinks.append(link.attrs["href"])
    return internalLinks


def getArticles(bsObj, excludeUrl):
    externalLinks = []
    #for link in bsObj.findAll("a", href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
    #my_links = bsObj.findAll("a", {"class": "search-result-title"})

    driver = webdriver.Firefox()
    driver.get(siteUrl)
    html = driver.page_source
    soup = BeautifulSoup(html)
#    my_links = bsObj.findAll("div", {"class": "search-result-title"})
    my_links = soup.findAll("div", {"class": "search-result-title"})
    for link in my_links:
            if "href" in link.attrs:
                if link.attrs["href"] not in externalLinks:
                    externalLinks.append(link.attrs["href"])
    return externalLinks


def splitAddress(address):
    addressParts = address.replace("http://", "").split("/")
    return addressParts


def getAllExternalLinks(siteUrl, allExtLinks, allIntLinks):
    try:
        html = requests.get(siteUrl)
    except ValueError:
        return None
    bsObj = BeautifulSoup(html.text, "html.parser")
    articles = getArticles(bsObj, splitAddress(siteUrl)[0])
    externalLinks = getInternalLinks(bsObj, splitAddress(siteUrl)[0])
    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print(link)
    for article in articles:
        if link not in allIntLinks:
            print("A punto de obtener el enlace: "+link)
            allIntLinks.add(link)
            getAllExternalLinks(link, allExtLinks, allIntLinks)

getAllExternalLinks(siteUrl, set(), set())