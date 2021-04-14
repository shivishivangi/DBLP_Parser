import xml.etree.ElementTree as ET 
import pandas as pd

# function parses through a single xml file  
# returns the author and a dictionary of n, pid, coauthor names, and coauthor pids for that specific author 
def parseXML(xmlfile): 
    tree = ET.parse(xmlfile)
    root = tree.getroot() 

    innerDict = {}
    author_list = [] # list of author pid and count of articles with main author
    article_name_list = [] # list of names of articles with the specified tags
    article_key_list = [] # list of article key and year (corresponds with the index of article name list)
    author_to_article_count_dict = {}
    coAuthors = ''
    coAuthorPID = ''

    for name in root.attrib:
        # gets author name, pid, n from each homepage 
        if name == 'n':
            n = root.attrib[name]
        if name == 'name':
            author_name = root.attrib[name]
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

    # count articles tag <article> 

    a_count = 1
    for article in root.findall('r/article'):
        if article.attrib.get('key') == None:
            article_key = 'NA'
        elif article.find('title').text == None:
            article_name = 'NA'
        elif article.find('year').text == None:
            article_year = 'NA'
        else:
            article_name = article.find('title').text
            article_key = article.attrib.get('key')
            article_year = article.find('year').text
        
        for author in article.findall('author'):
            if author.attrib.get('pid') == None:
                a_pid = 'NA'
            elif author.text == None:
                a_name = 'NA'
            else: 
                a_pid = author.attrib.get('pid')
                a_name = author.text
            
            if a_pid != pid:
                if a_pid not in author_to_article_count_dict:
                    author_info = (a_name, a_pid, str(1))
                    author_to_article_count_dict[a_pid] = author_info
                else:
                    count = int(author_to_article_count_dict[a_pid][2]) + 1
                    author_info = (a_name, a_pid, str(count))
                    author_to_article_count_dict[a_pid] = author_info

        article_info = (article_key, article_year)
        article_name_list.append(article_name)
        article_key_list.append(article_info)

        a_count += 1
    
    # count articles tag <inproceedings>

    for article in root.findall('r/inproceedings'):
        if article.attrib.get('key') == None:
            article_key = 'NA'
        elif article.find('title').text == None:
            article_name = 'NA'
        elif article.find('year').text == None:
            article_year = 'NA'
        else:
            article_name = article.find('title').text
            article_key = article.attrib.get('key')
            article_year = article.find('year').text
        
        for author in article.findall('author'):
            if author.attrib.get('pid') == None:
                a_pid = 'NA'
            elif author.text == None:
                a_name = 'NA'
            else: 
                a_pid = author.attrib.get('pid')
                a_name = author.text
            
            if a_pid != 'l/LinXuemin':
                if a_pid not in author_to_article_count_dict:
                    author_info = (a_name, a_pid, str(1))
                    author_to_article_count_dict[a_pid] = author_info
                else:
                    count = int(author_to_article_count_dict[a_pid][2]) + 1
                    author_info = (a_name, a_pid, str(count))
                    author_to_article_count_dict[a_pid] = author_info

        article_info = (article_key, article_year)
        article_name_list.append(article_name)
        article_key_list.append(article_info)
        a_count += 1

    for a in author_to_article_count_dict:
        author_list.append(author_to_article_count_dict[a])
            
    innerDict['pid'] = pid
    innerDict['n'] = n    
    innerDict['Article Count'] = a_count
    innerDict['Co-Author Names'] = coAuthors
    innerDict['Co-Author PIDs'] = coAuthorPID
    innerDict['Article Names'] = article_name_list
    innerDict['Article Keys and Year'] = article_key_list
    innerDict['Author Article Count'] = author_list

    return innerDict, author_name
    # print(coAuthorPID)

def publication_tag(tag, root, pub_count, article_name, article_key, author_collaboration_count_dict, pid):
    for article in root.findall('r/article'):
        if article.attrib.get('key') == None:
            article_key = 'NA'
        elif article.find('title').text == None:
            article_name = 'NA'
        elif article.find('year').text == None:
            article_year = 'NA'
        else:
            article_name = article.find('title').text
            article_key = article.attrib.get('key')
            article_year = article.find('year').text
        
        for author in article.findall('author'):
            if author.attrib.get('pid') == None:
                a_pid = 'NA'
            elif author.text == None:
                a_name = 'NA'
            else: 
                a_pid = author.attrib.get('pid')
                a_name = author.text
            
            if a_pid != pid:
                if a_pid not in author_collaboration_count_dict:
                    author_info = (a_name, a_pid, str(1))
                    author_collaboration_count_dict[a_pid] = author_info
                else:
                    count = int(author_collaboration_count_dict[a_pid][2]) + 1
                    author_info = (a_name, a_pid, str(count))
                    author_collaboration_count_dict[a_pid] = author_info

        article_info = (article_key, article_year)
        article_name.append(article_name)
        article_key.append(article_info)

        pub_count += 1
    
    return pub_count, article_name, article_key, author_collaboration_count_dict

# this part goes through an array of homepage xml files and populates a csv file 
# columns of the excel file are Author,pid,n,Co-Author Names,Co-Author PIDs


xmlFiles = ['LinXuemin.xml', 'BengChinOoi.xml', 'JXuYu.xml', 'WangChiewTan.xml', 'XiaofangZhou.xml']
# xmlFiles = ['LinXuemin.xml']
authorDict = {}
for file in xmlFiles:
    # authorDict[author] = parseXML(file)
    dict_val, author = parseXML(file)
    authorDict[author] = dict_val

dataset = pd.DataFrame.from_dict(authorDict, orient = "index") 
dataset.to_csv('author_count_information.csv')

# parseXML('LinXuemin.xml')
