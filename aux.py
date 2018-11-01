import dblp
#do a simple author search for michael ley
authors = dblp.search('michael ley')
michael = authors[0]
print michael.name
print len(michael.publications)
