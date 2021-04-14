import xml.etree.ElementTree as ET 
import pandas as pd

# function parses through a single xml file  
# returns the author and a dictionary of n, pid, coauthor names, and coauthor pids for that specific author 
def parseXML(xmlfile): 
  
    # create element tree object 
    # parse = ET.XMLParser(encoding="utf-8")
    # tree = ET.parse('JeffreyXuYu.xml', ET.XMLParser(encoding="utf-8"))
    
    tree = ET.parse(xmlfile)
    # get root element 
    root = tree.getroot() 

    innerDict = {}
    coAuthors = ''
    coAuthorPID = ''

    for name in root.attrib:
        # gets author name, pid, n from each homepage 
        if name == 'n':
            n = root.attrib[name]
        if name == 'name':
            author = root.attrib[name]
        if name == 'pid':
            pid = root.attrib[name]
        # print(name, root.attrib[name])
    # print(author, pid, n)
    i = 1
    for coauthor in root.findall('coauthors/co/na'):
        if coauthor.text == None:
            coName = 'NA'
        elif coauthor.attrib.get('pid') == None:
            coPID = 'NA'
        else:
            coPID = coauthor.attrib.get('pid')
            coName = coauthor.text
        
        if i == 1:
            coAuthors = coName
            coAuthorPID = coPID
        else:
            coAuthors = coAuthors + ', ' + coName
            coAuthorPID = coAuthorPID + ', ' + coPID
        i = i + 1
    
    innerDict['pid'] = pid
    innerDict['n'] = n
    innerDict['Co-Author Names'] = coAuthors
    innerDict['Co-Author PIDs'] = coAuthorPID

    return innerDict, author
    # print(coAuthorPID)


# this part goes through an array of homepage xml files and populates a csv file 
# columns of the excel file are Author,pid,n,Co-Author Names,Co-Author PIDs


xmlFiles = ['LinXuemin.xml', 'BengChinOoi.xml', 'JXuYu.xml', 'WangChiewTan.xml', 'XiaofangZhou.xml']
authorDict = {}
for file in xmlFiles:
    # authorDict[author] = parseXML(file)
    dict_val, author = parseXML(file)
    authorDict[author] = dict_val

dataset = pd.DataFrame.from_dict(authorDict, orient = "index") 
dataset.to_csv('testing.csv')
    


