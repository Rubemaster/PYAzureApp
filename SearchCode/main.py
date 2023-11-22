import os

#It is first of all paramount that this is set to the directory of this file on the system
os.chdir("C:\\Users\\ruri3531\\OneDrive - Uppsala universitet\\Ventures\\Projects\\Lit-erally")

from indexLibrary import *
from searchContent import *



#Take a directory of PDF files, index all files and save the indexed "library" as a .library file
#It is important for the functioning of the summary that all PDFs are have their requested citation in parenthesis in their filename
#For instance "(Deloitte 2014) Establishing the investment case wind power.pdf"
#processLibrary() also accepts a name argument for the name of the library, this name is given without the file type

#processLibrary("C:\\Users\\ruri3531\\Documents\\EIA","EIA")

#Running access will extract a library file and replace any current temporary library.
access('Wind Power Project Management.library')

inUKorCommunity=either("stakeholder","england","scotland","british","uk","united kingdom","commun","engage")
offshore=either("offshore","nearshore","archipelago","water","sea ","coast")

search(paragraph(either("threatened"),beneath(1000),above(300)),visual=True)




#summarize(paragraph(either("russia","soviet"),beneath(1000),above(300)),"Russia's role in Latvian intgration policy")


#    Summarize will search a library for paragraphs
#    that meet the criteria defined by constructing
#    an Affirmation.
#
#    It will proceed to construct a xml string with
#    all of the relevant paragraphs along with page
#    references to each of them, this xml will then
#    be passed on to ChatGPT. Which in turn will be
#    asked to summarize the content. The summary is
#    then displayed in the command line using python
#    print. The code presently stipulates a requested
#    text length of eight paragraphs.

#    It is important to understand that the functioning
#    of the interaction with Open AI requires a valid
#    API key

OPEN_AI.API_KEY="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"

summarize(paragraph(includes("integration","minority"),beneath(1000)))





