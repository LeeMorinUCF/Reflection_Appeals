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
# import zipfile
# from lxml import etree

# Modules for reading from doc (Word 97 2003):
import win32com

# Module for detecting type of character.
# import chardet

# Module for handling files and directories.
import glob


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
    if len(line_list) > 1:
        return(line_list[0].isdigit() and line_list[-1].isdigit())
    else:
        return False
        
# Function to find and get the case code.
def get_case_code(file):

    # First look for the case code.
    found_case_code = False
    # while not found_case_num and lines_read < 10:
    while not found_case_code:
        line = file.readline()
        found_case_code = is_case_code(line)
    
    # Record the case code. 
    case_code = line.replace("\n","")
    
    return(case_code)

# Determine if the line contains the string
# "United States Court of Appeals,"
def is_uscoa(line):
    line_list = line.split()
    if len(line_list) > 1:
        return(line_list[0].strip() == "United" and line_list[1].strip() == "States")
    else:
        return False
    
    

# Record the circuit number.
def get_circ_num(file):
    
    # Assumes the case code was just recorded. 
    # The next line should be "United States Court of Appeals,"
    # Keep reading until then. 
    found_uscoa = False
    while not found_uscoa:
        line = file.readline()
        found_uscoa = is_uscoa(line)
    
    # This line should be the circuit number.
    line = file.readline()
    circ_num = line.split()[0]
    
    return(circ_num)

# Get names of parties.
def get_party_names(file):
    
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
    
    return( (pla_appnt, def_appee) )


# Record the case number.
def get_case_num(file):
    
    # Assumes names of parties was just recorded. 
    # The next line should be the case number.
    line = file.readline()
    case_num = line.replace("\n","")
    
    return(case_num)
    


# Record the case date.
def get_case_date(file):
    
    # Assumes case number was just recorded. 
    # Sometimes there are multiple dates:
    # Submitted, Submitted and Argued, Filed.
    # Dates separated by a pipe (|).
    # After all dates is a line with the word "Synopsis".
    
    case_date = []
    found_synopsis = False
    while not found_synopsis:
        line = file.readline()
        line_list = line.split()
        # Check if the next line is "Synopsis".
        found_synopsis =  line_list[0].strip() == "Synopsis"
        # Skip the next line if it is a pipe (|).
        if not found_synopsis and line_list[0].strip() != "|":
            # The next line should be a date in text format.
            case_date.append(line.replace("\n",""))
    
    # Return one or all of the dates.
    # case_date = do_something_to(case_date)
    
    return(case_date)
    
# Record the background, a paragraph describing the case. 
def get_background(file):
    
    # Assumes the case date was just read. 
    # and that the previous line was the header "Synopsis".
    # line = file.readline()
    
    # The next line is the "Background" paragraph.
    line = file.readline()
    background = line.replace("\n","")
    
    return(background)



# Determine whether line goes beyond list of holdings.
def is_finished_holdings(line):
    if line[0] == '[' or line[0].strip() == '':
        return False
    else:
        return True

# Record the "Holdings" header statement.
def get_holdings(file):
    
    # The next line is the "Holdings" header statement.
    line = file.readline() # Skip a blank line.
    line = file.readline()
    holdings_hdr = line.replace("\n","")
    
    # For now, skip the contents of the holdings. 
    finished_holdings = False
    while not finished_holdings:
        line = file.readline()
        finished_holdings = is_finished_holdings(line)
        
    return(holdings_hdr)

# Record the case outcome. 
def get_outcome(file):
    
     # Assumes the holdings were just passed.
    # Record the case outcome. 
    outcome = line.replace("\n","")
    
    return(outcome)



# Record the statement of "Procedural Posture(s)".
def get_posture(file):
    
    # The next line is the statement of "Procedural Posture(s)".
    line = file.readline() # Skip a blank line.
    line = file.readline()
    posture = line.replace("\n","")
    
    return(posture)
        

##################################################
# Select a File and Scrape Contents
##################################################


# # Translate a single file.

# case_num = '01'
# party_1 = 'Helm'
# party_2 = 'Kansas'

# case_file_tag = case_num + " - " + party_1 + " v " + party_2
# doc_file = doc_path + case_file_tag + ".doc"
# txt_file = txt_path + case_file_tag + ".txt"


# # Initialize object for Word application
# app = win32com.client.Dispatch('Word.Application')
# app.Visible = True


# doc2txt_file(app, doc_file, txt_file)



##################################################
# Read through file and parse data
##################################################


# Get list of all files in a given directory sorted by name
txt_file_list = sorted( filter( os.path.isfile,
                        glob.glob(txt_path + '*') ) )


# Choose a file and read the case information. 
# txt_file_num = 0
txt_file_num = 1

# Read the information from this case.
txt_file = txt_file_list[txt_file_num]

print("Reading case information from file:")
print(txt_file)
print("")


lines_read = 0
with open(txt_file, 'r', encoding = 'utf-16') as file:
    
    # Record the case code. 
    case_code = get_case_code(file)
    
    # Record the circuit number.
    circ_num = get_circ_num(file)

    # Record the names of parties.
    (pla_appnt, def_appee) = get_party_names(file)
    
    # Record the case number.
    case_num = get_case_num(file)
    
    # Record the case date.
    case_date = get_case_date(file)
    
    # Record the background, a paragraph describing the case. 
    background = get_background(file)
    
    # Record the "Holdings" header statement.
    holdings_hdr = get_holdings(file)
    
    # Record the case outcome. 
    outcome = get_outcome(file)
    
    # Record the statement of "Procedural Posture(s)".
    posture = get_posture(file)
    


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
# Extra Code Snippets
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




##################################################
# End
##################################################
