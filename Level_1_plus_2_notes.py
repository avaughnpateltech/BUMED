# -*- coding: utf-8 -*-
"""
Spyder Editor



This is a temporary script file.
"""

#STEP1: Level_1 ASCII EXTRACT
#Author: S Patel

#STEP1 START


from PyPDF2 import PdfFileReader
def get_info(path):
    global author, creator, producer, subject, title
    with open(path,'rb') as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    print(info)
    author = info.author
    creator = info.creator
    producer = info.producer
    subject = info.subject
    title = info.title

if __name__ == '__main__':
    
    path = r'C:\Users\aevaughn\Documents\BUMED\1001.2C.pdf'
    get_info(path)
    
    
#STEP1 END

#STEP2: Level_1 ASCII IF/ELSE
#Author: A Vaughn

#STEP2 START

def isNaN(string):
    return string != string

if (isNaN(author)==False or isNaN(subject)==False or isNaN(title)==False):
    print("Will Continue")
    
#STEP2 END

#STEP3: Level_1 RAW DATA PULL
#Author: A Vaughn

#STEP3 START

    import pdfplumber
    with pdfplumber.open(path) as pdf:
        first_page = pdf.pages[0]
        print(first_page.extract_text())

    import pandas as pd

    pdf_object = pdfplumber.open(path)

    char_df = pd.DataFrame()

    for page in pdf_object.pages:
        temp_df = pd.DataFrame(page.chars)
        char_df = char_df.append(temp_df)

    print(char_df)
    char_df.dtypes

    char_df2 = pd.DataFrame(char_df['text'])
    print(char_df2)

    prechar_df3 = first_page.extract_text()

    print(prechar_df3)

    from io import StringIO
    TESTDATA = StringIO(prechar_df3)
    print(TESTDATA)
    chardf3 = pd.read_table(TESTDATA, sep='!', error_bad_lines=False, header=None)
# Dataset is now stored in a Pandas Dataframe

    chardf3['page'] = 1

#STEP3 END

#STEP4: Level_2 RAW DATA PULL - includes whitespace
#Author: A Vaughn

#STEP4 START

#Imports
from pdf2image import convert_from_path
import pytesseract
import os
import pandas as pd

#I. Turn pdf into image
os.chdir(r"C:\Users\aevaughn\Documents\BUMED")
images = convert_from_path("1001.2C.pdf")

#II. For each image page, save it as page{i}

for i,image in enumerate(images,start=1):
    newimagepath = r"r'C:\Users\aevaughn\Documents\BUMED\page_" + str({i}) + ".jpg'"
    print(newimagepath)
    image.save(newimagepath,"JPEG")

#III. Extract the text from the image using pytesseract
    
docwithstrings = pytesseract.image_to_string(r"C:\Users\aevaughn\Documents\BUMED\page_1.jpg")

#IV. Place text into a dataframe

chardf4 = pd.read_table(docwithstrings, sep=None, error_bad_lines=False, header=None)    

#V. Create flag for blank lines

if chardf4['0'] == '':
    chardf4['blankflag'] = 1
else:
    chardf4['blankflag'] = 0

#VI. Transpose blankflag
#At this point, each blank line should have a '1' or a '0' associated with it
#Transposing the dataframe, we get a 'layout' we can compare to other layouts

chardf4_transp = chardf4['blankflag'].T

#At this point we would have a dataframe with this layout:
# 0  1  2  3  4 . . .
# 1  0  1  0  0 . . . 
#Each boolean column gives the 'blank' or 'nonblank' state of that row in the doc
#2.  In the corpus, then, we would do this for every document and group them by appending each transposition
#    and gathering each layout with > 1 frequency
#3. Then, we would have to have business analysts inspect them and determine where the fields appeared
#   and what each type of document was.  Ex. "Navy Research", "fields on first line", etc. This could
#   be done programatically if the documents contained some sort of tags. 
#4. We would then retain these layouts in a lookup table that we can run against each time a new document
#   is added to the corpus.  Then fields could be extracted by 'document type'

#STEP4 END

# Level 2 Code begins here

#SECTION 1: Build Document Component Analysis for Text Data

#Rules:
#1. If Document has labeled Document Fields, extract them
#2. If Document has spaced fields from first page, extract them
#3. If Document has date on first page, extract it

#1. 

#print(chardf3)

#chardf3['newf'] = 0

#for ind in chardf3.index:
  #if chardf3['page'][ind] ==1 and chardf3[0][ind].split()[0] == 'Subj:':
    #chardf3['newf'][ind] = 1



    
#2. 

#print(chardf3)

#chardf3['newf2'] = 0

#for ind in chardf3.index:
  #if chardf3['page'][ind] ==1 and chardf3[0][ind].split()[0][-1] == ':':
    #chardf3['newf2'][ind] = 1


#3. 

#print(chardf3)

#chardf3['newf'] = 0

#for ind in chardf3.index:
  #if chardf3['page'][ind] ==1 and chardf3[0][ind].split()[1] in ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'):
    #chardf3['newf'][ind] = 1