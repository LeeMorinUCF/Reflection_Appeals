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
# This version repaets for each year from 2000 to 2019. 
# 
# TODO: Test cases by year to find which fail. 
#   Done 2011-2019. Approx 20% failure rate (failure to read to end).
#   100% of files are read without failure; Done.
#   Some errors remaining in reading the fields.
# 
# TODO: Create function to output data frame from list of files. Done.
# TODO: Modify get_case_info() to stop at a certain point, 
#   for partial reading of files. Done.
# TODO: Create is_valid_field(line) functions to test at scale. Done.
# TODO: Verify that fields are reading valid information 
#   (i.e. no wrong fields). Done. Some different case types remain partially read. 
# TODO: Display incorrect fields. DOne. 
# TODO: Modify functions collecting invalid feilds and iterate. 
#   Some iteration complete. Some adjustments remain. 
# 
# TODO: Make a function which_case_info(line) to 
#   determine type of case info, in case the info 
#   is skipped or stored in a different order. Done. 
# 
# TODO: Create function to extract judges' names from
#   line with judicial panel. 
# TODO: Create master list of judges. 
# TODO: Create function that parses case numbers
#   to get list of numbers of case numbers related to each case. 
#   Return a list of case numbers. 
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
# case_year = 2000
# case_year = 2001
case_year = 2002
# case_year = 2003 # Background not labeled. 
# case_year = 2004
# case_year = 2005
# case_year = 2006
# case_year = 2007
# case_year = 2008
# case_year = 2009
# case_year = 2010
# case_year = 2011
# case_year = 2012
# case_year = 2013
# case_year = 2014
# case_year = 2015
# case_year = 2016
# case_year = 2017
# case_year = 2018
# case_year = 2019

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
# txt_file_num_excl = [52, 116]
# From 2012:
# txt_file_num_excl = [10, 23, 104, 150, 152, 170]
# From 2013:
# txt_file_num_excl = [26, 46, 50, 64, 82, 84, 89, 106, 
#                       121, 122, 123, 124, 
#                       132]
# From 2014:
# txt_file_num_excl = [5, 17, 34, 62, 65, 82, 86, 93, 96, 98, 106, 113, 123, 137]
# From 2015:
# txt_file_num_excl = [15, 21, 55, 57, 71, 75, 86, 94, 109]
# From 2016:
# txt_file_num_excl = [34, 
#                      36, 37, 55, 61, 62, 67, 68, 69, 82, 
#                       90, 91, 94, 97, 102, 103, 104, 
#                       109, 111, 115, 116]
# From 2017:
# txt_file_num_excl = [7, 15, 16, 23, 29, 45, 58, 61, 63, 65, 74, 
#                       87, 89, 95, 103, 105, 
#                       118, 119, 120, 121, 125, 126, 129, 130, 131, 
#                       134, 135, 136, 147, 151]
# From 2018:
# txt_file_num_excl = [19, 25, 35, 39, 48, 51, 53, 59, 62, 63, 65, 70, 
#                       78, 82, 83, 89, 91, 99, 102, 108, 109, 114, 116]
# From 2019:
# txt_file_num_excl = [0, 30, 37, 39, 40, 59, 66, 76, 78, 81, 
#                       90, 91, 92, 94, 100, 106, 108, 109, 122, 128]

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

import caser

# fields = 'all'
num_fields = 12
print_msg = True
appeals = caser.get_case_df(txt_file_list_sel, num_fields, print_msg)



##################################################
# Count the valid observations
##################################################


valid_counts = caser.count_valid_obsns(appeals)

# valid_counts.describe()

valid_counts[['case_code', 'circ_num', 'case_num']].describe()


valid_counts[['background', 'holdings_hdr', 'outcome', 
              'posture', 'judicial_panel']].describe()



##################################################
# Inspect the fields individually.
##################################################

print(num_files - len(txt_file_num_excl))


# Print selected fields to screen. 
appeals['file_name']
appeals['case_code']
is_valid = caser.is_case_code_vec(appeals['case_code'])['is_valid']
sum(is_valid)
appeals['case_code'][is_valid == False]


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

appeals[['file_name', 'case_num']][is_valid == False]


appeals['case_num_1']
appeals['case_num_2']
appeals['case_num_3']

appeals['num_case_nums'].describe()
appeals['num_case_nums'].value_counts()


