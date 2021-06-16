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
#   line with judicial panel. Done.
# TODO: Create master list of judges. 
# TODO: Create function that parses case numbers
#   to get list of numbers of case numbers related to each case. 
#   Return a list of case numbers. 
# 
# This version reads all years of data in one sample. 
#
##################################################
"""


##################################################
# Import Modules.
##################################################


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

# from caser import * # To read cases.
import caser # To read cases.



# Note:
# To change names of files.
# Append a prefix "2" for files 200+.
# for file in 20*.doc; do   newfile=2"$(echo "$file" | cut -c3-)";   mv "$file" "$newfile"; done
# 


##################################################
# Set paths for handling files.
# Translate a year of doc files to txt
##################################################

data_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\SH_Sample' 

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
# Append data from each year.
appeals = pd.DataFrame(columns = ['file_name', 'case_code', 'circ_num', 
                                      'pla_appnt_1', 'pla_appnt_2', 'pla_appnt_3', 
                                      'def_appee_1', 'def_appee_2', 'def_appee_3', 'def_appee_4',
                                      'case_num', 'case_num_list', 'num_case_nums', 
                                      'case_num_1', 'case_num_2', 'case_num_3',
                                      'case_date_1', 'case_date_2', 'case_date_3', 'case_date_4', 
                                      'background', 
                                      'holdings_hdr', 'outcome', 'posture', 
                                      'judicial_panel', 'judge_names', 'num_judges', 
                                      'judge_1', 'judge_2', 'judge_3', 'judge_4'])

for case_year in range(2000, 2019):
    print("Translating files for cases in year " + str(case_year))

    # Set the directory with data files.
    # doc_folder = data_folder + "\\Court_Docs_SH_LE_" + str(case_year) + '\\'
    # doc_path = drive_path + doc_folder
    
    # Set the directory with txt files after translation.
    txt_folder = data_folder + "\\Court_Docs_SH_LE_" + str(case_year) + '\\'
    txt_path = drive_path + txt_folder
    
    
    ##################################################
    # Translate this doc File to txt
    ##################################################
    
    # Translate them all at once.
    # It takes a few seconds each. 
    
    # # Initialize object for Word application
    # app = win32com.client.Dispatch('Word.Application')
    # app.Visible = True
    
    # # Translate all files in a folder.
    # caser.doc2txt_dir(app, doc_path, txt_path)
    
    
    
    # Get list of all files in a given directory sorted by name
    txt_file_list = sorted( filter( os.path.isfile,
                            glob.glob(txt_path + '*' + ".txt") ) )
    
    num_files = len(txt_file_list)
    txt_file_num_list = range(num_files)
    
    
    # Generate dataset from cases for each year.
    # fields = 'all'
    num_fields = 12
    print_msg = True
    appeals_sub = caser.get_case_df(txt_file_list, num_fields, print_msg)
    
    
    # Append into the full dataset. 
    appeals = appeals.append(appeals_sub)
    
    
    
    # End data collection.


type(appeals)
appeals.describe()

# Note that index is inherited from sub-data frames:
# Index restarts at zero each year and multiple rows have same index.
# Result is a series on each call of an "element".
appeals.index

# Fix this by replacing with a clean index. 
appeals.index = range(appeals.shape[0])

# Much better.
appeals.index



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

# print(num_files - len(txt_file_num_excl))


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

appeals['file_name'][is_valid == False]



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
appeals['judicial_panel'][appeals['num_judges'] == 9]
appeals['judicial_panel'][appeals['num_judges'] == 10]
appeals['judicial_panel'][appeals['num_judges'] == 11]
appeals['judicial_panel'][appeals['num_judges'] == 12]
appeals['judicial_panel'][appeals['num_judges'] == 13]
appeals['judicial_panel'][appeals['num_judges'] == 14]
appeals['judicial_panel'][appeals['num_judges'] == 15]
appeals['judicial_panel'][appeals['num_judges'] == 16]
appeals['judicial_panel'][appeals['num_judges'] == 18]

appeals['judicial_panel'][appeals['num_judges'] > 3]


appeals[['file_name', 'judicial_panel']][appeals['num_judges'] == 11]

# The panels with > 3 judges are "en banc" hearings, 
# after a reguler three-judge panel "makes a goofy decision". 
appeals[['circ_num', 'num_judges']][appeals['num_judges'] > 3].sort_values(by = 'circ_num')

appeals[['circ_num', 'num_judges']][appeals['num_judges'] == 2].sort_values(by = 'circ_num')





# Check list of circuit numbers.
appeals['circ_num'].unique()

appeals['circ_num'].value_counts()
circ_num_list = appeals['circ_num'].unique()
# These are consistent enough to use as a reliable group by variable. 


# Create a master table of judges. 
judge_list_cols = ['circ_num', 'judge_name']
judge_list = pd.DataFrame(columns = judge_list_cols)

# Stack all of the first three judges names and remove duplicates. 

is_valid = caser.is_panel_vec(appeals['judicial_panel'])['is_valid']
judge_list_sub = appeals[['circ_num', 'judge_1']][is_valid == True]
judge_list_sub.columns = judge_list_cols
judge_list = judge_list.append(judge_list_sub)

judge_list_sub = appeals[['circ_num', 'judge_2']][is_valid == True]
judge_list_sub.columns = judge_list_cols
judge_list = judge_list.append(judge_list_sub)

judge_list_sub = appeals[['circ_num', 'judge_3']][is_valid == True]
judge_list_sub.columns = judge_list_cols
judge_list = judge_list.append(judge_list_sub)



judge_list.index = range(judge_list.shape[0])


# Select unique judge names. 
# judge_list = judge_list.drop_duplicates()
# judge_list.index
# Now only 1863 judges total (includes position number, in error). 
# Now only 1154 judges total. 
# Down to 1010 after rmoving invalids and converting to upper case. 

# Instead, preserve number of appearances with a group_by.
judge_list['num'] = 1
judge_list = judge_list.groupby(['circ_num','judge_name'], as_index = False).sum()

judge_list.index
judge_list.columns


# Print out judge list by circuit number.
circ_num_sel = 'First Circuit'
judge_list[['circ_num','judge_name']][judge_list['circ_num'] == circ_num_sel].value_counts()


judge_list.sort_values(by=['circ_num','judge_name'], inplace = True)

judge_list.to_csv('judge_list.csv')

# # In 2000:
# txt_file_num = 224 # Legit 10 judges.
# txt_file_num = 260 # Legit 11 judges.
# txt_file_num = 300 # Legit 11 judges.
# txt_file_num = 191 # Legit 12 judges.

# txt_file_num = 109 # Extra numbers.
# txt_file_num = 213 # Extra numbers.



# # In 2001:
# txt_file_num = 284 # Legit 2 judges.
# txt_file_num = 81 # Legit 9 judges.
# txt_file_num = 19 # Legit 11 judges.
# txt_file_num = 130 # Legit 11 judges.

# txt_file_num = 99 # 2 *767 at end.

# In 2002:
# txt_file_num = 27 # Wordy titles.
# txt_file_num = 220 # Legit 7 judges.
# txt_file_num = 231 # Legit 2 judges.
# txt_file_num = 4 # Legit 11 judges. 
# txt_file_num = 180 # Legit 11 judges. 
# txt_file_num = 251 # Legit 10 judges. 
# txt_file_num = 226 # Legit 15 judges. 

# # In 2003:
# txt_file_num = 29 # Legit 2 judges.
# txt_file_num = 51 # Legit 2 judges.
# txt_file_num = 142 # Legit 2 judges.
# txt_file_num = 202 # Legit 10 judges.
# txt_file_num = 12 # Legit 12 judges.

# # In 2004:
# txt_file_num = 216 # Legit 11 judges.
# txt_file_num = 157 # Legit 13 judges.

# # In 2005:
# txt_file_num = 223 # Legit 2 judges.

# # In 2006:
# txt_file_num = 60 # Separated by "&".
# txt_file_num = 114 # Legit 11 judges.

# # In 2007:
# txt_file_num = 17 # Legit 10 judges.
# txt_file_num = 214 # Legit 11 judges.

# # In 2008:
# txt_file_num = 149 # Legit 2 judges.
# txt_file_num = 136 # Character '.a1' appended? Remove later?

# # In 2009:
# txt_file_num = 56 # Contains (Ret.).
# txt_file_num = 84 # Contains (Ret.).
# txt_file_num = 34 # Legit 11 judges.
# txt_file_num = 200 # Legit 16 judges.

# # In 2010:
# txt_file_num = 71 # Legit 2 judges.
# txt_file_num = 134 # Legit 2 judges.
# txt_file_num = 12 # Legit 11 judges.
# txt_file_num = 125 # Legit 11 judges.

# # In 2011:
# txt_file_num = 165 # Legit 2 judges.

# # In 2012:
# txt_file_num = 124 # Legit 18 judges!!!

# # In 2013:
# txt_file_num = 161 # Legit 11 judges.
# txt_file_num = 86 # Legit 14 judges!!!
# txt_file_num = 1 # Legit 16 judges!!!

# # In 2014:
# txt_file_num = 58 # Legit 11 judges.

# # In 2015:
# txt_file_num = 27 # Not a judicial panel. Remove sentences by list length?
# txt_file_num = 124 # Legit 15 judges.

# # In 2016:
# txt_file_num = 51 # Middle District.

# # In 2017:
# txt_file_num = 34 # Legit 11 judges.
# txt_file_num = 79 # Legit 11 judges.
# txt_file_num = 80 # Legit 11 judges.

# In 2018:
# All good except for zeros.
    
# In 2019:
txt_file_num = 97 # Legit 11 judges.


txt_file = txt_file_list[txt_file_num]
case_info = caser.get_case_info(txt_file)
# caser.print_case_info(case_info)
print(case_info['judicial_panel'])
print(case_info['judge_names'])


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

txt_file_num = 284

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
