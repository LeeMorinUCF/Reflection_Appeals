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

# Module for detecting type of character.
import chardet


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


##################################################
# Set paths for handling files.
##################################################

# Set the directory with data files.
doc_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Sample_Sex_Har_2011\\'
doc_path = drive_path + data_folder


# Set the directory with txt files after translation.
txt_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Sample_Sex_Har_2011_txt\\'
txt_path = drive_path + txt_folder



##################################################
# Define functions for translating files.
##################################################


# Translate all doc files in a directory.
def doc2txt_dir(app, doc_path, txt_path):

    # Loop through all doc files and convert to txt in another folder.
    for subdir, dirs, files in os.walk(doc_path):
        for file in files:
            # fullpath = os.path.join(*[subdir, file])
            if file.endswith(".doc"):
                out_name = file.replace("doc", r"txt")
                in_file = os.path.abspath(doc_path + "\\" + file)
                out_file = os.path.abspath(txt_path + "\\" + out_name)
                doc = app.Documents.Open(in_file)
                # content = doc.Content.Text
                print('Exporting the txt version of ', file)
                doc.SaveAs(out_file, FileFormat = 7)
                doc.Close()

# Translate a single file from doc to txt.

def doc2txt_file(app, doc_file, txt_file):
    doc = app.Documents.Open(doc_file)
    doc.SaveAs(txt_file, FileFormat = 7)
    doc.Close()



# Function to determine if a line contains the case code.
def is_case_code(line):
    # Case numbers have digits at the beginning and end of the line.
    line_list = line.split()
    if len(line) > 1:
        
        if line_list[0].isdigit() and line_list[-1].isdigit():
            return True
        else:
            return False

# Determine whether line goes beyond list of holdings.
def is_finished_holdings(line):
    if line[0] == '[' or line[0].strip() == '':
        return False
    else:
        return True
        

##################################################
# Select a File and Scrape Contents
##################################################


# Translate a single file.

case_num = '01'
party_1 = 'Helm'
party_2 = 'Kansas'

case_file_tag = case_num + " - " + party_1 + " v " + party_2
doc_file = doc_path + case_file_tag + ".doc"
txt_file = txt_path + case_file_tag + ".txt"


# Initialize object for Word application
app = win32com.client.Dispatch('Word.Application')
app.Visible = True


doc2txt_file(app, doc_file, txt_file)



##################################################
# Read through file and parse data
##################################################




# with open(txt_file, 'r', encoding = 'utf-16') as file:
#     for line_num in range(20):
#         line = file.readline()
#         print(line)
#         print(str(line))
#         print(line.rstrip())
#         # print(line.decode('utf-16'))
#         print(line.split())
#         print(str(line).rstrip().split())
#         print(line.replace("\r\n","").split())




import glob

# Get list of all files in a given directory sorted by name
txt_file_list = sorted( filter( os.path.isfile,
                        glob.glob(txt_path + '*') ) )


# Choose a file and read the case information. 
txt_file_num = 1

# Read the information from this case.
txt_file = txt_file_list[txt_file_num]

print("Reading case information from file:")
print(txt_file)
print("")


lines_read = 0
with open(txt_file, 'r', encoding = 'utf-16') as file:
    
    # First look for the case number.
    found_case_code = False
    # while not found_case_num and lines_read < 10:
    while not found_case_code:
        # lines_read = lines_read + 1
        line = file.readline()
        # print(line)
        
        found_case_code = is_case_code(line)
        
        # line_bytes = line_bytes[0:(len(line_bytes) - 1)]
        # line_bytes = line_bytes.rstrip()
        # line_str = line_bytes.decode('utf-16')
        # found_case_num = is_case_num(line_str)
    
    # Record the case number. 
    case_code = line.replace("\n","")
    
    # The next line should be "United States Court of Appeals,"
    # lines_read = lines_read + 1
    line = file.readline()
    # This line should be the circuit number.
    line = file.readline()
    circ_num = line.split()[0]
    
    # The next name should be the Plaintiff-Appellant.
    line = file.readline()
    pla_appnt_list = line.split()
    pla_appnt = ' '.join(pla_appnt_list[0:len(pla_appnt_list) - 1])
    pla_appnt = pla_appnt.replace(",","")
    
    # The next line is "v."
    line = file.readline()
    
    # The next name should be the Defendant-Appellee.
    line = file.readline()
    def_appee_list = line.split()
    def_appee = ' '.join(def_appee_list[0:len(def_appee_list) - 1])
    def_appee = def_appee.replace(",","")
    
    # The next line should be the case number.
    line = file.readline()
    case_num = line.replace("\n","")
    
    # The next line is a pipe (|).
    line = file.readline()
    
    # The next line is the date in text format.
    line = file.readline()
    case_date = line.replace("\n","")
    
    # The next line is the header "Synopsis".
    line = file.readline()
    
    # The next line is the "Background" paragraph.
    line = file.readline()
    background = line.replace("\n","")
    
    # The next line is the "Holdings" header statement.
    line = file.readline() # Skip a blank line.
    line = file.readline()
    holdings_hdr = line.replace("\n","")
    
    finished_holdings = False
    while not finished_holdings:
        line = file.readline()
        finished_holdings = is_finished_holdings(line)
        
    # Record the case outcome. 
    outcome = line.replace("\n","")
    
    # The next line is the statement of "Procedural Posture(s)".
    line = file.readline() # Skip a blank line.
    line = file.readline()
    posture = line.replace("\n","")


# Print the results.
print("case_code = ")
print(case_code)

print("circ_num = ")
print(circ_num)

print("pla_appnt = ")
print(pla_appnt)

print("def_appee = ")
print(def_appee)

print("case_num = ")
print(case_num)

print("case_date = ")
print(case_date)

print("background = ")
print(background)

print("holdings_hdr = ")
print(holdings_hdr)

print("outcome = ")
print(outcome)

print("posture = ")
print(posture)






##################################################
# End
##################################################
