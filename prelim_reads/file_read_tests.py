# -*- coding: utf-8 -*-
"""
##################################################
#
# Identification and Estimation in Judicial Panel Voting
#
# Lealand Morin, Ph.D.
# Assistant Professor
# Department of Economics
# College of Business 
# University of Central Florida
#
# May 28, 2021
# 
##################################################
#
# Identification and Estimation in Judicial Panel Voting
# Functions for Scraping Information from 
# Documents from US Courts of Appeals
#
##################################################
"""


##################################################
# Import Modules.
##################################################


import os # To set working directory

# Modules for reading pdfrs (need to be installed):
# import PyPDF2
# import textract

# Modules for reading from docx:
import zipfile
from lxml import etree

# Modules for reading from doc (Word 97 2003):
import win32com


##################################################
# Set Working Directory.
##################################################



# Find out the current directory.
os.getcwd()
# Change to a new directory.
# git_path = 'C:\\Users\\le279259\\Documents\\Teaching\\ECP3004_Spring_2021\\GitRepo\\ECP3004S21\\'
# os.chdir(git_path + 'demo_26_PP_Ch_15_Test_Debug')
drive_path = 'C:\\Users\\le279259\\OneDrive - University of Central Florida\\Documents\\'
# git_path = 'GitHub\\ECP3004S21\\'
git_path = 'Research\\Appeals_Reflection\\Reflection_Appeals\\'
os.chdir(drive_path + git_path + 'prelim_reads')
# Check that the change was successful.
os.getcwd()


# Set the directory with data files.
data_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Sample_Sex_Har_2011\\'
data_path = drive_path + data_folder


# Set the directory with txt files after translation.
txt_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Sample_Sex_Har_2011_txt\\'
txt_path = drive_path + txt_folder


##################################################
## Opening a pdf File
##################################################

# I don't have adult access to install my own software.
# I have to ask permission from the guy with the pink hair. 



##################################################
## Opening a docx File
##################################################

# This is simply unzipping the docx to get the xml code.

# Function for parsing xml content from docx document.
def get_word_xml(docx_filename):
   with open(docx_filename, 'rb') as f:
       # Unzipping opens a number of files and folders with standardized names.
      zip = zipfile.ZipFile(f)
       # One of these folders is "word".
       # A file in this folder is called "document.xml".
      xml_content = zip.read('word/document.xml')
      # This file contains the text content of the docx file.
   return xml_content


# Next, we need to parse this string containing XML into a usable tree. 
# For this, we use the lxml package (pip install lxml):

def get_xml_tree(xml_string):
   return etree.fromstring(xml_string)



# etree.tostring(xmltree, pretty_print=True)





# Try with a simple file.
sample_file_name = "Sample_Word_Document"
docx_file_name = sample_file_name + ".docx"

docx_path = data_path + docx_file_name 

zip_file_name = sample_file_name + "_zip.zip"

zip_path = data_path + zip_file_name 


# Unzip the docx file.
xml_sample_docx = get_word_xml(docx_path)


# Doesn't work: must be a zip file. 
# Works! Needed to read as binary.


# Rename docx to zip file. 

# Do later.
# May not be necessary. 


# Unzip a zip file.
xml_sample_zip = get_word_xml(zip_path)
# Also works when reading binary.


# Now convert to xml tree.
xml_tree_docx = get_xml_tree(xml_sample_docx)
xml_tree_zip = get_xml_tree(xml_sample_zip)
# They both look the same.

# Printing doesn't show much:
# for line in xml_tree_docx:
#     print(line)


# Instead, use a function designed for xml trees.
etree.tostring(xml_tree_docx, pretty_print=True)
etree.tostring(xml_tree_zip, pretty_print=True)
# They look the same.


xml_tree_str_docx = etree.tostring(xml_tree_docx, pretty_print=True)
# Try to print this:
# for line in xml_tree_str_docx:
#     print(line)
# Nonsensical sequence of numbers.