appeals['case_num'][appeals['num_case_nums'] == 0]
appeals['case_num'][appeals['num_case_nums'] == 4]
appeals['case_num'][appeals['num_case_nums'] == 3]
appeals['case_num'][appeals['num_case_nums'] == 2]
# Some cases have suffixes (L) or (XAP)
# Some cases have trailing 3, 4, or 5 digits.

appeals['case_num_1'].describe()
appeals['case_num_2'].describe()
appeals['case_num_3'].describe()

# Save file of case numbers. 



appeals['case_date_1']
appeals['case_date_2']
appeals['case_date_3']
appeals['case_date_4']


appeals['background']
is_valid = caser.is_background_vec(appeals['background'])['is_valid']
sum(is_valid)
appeals['background'][is_valid == False].unique()
# Some are legitimately missing the background.
appeals[['file_name', 'background']][is_valid == False]



appeals['holdings_hdr']
is_valid = caser.is_holdings_hdr_vec(appeals['holdings_hdr'])['is_valid']
sum(is_valid)
appeals['holdings_hdr'][is_valid == False].unique()


appeals['outcome']
appeals['outcome'].unique()
is_valid = caser.is_outcome_vec(appeals['outcome'])['is_valid']
sum(is_valid)
appeals['outcome'][is_valid == False].unique()


# import caser


appeals['posture']
is_valid = caser.is_posture_vec(appeals['posture'])['is_valid']
sum(is_valid)
appeals['posture'][is_valid == False].unique()



appeals['judicial_panel']
is_valid = caser.is_panel_vec(appeals['judicial_panel'])['is_valid']
sum(is_valid)
appeals['judicial_panel'][is_valid == False].unique()

appeals[['file_name', 'judicial_panel']][is_valid == False]



appeals['judge_1']
appeals['judge_2']
appeals['judge_3']
appeals['judge_4']


appeals['num_judges'].value_counts()

appeals['judicial_panel'][appeals['num_judges'] == 0]
appeals['judicial_panel'][appeals['num_judges'] == 1]
appeals['judicial_panel'][appeals['num_judges'] == 2]
# Some names are separated by semicolons.
appeals['judicial_panel'][appeals['num_judges'] == 3]
appeals['judicial_panel'][appeals['num_judges'] == 4]
# Some judges have Jr. suffix. 
appeals['judicial_panel'][appeals['num_judges'] == 5]
# Some sentences happen to start with the word "Before".
appeals['judicial_panel'][appeals['num_judges'] == 6]
appeals['judicial_panel'][appeals['num_judges'] == 7]
appeals['judicial_panel'][appeals['num_judges'] == 8]
appeals['judicial_panel'][appeals['num_judges'] == 11]
appeals['judicial_panel'][appeals['num_judges'] == 15]

txt_file_num = 27 # Wordy titles.
# txt_file_num = 220 # Legit 7 judges.
txt_file_num = 139
txt_file = txt_file_list[txt_file_num]
case_info = caser.get_case_info(txt_file)
# caser.print_case_info(case_info)
case_info['judicial_panel']
case_info['judge_names']


appeals['judge_1'].describe()
appeals['judge_2'].describe()
appeals['judge_3'].describe()
appeals['judge_4'].describe()



##################################################
# Inspect individual cases
##################################################

import caser

# Choose a file and read the case information. 
# txt_file_num = 10 # In 2012, (Table) in case code.
txt_file_num = 152 # In 2012, In re complaint.
txt_file_num = 137 # In 2014, blank lines after date.  
txt_file_num = 7 # In 2017
txt_file_num = 0 # In 2019
txt_file_num = 114 # 32 # 22 # In 2002
txt_file_num = 0 # In 2003

txt_file_num = 109

# Read the information from this case.
txt_file = txt_file_list[txt_file_num]

print("Reading case information from file:")
print(txt_file)
print("")

# Get the dictionary of case info.
case_info = caser.get_case_info(txt_file)


caser.print_case_info(case_info)




import caser


# Run functions one at a time.
with open(txt_file, 'r', encoding = 'utf-16') as file:
    
    case_code = caser.get_case_code(file)
    print(case_code)
    circ_num = caser.get_circ_num(file)
    print(circ_num)
    (pla_appnt, def_appee, last_line) = caser.get_party_names(file)
    print(pla_appnt)
    print(def_appee)
    print(last_line)
    case_num = caser.get_case_num(file, last_line)
    print(case_num)
    (case_date, line) = caser.get_case_date(file)
    print(case_date)
    print(line)

##################################################
# Create data frame of strings from the judicial panel.
##################################################

import caser



##################################################
# Extra Code Snippets
##################################################





##################################################
# End
##################################################
