import os
import itertools
from zipfile import ZipFile
from SearchCode.arbitrary import *
#from openai import OpenAI
import shutil

#class OPEN_AI:
#    API_KEY="EMPTY"
class color:
   BOLD = '<b>'
   END = '</b>'

def pageResults(bookName,pageName,pageContent,qualifier,visual=False):
    results="\n\n".join(capture(pageContent,which(pageContent,lambda v1: qualifier(v1))))
    bookName=bookName[bookName.find("(")+1:bookName.find(")")]
    if len(results)>0:
        if visual:
            return("\n\n\n"+bookName+", p."+pageName+"\n\n"+results)
        else:
            return("<page><id>"+bookName+", p."+pageName+"</id><content>"+results+"</content></page>")
    return("")

def bookResults(bookName,bookID,qualifier,visual=False):
    pages=list(itertools.chain.from_iterable(itertools.chain.from_iterable(
               operate(qualifier(),lambda v1: 
                       operate(capture(open("library/books/"+bookID+"/index page/"+v1[0].upper()+".txt").read().split(";"),
                                       which(open("library/books/"+bookID+"/index word/"+v1[0].upper()+".txt").read().split(","),
                                             lambda v2: v1 in v2)),
                               lambda v3: v3.split(","))))))
    pageContents=operate(pages, lambda page: open("library/books/"+bookID+"/pages/page" + page +".txt").read().split(";"))
    return("".join(operate(pageContents, lambda i1,page: pageResults(bookName,pages[i1],page,qualifier,visual))))

def search(qualifier, visual=False,capture=False):
    masterIndex=open("library/masterIndex.txt").read().split(";")
    returnValue="".join(operate(range(0,len(masterIndex),2),lambda i1: bookResults(masterIndex[i1],masterIndex[i1+1],qualifier,visual)))
    if visual:
        returnValue="n\n\n".join(unique(returnValue.split("\n\n\n")))
    for i1 in range(0,100,1):
        returnValue=returnValue.replace("\n\n\n","\n\n")
    if visual:
        for p in qualifier():
            returnValue=(color.BOLD+p+color.END).join(returnValue.split(p))
        if capture:
            return(returnValue.replace("\n","<br>"))
        else:
            print(returnValue)
            return(None)
    else:
        return("<page>".join(unique(returnValue.split("<page>"))))

def access(libraryName):
    if os.path.isdir("library"):
        shutil.rmtree("library")
    with ZipFile(libraryName, 'r') as f:
        f.extractall("library")

#def summarize(qualifier,topic=""):
#    xml=search(qualifier)
#    client = OpenAI(
#        api_key=OPEN_AI.API_KEY
#    )
#    if topic!="":
#        topic="Topic: "+topic
#    response  = client.chat.completions.create(
#        messages=[
#                {"role": "system", "content": "You will be provided with pages from articles (delimited with XML tags) about the same topic. Your task is to summarize the information in 8 paragraphs using only the provided pages and to cite the pages used. All sentences must be annotated with a citation."},
#                {"role": "user",   "content": topic+xml}
#        ],
#        model="gpt-3.5-turbo-16k",
#    )
#    print(response.choices[0].message.content)


#    The below functions are used for qualification of 
#    strings. Each function will create a function which
#    when called with a string as an input value will 
#    return a boolean.
#    
#    Example:
#
#    includes("mash","lunch","price")("Todays lunch: bangers and mash, price £8.20")
#
#    True
#   

def includes(*words):
    return(lambda *v1: (not (False in operate(list(words), lambda v2: v2.lower() in v1[0].lower()))) if len(v1)>0 else list(words))

def either(*words,minCount=1):
    return(lambda *v1: len(
                          which( 
                                operate(list(words), 
                                        lambda v2: v2.lower() in v1[0].lower()
                                        ),
                                lambda v:v==True))>=minCount if len(v1)>0 else list(words))

def exclude(*words):
    return(lambda *v1: (not (True in operate(list(words),lambda v2: v2.lower() in v1[0].lower()))) if len(v1)>0 else list())

def beneath(characterCount):
    return(lambda *v1: len(v1[0])<characterCount if len(v1)>0 else list())

def above(characterCount):
    return(lambda *v1: len(v1[0])>characterCount if len(v1)>0 else list())

def sentence(*FUNs):
    return(lambda *v1: (True in operate(v1[0].replace("?",".").replace("!",".").replace(";",".").split("."),lambda v2: (not (False in operate(list(FUNs), lambda FUN: FUN(v1[0])))))) if len(v1)>0 else list(itertools.chain.from_iterable(operate(FUNs,lambda v: v()))))

def paragraph(*FUNs):
    return(lambda *v1: (not (False in operate(list(FUNs), lambda FUN: FUN(v1[0])))) if len(v1)>0 else list(itertools.chain.from_iterable(operate(FUNs,lambda v: v()))))





