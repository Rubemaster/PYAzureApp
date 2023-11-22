
import inspect

#This python file contains several functions created to add convenience, mainly for the processing of lists of items.

#Intented for use with which, for instance capture(LIST, which(LIST, lambda v: v=="Banana"))
def capture(lst,index):
    return([lst[i1] for i1 in index])

#Function to perform same action on each item of a list, sample use: operate(LIST, lambda v: v+1). This will add one to each item of LIST
def operate(lst,fun):
    if len(inspect.signature(fun).parameters)==1:
        return([fun(item) for item in lst])
    return([fun(i1,item) for i1,item in enumerate(lst)])



#Function for selecting elements of a list that fulfill a certain criteria, for instance: which(LIST, lambda v: v=="Banana").
#This will return an index of all items of LIST that are equal to banana.
#Use together with capture to select the enumerated items

def which(lst,lambdaEvaluation):
    return([i1 for i1, v in enumerate(lst) if lambdaEvaluation(v)])

#This function will create a file and fill the file with a string.
def ink(filename,text):
    out = open(filename, "w")
    out.write(text)
    out.close()


import csv

csv.field_size_limit(1000000)
csv.field_size_limit(1000000)

def readCSV(filename):
  with open(filename, 'r') as read_obj:
    csv_reader = csv.reader(read_obj) 
    list_of_csv = list(csv_reader)
  return(list_of_csv)


import itertools

def flatten(listIn):
    return(list(itertools.chain.from_iterable(listIn)))

import re

def each(needle, haystack):
    return([m.start() for m in re.finditer( needle,haystack)])

def last(listIn):
    return(listIn[len(listIn)-1])

def unique(lisIn):
    return(list(dict.fromkeys(lisIn)))

def writeCSV(listIn,name):
    with open(name, 'w', newline='') as file:
          writer = csv.writer(file)
          writer.writerows(listIn) # Use writerow for single list

from nltk.corpus import wordnet

def wordTypeSub(word):
    try: 
        return(wordnet.synsets(word)[0].lexname().split(".")[0])
    except: 
        return("unknown")

def wordType(words):
    return(operate(words, lambda v: wordTypeSub(v)))

def terms(stringIn):
    terms=re.compile('[^a-z ]').sub(" ",stringIn.replace("-","").lower()).replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").split(" ")
    return(capture(terms,which(terms,lambda v: len(v)>3)))


def commonality(stringIn):
    words=terms(stringIn)
    words=capture(words,which(wordType(words),lambda v: v=="adj" or v=="noun"))
    uniques=unique(words)
    uniques=capture(uniques,which(uniques, lambda v: v!="such"))
    
    rank=operate(uniques,lambda v: words.count(v))
    order=sorted(range(len(rank)), key=lambda k: rank[k],reverse=True)
    return(operate(list(range(0,len(order))),lambda i1: [uniques[order[i1]],rank[order[i1]]]))
