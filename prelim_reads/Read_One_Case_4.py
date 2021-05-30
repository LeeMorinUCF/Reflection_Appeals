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
# This script reads case information from a single file.
#
##################################################
"""


##################################################
# Import Modules.
##################################################


# from caser import * # To read cases.
import caser # To read cases.

import os # To set working directory

# Modules for reading from doc (Word 97 2003):
# import win32com

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
doc_path = drive_path + doc_folder


# Set the directory with txt files after translation.
txt_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Sample_Sex_Har_2011_txt\\'
txt_path = drive_path + txt_folder




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
# txt_file_num = 1
# txt_file_num = 2
# txt_file_num = 4
# txt_file_num = 11
# txt_file_num = 12
# txt_file_num = 13
txt_file_num = 15

# Read the information from this case.
txt_file = txt_file_list[txt_file_num]

print("Reading case information from file:")
print(txt_file)
print("")


# lines_read = 0
with open(txt_file, 'r', encoding = 'utf-16') as file:
    
    # Record the case code. 
    case_code = caser.get_case_code(file)
    
    # Record the circuit number.
    circ_num = caser.get_circ_num(file)
    
    # Record the names of parties.
    # (pla_appnt, def_appee) = get_party_names(file)
    (pla_appnt, def_appee, last_line) = caser.get_party_names(file)
    
    # Record the case number.
    # case_num = get_case_num(file)
    case_num = caser.get_case_num(file, last_line)
    
    # Record the case date.
    case_date = caser.get_case_date(file)
    
    # Record the background, a paragraph describing the case. 
    background = caser.get_background(file)
    
    # Record the list of holdings.
    holdings = caser.get_holdings(file)
    # Record the "Holdings" header statement.
    holdings_hdr = holdings[0]
    # Record the case outcome. 
    outcome = holdings[-1]
    
    # Record the statement of "Procedural Posture(s)".
    posture = caser.get_posture(file)
    
    # Record the names of lawyers, judges and previous case.
    jurist_list = caser.get_jurist_list(file)
    # The first line is the council for the plaintiff-appellant.
    pla_appnt_council = jurist_list[0]
    # The next line is the council for the defendant-appellee.
    pla_appnt_council = jurist_list[1]
    # The last line is the judicial panel.
    judicial_panel = jurist_list[len(jurist_list) - 1]
    


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

print("judicial_panel = ")
print(judicial_panel)



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
