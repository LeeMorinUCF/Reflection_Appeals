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
# May 31, 2021
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
# This version processes all 175 cases in 2011
# referring to sexual harassment
# and categorized under Labor and Employment. 
# 
# TODO: Test cases by year to find which fail. 
#   Done 2011-2019. Approx 20% failure rate (failure to read to end). 
# 
# TODO: Create function to output data frame from list of files.
# TODO: Modify get_case_info() to stop at a certain point, 
#   for partial reading of files.
# TODO: Create is_valid_field(line) functions to test at scale.
# TODO: Verify that fields are reading valid information 
#   (i.e. no wrong fields). 
# TODO: Display incorrect fields. 
# TODO: Modify functions collecting invalid feilds and iterate.
# 
# TODO: Make a function which_case_info(line) to 
#   determine type of case info, in case the info 
#   is skipped or stored in a different order. 
# 
# TODO: Create function to extract judges' names from
#   line with judicial panel. 
# TODO: Create master list of judges. 
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
import win32com

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


# Note:
# To change names of files.
# Append a prefix "2" for files 200+.
# for file in 20*.doc; do   newfile=2"$(echo "$file" | cut -c3-)";   mv "$file" "$newfile"; done
# 


##################################################
# Set paths for handling files.
# Translate a year of doc files to txt
##################################################

data_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Court_Docs_SH_LE_' 

# # Set path for files in a single year.
# case_year = 2015

# doc_folder = data_folder + str(case_year) + '\\'
# doc_path = drive_path + doc_folder

# txt_folder = data_folder + str(case_year) + '\\'
# txt_path = drive_path + txt_folder


    
    
# ##################################################
# # Translate these doc Files to txt for this year
# ##################################################

# # Translate them all at once.
# # It takes a few seconds each. 

# # Initialize object for Word application
# app = win32com.client.Dispatch('Word.Application')
# app.Visible = True

# # Translate all files in a folder.
# caser.doc2txt_dir(app, doc_path, txt_path)




# Loop over files across several years.

# for case_year in range(2000, 2009):
#     print("Translating files for cases in year " + str(case_year))

#     # Set the directory with data files.
#     # doc_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Sample_Sex_Har_2011\\'
#     # doc_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Court_Docs_SH_LE_2011\\'
#     # doc_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Court_Docs_SH_LE_2012\\'
#     # doc_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Court_Docs_SH_LE_2013\\'
#     doc_folder = data_folder + str(case_year) + '\\'
#     doc_path = drive_path + doc_folder
    
    
#     # Set the directory with txt files after translation.
#     # txt_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Sample_Sex_Har_2011_txt\\'
#     # Place them in the same folder.
#     # txt_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Court_Docs_SH_LE_2011\\'
#     # txt_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Court_Docs_SH_LE_2012\\'
#     # txt_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Court_Docs_SH_LE_2013\\'
#     txt_folder = data_folder + str(case_year) + '\\'
#     txt_path = drive_path + txt_folder
    
    
    
    
    
#     ##################################################
#     # Translate this doc File to txt
#     ##################################################
    
#     # Translate them all at once.
#     # It takes a few seconds each. 
    
#     # Initialize object for Word application
#     app = win32com.client.Dispatch('Word.Application')
#     app.Visible = True
    
#     # Translate all files in a folder.
#     caser.doc2txt_dir(app, doc_path, txt_path)



##################################################
# Translate an Individual doc File to txt
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
# Read through text files and parse data
##################################################

# Set path for files in a single year.
case_year = 2011

txt_folder = data_folder + str(case_year) + '\\'
txt_path = drive_path + txt_folder



# Get list of all files in a given directory sorted by name
txt_file_list = sorted( filter( os.path.isfile,
                        glob.glob(txt_path + '*' + ".txt") ) )

num_files = len(txt_file_list)
txt_file_num_list = range(num_files)

# Exclude some files that are problematic. 
txt_file_num_excl = []

