# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 16:25:50 2021

@author: aevaughn
"""

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