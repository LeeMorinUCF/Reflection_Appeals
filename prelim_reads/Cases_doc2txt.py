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
# Functions for Translating Documents from US Courts of Appeals
# from doc format to txt format. 
#
##################################################
"""


##################################################
# Import Modules.
##################################################


import os # To set working directory

import win32com.client # To interact with Windows applications (like Word).
import re # To work with reg expressions.



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
# Define function for translating files.
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



##################################################
# Translate some files.
##################################################




# Initialize object for Word application
app = win32com.client.Dispatch('Word.Application')
app.Visible = True

# Translate all files in a folder.
doc2txt_dir(app, doc_path, txt_path)





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
