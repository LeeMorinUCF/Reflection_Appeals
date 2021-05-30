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
# May 29, 2021
# 
##################################################
#
# Identification and Estimation in Judicial Panel Voting
# Functions for Scraping Information from 
# Documents from US Courts of Appeals
# 
# This script reads case information from several files.
# The previous version imports a module for reading cases.
# This version pulls several fields and compares across cases.
# The information from any anomalies is used to refine
# the functions that extract fields.
# This version stores the result in a data frame. 
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

# Module for organizing case data into a data frame.
import pandas as pd


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


# Assume all files are translated to txt. 
# Later version will translate directly from 
# original doc file. 

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


# file_num_list = []
# case_code_list = []
# circ_num_list = []
# case_num_list = []
# case_date_list = []
# holdings_hdr_list = []
# outcome_list = []
# posture_list = []
# judicial_panel_list = []


# Get list of all files in a given directory sorted by name
txt_file_list = sorted( filter( os.path.isfile,
                        glob.glob(txt_path + '*') ) )

num_files = len(txt_file_list)
txt_file_num_list = range(num_files)

# Initialize data frame.
appeals = pd.DataFrame(columns = ['file_name', 'case_code', 'circ_num', 'case_num', 
                                  'case_date_1', 'case_date_2', 'case_date_3', 
                                  'background', 
                                  'holdings_hdr', 'outcome', 'posture', 'judicial_panel'], 
                       index = txt_file_num_list)


# Exclude some files that are problematic. 
# txt_file_num_excl = [12, 15, 17]
# txt_file_num_excl = [12, 15]
txt_file_num_excl = []
# Fix the anomalies and add them back. 

# txt_file_num_list = txt_file_num_list[txt_file_num_list not in txt_file_num_excl]

for txt_file_num in txt_file_num_list:
    
    if txt_file_num not in txt_file_num_excl:
        
        # Read the information from this case.
        txt_file = txt_file_list[txt_file_num]
        
        # Isolate the file name and primt a message.
        txt_file_name = os.path.split(txt_file)[1]
        print("Reading case information from file " + "'" +  txt_file_name + "'")
        
        # Get the dictionary of case info.
        case_info = caser.get_case_info(txt_file)
        
        
        # Enter the fields into the data frame.
        appeals['file_name'][txt_file_num] = txt_file_name
        appeals['case_code'][txt_file_num] = case_info["case_code"]
        appeals['circ_num'][txt_file_num] = case_info["circ_num"]
        
        # Skip parties, for now. 
        
        appeals['case_num'][txt_file_num] = case_info["case_num"]
        
        # Dates might occur in a list.
        # appeals['case_date_1'][txt_file_num] = case_info["case_date"]
        
        appeals['background'][txt_file_num] = case_info["background"]
        
        appeals['holdings_hdr'][txt_file_num] = case_info["holdings_hdr"]
        appeals['outcome'][txt_file_num] = case_info["outcome"]
        appeals['posture'][txt_file_num] = case_info["posture"]
        appeals['judicial_panel'][txt_file_num] = case_info["judicial_panel"]
        




# Print selected fields to screen. 
appeals['file_name']
appeals['case_code']
appeals['circ_num']
appeals['case_num']

appeals['background']

appeals['holdings_hdr']
appeals['outcome']

appeals['posture']
appeals['judicial_panel']


# import caser


# # Print selected fields to screen. 
# field_sel = 'case_code'
# field_sel = 'circ_num'
# print("List of results for field " + "'" + field_sel + "'")
# # Now inspect the contents. 
# for txt_file_num in txt_file_num_list:
    
#     print("Case %d: %s: %s" % (txt_file_num_list[txt_file_num], 
#                                field_sel, 
#                                case_info[field_sel][txt_file_num]))
    
    






##################################################
# Inspect individual cases
##################################################

# Choose a file and read the case information. 
# txt_file_num = 0
# txt_file_num = 1
# txt_file_num = 2
# txt_file_num = 4
# txt_file_num = 10
# txt_file_num = 11
# txt_file_num = 12
txt_file_num = 13
# txt_file_num = 15

# Read the information from this case.
txt_file = txt_file_list[txt_file_num]

print("Reading case information from file:")
print(txt_file)
print("")

# Get the dictionary of case info.
case_info = caser.get_case_info(txt_file)


caser.print_case_info(case_info)



##################################################
# Extra Code Snippets
##################################################





##################################################
# End
##################################################