# Extracting text.
class DocX_Doc:
    
    def _itertext(self, my_etree):
        """Iterator to go through xml tree's text nodes"""
        for node in my_etree.iter(tag=etree.Element):
            if self._check_element_is(node, 't'):
                yield (node, node.text)
                
    def _check_element_is(self, element, type_char):
        word_schema = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        return element.tag == '{%s}%s' % (word_schema,type_char)
    
    
    def get_word_xml(self, docx_filename):
        
        # print("")
        # print("The self object is:")
        # print(self)
        # print("")
        # print("")
        # print("The docx_filename is:")
        # print(docx_filename)
        # print("")
        # print("")
        with open(docx_filename, 'rb') as f:
            # Unzipping opens a number of files and folders with standardized names.
           zip = zipfile.ZipFile(f)
            # One of these folders is "word".
            # A file in this folder is called "document.xml".
           xml_content = zip.read('word/document.xml')
           # This file contains the text content of the docx file.
        return xml_content
    
    
    
    # Next, we need to parse this string containing XML into a usable tree. 
    # For this, we use the lxml package (pip install lxml):
    
    def get_xml_tree(self, xml_string):
       return etree.fromstring(xml_string)




# Doesn't work because self is not defined.
# xml_from_file = self.get_word_xml(xml_sample_docx)


# xml_tree = self.get_xml_tree(xml_from_file)
# for node, txt in self._itertext(xml_tree):
#     print(txt)


# Initialize an object.
my_docx = DocX_Doc()

# Get the xml code from the docx file. 
xml_from_file = my_docx.get_word_xml(docx_path)

# Parse this string containing XML into a usable tree. 
xml_tree = my_docx.get_xml_tree(xml_from_file)



# Print the contents here. 
for node, txt in my_docx._itertext(xml_tree):
    # print(node) # Uninteresting.
    print(txt) # The text content. 



# Now try it with a court document. 


# Choose an arbitrary court case.
court_docx_file_name = "01 - Helm v Kansas.doc"
court_docx_path = data_path + court_docx_file_name 


# Initialize an object.
my_docx = DocX_Doc()

# Get the xml code from the docx file. 
xml_from_file = my_docx.get_word_xml(court_docx_path)

# Parse this string containing XML into a usable tree. 
xml_tree = my_docx.get_xml_tree(xml_from_file)



# Print the contents here. 
for node, txt in my_docx._itertext(xml_tree):
    # print(node) # Uninteresting.
    print(txt) # The text content. 




# Problem: The data are actually in doc Word 97 2003 format.


from win32com.client import gencache, constants, Dispatch
# that's the magic part
gencache.EnsureModule('{00020905-0000-0000-C000-000000000046}', 0, 8, 3)

app = Dispatch("Word.Application.8")

# open a document
app.Documents.Open(court_docx_file_name)

print(app)

print(app.Documents.Open(court_docx_file_name))


# with app.Documents.Open(court_docx_file_name) as file:
#     print(file)


# Try this:
doc = app.Documents.Open(court_docx_file_name)
docText = (doc.Content)
print(docText)
app.Quit()
# Problem: doc is None.


# Try this to convert to txt.

import win32com.client 
import os
import re
# rootdir ='C:\Users\IdaLim\Desktop\docs'     
rootdir = data_path
try:
    app = win32com.client.Dispatch('Word.Application')
    app.Visible = True
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            fullpath = os.path.join(*[subdir, file])
            if file.endswith(".doc"):
                out_name = file.replace("doc", r"txt")
                in_file = os.path.abspath(rootdir + "\\" + file)
                out_file = os.path.abspath(rootdir + "\\" + out_name)
                doc = app.Documents.Open(in_file)
                content = doc.Content.Text
                print('Exporting', out_file)
                doc.SaveAs(out_file, FileFormat=7)
                doc.Close()
except Exception, e:
    print e
finally:
    app.Quit()


# Just take the inner block.
   
rootdir = data_path
file = court_docx_file_name
out_name = file.replace("doc", r"txt")

in_file = os.path.abspath(rootdir + "\\" + file)
out_file = os.path.abspath(rootdir + "\\" + out_name)
doc = app.Documents.Open(in_file)
content = doc.Content.Text
print('Exporting', out_file)
doc.SaveAs(out_file, FileFormat=7)
doc.Close()





# Set paths for in_files (doc) and out_files (txt).
data_path
txt_path


# Initialize object for Word application
app = win32com.client.Dispatch('Word.Application')
app.Visible = True


# Loop through all doc files and convert to txt in another folder.
for subdir, dirs, files in os.walk(data_path):
    for file in files:
        fullpath = os.path.join(*[subdir, file])
        if file.endswith(".doc"):
            out_name = file.replace("doc", r"txt")
            in_file = os.path.abspath(data_path + "\\" + file)
            out_file = os.path.abspath(txt_path + "\\" + out_name)
            doc = app.Documents.Open(in_file)
            content = doc.Content.Text
            print('Exporting the txt version of ', out_file)
            doc.SaveAs(out_file, FileFormat=7)
            doc.Close()



##################################################
# End
##################################################
