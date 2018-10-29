

r = requests.get(url)
content = r.content.decode('utf-8')
BeautifulSoup(content, 'html.parser')