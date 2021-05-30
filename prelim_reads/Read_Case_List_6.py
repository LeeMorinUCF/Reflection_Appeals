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


##################################################
# Set paths for handling files.
##################################################

# Set the directory with data files.
# doc_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Sample_Sex_Har_2011\\'
# doc_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Court_Docs_SH_LE_2011\\'
doc_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Court_Docs_SH_LE_2012\\'
doc_path = drive_path + doc_folder


# Set the directory with txt files after translation.
# txt_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Sample_Sex_Har_2011_txt\\'
# Place them in the same folder.
# txt_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Court_Docs_SH_LE_2011\\'
txt_folder = 'Research\\Appeals_Reflection\\Westlaw_Data\\Court_Docs_SH_LE_2012\\'
txt_path = drive_path + txt_folder





##################################################
# Select a File and Scrape Contents
##################################################

# Translate them all at once.
# It takes a few seconds each. 

# Initialize object for Word application
app = win32com.client.Dispatch('Word.Application')
app.Visible = True

# Translate all files in a folder.
caser.doc2txt_dir(app, doc_path, txt_path)




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


# Get list of all files in a given directory sorted by name
txt_file_list = sorted( filter( os.path.isfile,
                        glob.glob(txt_path + '*' + ".txt") ) )

num_files = len(txt_file_list)
txt_file_num_list = range(num_files)

# Initialize data frame.
appeals = pd.DataFrame(columns = ['file_name', 'case_code', 'circ_num', 
                                  'pla_appnt_1', 'pla_appnt_2', 'pla_appnt_3', 
                                  'def_appee_1', 'def_appee_2', 'def_appee_3', 'def_appee_4',
                                  'case_num', 
                                  'case_date_1', 'case_date_2', 'case_date_3', 'case_date_4', 
                                  'background', 
                                  'holdings_hdr', 'outcome', 'posture', 'judicial_panel'], 
                       index = txt_file_num_list)


# Exclude some files that are problematic. 
# txt_file_num_excl = [12, 15, 17]
# txt_file_num_excl = [12, 15]
txt_file_num_excl = [52, 116]
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
