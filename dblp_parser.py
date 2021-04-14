import codecs
from bs4 import BeautifulSoup
import logging
import pandas as pd
import hashlib


encodings = ['ISO-8859-1','ascii']
for e in encodings:
    try:
        fh = codecs.open('dblp_march.xml','r',encoding=e)
        fh.seek(0)
    except UnicodeDecodeError:
        logging.debug('got unicode error with %s, trying a different encoding' % e)
    else:
        logging.debug('opening the file with encoding: %s' % e)
        break

# f = codecs.open('authors.xml',encoding=e)
# soup = BeautifulSoup(f.read(),'html.parser')



# # homepages = soup.find_all('phdthesis')
# # h = soup.find('phdthesis')
# # a = h.find_all('author')
# # count = 0
# # for author in a:
# #     if count >= 100:
# #         break;
# #     print(author.get_text())
# #     count += 1

# # print(h["key"])
# innerDict = {}
# authorDict = {}
# count = 0
# homepages = soup.find_all('www')
# for h in homepages:
#     innerDict = {}
#     # if count >= 100:
#     #     break
#     key = h["key"]
#     authors = h.find_all('author')
#     i = 1
#     for a in authors:
#         authorName = a.get_text()
#         if i == 1:
#             name = authorName
#         else:
#             name = name + ', ' + authorName
#         i += 1
#     innerDict['author name'] = name
#     innerDict['key'] = key
#     authorDict[count] = innerDict
#     count += 1
#     # print(key, " ", name)
# dataset = pd.DataFrame.from_dict(authorDict, orient = "index") 
# dataset.to_csv('author.csv')

with codecs.open('dblp_march.xml',encoding=e) as f:
    hasher = hashlib.sha256()
    while block := f.read(64 * (1 << 20)):  # Assigns and tests result in conditional!
        soup = BeautifulSoup(block, 'html.parser')
        innerDict = {}
        authorDict = {}
        count = 0
        homepages = soup.find_all('www')
        for h in homepages:
            innerDict = {}
            # if count >= 100:
            #     break
            key = h["key"]
            authors = h.find_all('author')
            i = 1
            for a in authors:
                authorName = a.get_text()
                if i == 1:
                    name = authorName
                else:
                    name = name + ', ' + authorName
                i += 1
            innerDict['author name'] = name
            innerDict['key'] = key
            authorDict[count] = innerDict
            count += 1
            # print(key, " ", name)
        hasher.update(str(block).encode())
dataset = pd.DataFrame.from_dict(authorDict, orient = "index") 
dataset.to_csv('author.csv')