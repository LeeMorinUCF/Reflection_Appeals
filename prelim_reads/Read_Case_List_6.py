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
# May 30, 2021
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
# TODO: Verify that fields are reading valid information 
#   (i.e. no wrong fields). 
# TODO: Create is_valid_field(line) functions to test at scale.
# TODO: Modify invalid fileds and iterate.
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
case_year = 2019

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
txt_file_num_excl = [0, 30, 37, 39, 40, 59, 66, 76, 78, 81, 
                     90, 91, 92, 94, 100, 106, 109, 122, 128]

# Fix the anomalies and add them back. 




# Initialize data frame.
appeals = pd.DataFrame(columns = ['file_name', 'case_code', 'circ_num', 
                                  'pla_appnt_1', 'pla_appnt_2', 'pla_appnt_3', 
                                  'def_appee_1', 'def_appee_2', 'def_appee_3', 'def_appee_4',
                                  'case_num', 
                                  'case_date_1', 'case_date_2', 'case_date_3', 'case_date_4', 
                                  'background', 
                                  'holdings_hdr', 'outcome', 'posture', 'judicial_panel'], 
                       index = txt_file_num_list)



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
        
        # Record the names of parties.
        # Plaintiff-Appellant:
        for party_num in range(3):
            party_var_name = "pla_appnt_" + str(party_num + 1)
            if party_num < len(case_info["pla_appnt"]):
                appeals[party_var_name][txt_file_num] = case_info["pla_appnt"][party_num]
            else:
                appeals[party_var_name][txt_file_num] = "NA"
        # Defendant-Appellee:
        for party_num in range(4):
            party_var_name = "def_appee_" + str(party_num + 1)
            if party_num < len(case_info["def_appee"]):
                appeals[party_var_name][txt_file_num] = case_info["def_appee"][party_num]
            else:
                appeals[party_var_name][txt_file_num] = "NA"
        
        
        appeals['case_num'][txt_file_num] = case_info["case_num"]
        
        # Dates are collected in a list.
        for date_num in range(4):
            date_var_name = "case_date_" + str(date_num + 1)
            if date_num < len(case_info["case_date"]):
                appeals[date_var_name][txt_file_num] = case_info["case_date"][date_num]
            else:
                appeals[date_var_name][txt_file_num] = "NA"
        
        
        appeals['background'][txt_file_num] = case_info["background"]
        
        appeals['holdings_hdr'][txt_file_num] = case_info["holdings_hdr"]
        appeals['outcome'][txt_file_num] = case_info["outcome"]
        appeals['posture'][txt_file_num] = case_info["posture"]
        appeals['judicial_panel'][txt_file_num] = case_info["judicial_panel"]
        











# Print selected fields to screen. 
appeals['file_name'][0:txt_file_num]
appeals['case_code'][0:txt_file_num]
appeals['circ_num'][0:txt_file_num]

appeals['pla_appnt_1'][0:txt_file_num]
appeals['pla_appnt_2'][0:txt_file_num]
appeals['pla_appnt_3'][0:txt_file_num]

appeals['def_appee_1'][0:txt_file_num]
appeals['def_appee_2'][0:txt_file_num]
appeals['def_appee_3'][0:txt_file_num]
appeals['def_appee_4'][0:txt_file_num]


appeals['case_num'][0:txt_file_num]

appeals['case_date_1'][0:txt_file_num]
appeals['case_date_2'][0:txt_file_num]
appeals['case_date_3'][0:txt_file_num]
appeals['case_date_4'][0:txt_file_num]


appeals['background'][0:txt_file_num]

appeals['holdings_hdr'][0:txt_file_num]
appeals['outcome'][0:txt_file_num]

appeals['posture'][0:txt_file_num]
appeals['judicial_panel'][0:txt_file_num]


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
