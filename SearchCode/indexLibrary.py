import os
from arbitrary import *
import shutil
import fitz
import re
import inspect
import pathlib
import csv


def resetStructure():
    if os.path.isdir("temporary library"):
        shutil.rmtree("temporary library")
    os.mkdir("temporary library")
    os.mkdir("temporary library/books")

def trim(string):
    return(re.sub("[^a-zA-Z0-9().,!? -]+","",string.replace("\n"," ").replace("   "," ").replace("  "," ").replace("  "," ").replace("  "," ")).replace(" .","."))

def leafThrough(filename):
    if not 'PAGE_COUNT' in globals():
        global PAGE_COUNT
        PAGE_COUNT=0
    pages=operate(fitz.open(filename),lambda v1:operate(v1.get_textpage().extractBLOCKS(),lambda v2:trim(list(v2)[4])) )
    PAGE_COUNT=PAGE_COUNT+len(pages)
    print(PAGE_COUNT)
    pagesNew=[]
    for i1,page in enumerate(pages):
        pagesNew.append([])
        for i2,paragraph in enumerate(page):
            if len(paragraph)>0:
                if paragraph[0].islower() and i2>0:
                    paragraph=pages[i1][i2-1]+paragraph
                if paragraph[0].islower() and i2==0 and i1>0:
                    if len(pages[i1-1])>0:
                        paragraph=pages[i1-1][len(pages[i1-1])-1]+paragraph
                evaluateString=re.sub('[0-9]',"", paragraph).replace(". .","").replace("   "," ").replace("  "," ")
                if evaluateString.count(".")>1 and evaluateString.count(" ")>4:
                    pagesNew[i1].append(paragraph.replace("- ",""))
    return(pagesNew)

def indexBook(bookDirectory,pages):
    uniqueWords=sorted(list(set(re.sub('[^A-Za-z0-9]+', ' '," ".join(pages).lower()).replace("   "," ").replace("  "," ").split())))
    alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    firstLetter=operate(uniqueWords.copy(),lambda x: x[0])
    pages=operate(pages,lambda v:v.lower())
    for letter in alphabet:
	    wordHits=capture(uniqueWords,which(firstLetter,lambda v:v==letter)) 
	    wordPageNumber=";".join(operate(wordHits,lambda v1:",".join(operate(which(pages,lambda v3:v1 in v3),lambda v2: str(v2)))))
	    ink(bookDirectory+"/index word/"+letter.upper()+".txt",",".join(wordHits))
	    ink(bookDirectory+"/index page/"+letter.upper()+".txt",wordPageNumber)

def processBook(filename,bookDirectory):
    os.mkdir(bookDirectory+"/pages")
    os.mkdir(bookDirectory+"/index page")
    os.mkdir(bookDirectory+"/index word")
    pages=leafThrough(filename)
    operate(pages,lambda i1,v: ink(bookDirectory+"/pages/page"+str(i1)+".txt", ";".join(v)))
    indexBook(bookDirectory,operate(pages,lambda v: " ".join(v)))

def processLibrary(source,name):
    books=capture(os.listdir(source),which(os.listdir(source),lambda v: (".pdf" in v )|( ".epub" in v)))
    resetStructure()
    operate(books, lambda i1,v: os.mkdir("temporary library/books/book"+str(i1)))
    operate(books, lambda i1,v: processBook(source+"/"+v,"temporary library/books/book"+str(i1)))
    masterIndex=";".join(operate(books, lambda i1,v: v+";"+"book"+str(i1)))
    ink("temporary library/masterIndex.txt",masterIndex)
    shutil.make_archive(name, 'zip', "temporary library")
    shutil.rmtree("temporary library")
    if os.path.isfile(name+".library"):
        os.remove(name+".library")
    os.rename(name+".zip", name+".library")