# First 20 (now fixed):
# txt_file_num_excl = [12, 15, 17]
# txt_file_num_excl = [12, 15]
# From rest of 2011:
txt_file_num_excl = [52, 116]
# From 2012:
# txt_file_num_excl = [10, 23, 104, 150, 152, 170]
# From 2013:
# txt_file_num_excl = [26, 46, 50, 64, 82, 84, 89, 106, 
#                      121, 122, 123, 124, 
#                      132]
# From 2014:
# txt_file_num_excl = [5, 17, 34, 62, 65, 82, 86, 93, 96, 98, 106, 113, 123, 137]
# From 2015:
# txt_file_num_excl = [15, 21, 55, 57, 71, 75, 86, 94, 109]
# From 2016:
# txt_file_num_excl = [36, 37, 55, 61, 62, 67, 68, 69, 82, 
#                      90, 91, 94, 97, 102, 103, 104, 
#                      109, 111, 115, 116]
# From 2017:
# txt_file_num_excl = [7, 15, 16, 23, 29, 45, 58, 61, 63, 65, 74, 
#                      87, 89, 95, 103, 105, 
#                      118, 119, 120, 121, 125, 126, 129, 130, 131, 
#                      134, 136, 147, 151]
# From 2018:
# txt_file_num_excl = [19, 25, 35, 39, 48, 51, 53, 59, 62, 63, 65, 70, 
#                      78, 82, 83, 89, 91, 99, 108, 114, 116]
# From 2019:
# txt_file_num_excl = [0, 30, 37, 39, 40, 59, 66, 76, 78, 81, 
#                      90, 91, 92, 94, 100, 106, 109, 122, 128]

# Fix the anomalies and add them back. 


# Calculate sub list after exclusions.
# txt_file_num_list = list(range(num_files))
# txt_file_num_list = [num for num in txt_file_num_list if num not in txt_file_num_excl]

# Select subset to skip problematic files. 
txt_file_list_sel = []
for txt_file_num in txt_file_num_list:
    
    if txt_file_num not in txt_file_num_excl:
        
        txt_file_list_sel.append(txt_file_list[txt_file_num])


# Get data frame of case info from list of case files. 
# fields = ['file_name', 'case_code', 'circ_num', 
#           'pla_appnt', 
#           'def_appee',
#           'case_num', 
#           'case_date', 
#           'background', 
#           'holdings_hdr', 'outcome', 'posture', 'judicial_panel']

# import caser

# fields = 'all'
num_fields = 12
print_msg = True
appeals = caser.get_case_df(txt_file_list_sel, num_fields, print_msg)



# Print selected fields to screen. 
appeals['file_name']
appeals['case_code']
is_valid = caser.is_case_code_vec(appeals['case_code'])['is_valid']
sum(is_valid)


appeals['circ_num']
appeals['circ_num'].unique()
is_valid = caser.is_circ_num_vec(appeals['circ_num'])['is_valid']
sum(is_valid)

appeals['pla_appnt_1']
is_valid = caser.is_pla_appnt_vec(appeals['pla_appnt_1'])['is_valid']
sum(is_valid)
appeals['pla_appnt_1'][is_valid == False]
# One apellee in error: 158 in 2011.

# Look for confounded parties:
is_valid = caser.is_def_appee_vec(appeals['pla_appnt_1'])['is_valid']
sum(is_valid)
appeals['pla_appnt_1'][is_valid == True]


appeals['pla_appnt_2']
is_valid = caser.is_pla_appnt_vec(appeals['pla_appnt_2'])['is_valid']
sum(is_valid)
appeals['pla_appnt_2'][is_valid]
appeals['pla_appnt_2'][is_valid == False].unique()
sum(appeals['pla_appnt_2'] == 'and')


appeals['pla_appnt_3']
is_valid = caser.is_pla_appnt_vec(appeals['pla_appnt_3'])['is_valid']
sum(is_valid)
appeals['pla_appnt_3'][is_valid == False].unique()
appeals['pla_appnt_3'].unique()

appeals['def_appee_1']
is_valid = caser.is_def_appee_vec(appeals['def_appee_1'])['is_valid']
sum(is_valid)
appeals['def_appee_1'][is_valid == False].unique()

# Look for confounded parties:
is_valid = caser.is_pla_appnt_vec(appeals['def_appee_1'])['is_valid']
sum(is_valid)
appeals['def_appee_1'][is_valid == False]

appeals['def_appee_2']
is_valid = caser.is_def_appee_vec(appeals['def_appee_2'])['is_valid']
sum(is_valid)

appeals['def_appee_3']
appeals['def_appee_4']


appeals['case_num']
is_valid = caser.is_case_num_vec(appeals['case_num'])['is_valid']
sum(is_valid)
appeals['case_num'][is_valid == False].unique()
# Success! (for 2011, at least)


appeals['case_date_1']
appeals['case_date_2']
appeals['case_date_3']
appeals['case_date_4']


appeals['background']
is_valid = caser.is_background_vec(appeals['background'])['is_valid']
sum(is_valid)
appeals['background'][is_valid == False].unique()
# Still some bugs to work out with the date. 
appeals[['file_name', 'background']][is_valid == False]


appeals['holdings_hdr']
appeals['outcome']

appeals['posture']
appeals['judicial_panel']






##################################################
# Inspect individual cases
##################################################

# Choose a file and read the case information. 
# txt_file_num = 0

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
