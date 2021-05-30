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
#
##################################################
"""


##################################################
# Import Modules.
##################################################


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
    
    # The next name(s) should be the Plaintiff-Appellant.
    pla_appnt = []
    line = file.readline()
    # When the next line is "v.", list of Plaintiff-Appellants is complete.
    found_v = line.strip()[0] == "v"
    while not found_v:
        pla_appnt.append(line.replace("\n",""))
        line = file.readline()
        found_v = line.strip()[0] == "v"
    
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
    return(line[0] != '[' and line[0].strip() != '')

# Record the "Holdings" header statement.
def get_holdings(file):
    
    # Skip a blank line and initialize list.
    line = file.readline()
    holdings = []
    
    # The next line is the "Holdings" header statement.
    line = file.readline()
    holdings_hdr = line.replace("\n","")
    holdings.append(holdings_hdr)
    
    # Append the contents of the holdings. 
    finished_holdings = False
    while not finished_holdings:
        line = file.readline()
        finished_holdings = is_finished_holdings(line)
        # Record last line unless it is blank:
        # the last line is the outcome. 
        if line[0].strip() != '':
            holdings.append(line.replace("\n",""))
        
    return(holdings)

# Record the case outcome. 
def get_outcome(file):
    
    # Assumes the holdings were just passed.
    line = file.readline()
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


# Determine when file is read up to list of jurists. 
def is_jurists(line):
    
    # Reads over legal information util a line
    # that contains "Attorneys and Law Firms".
    line_list = line.split()
    return("Attorneys" in line_list or "Firms" in line_list)
    

# Determine when list of jurists is read up to judicial panel. 
def is_panel(line):
    
    # Reads over legal information util a line
    # that begins with "Before". 
    line_list = line.split()
    return(line_list[0].strip() == "Before" or line_list[0].strip() == "Before:")


# Record the names of lawyers, judges and previous case.
def get_jurist_list(file):
    
    found_jurists = False
    while not found_jurists:
        line = file.readline()
        found_jurists = is_jurists(line)
        # Don't record; skip to jurists. 
        
    # Now record the jurists in a list.
    jurist_list = []
    # The last line with the judicial panel
    # should begin with "Before". 
    
    found_panel = False
    while not found_panel:
        line = file.readline()
        found_panel = is_panel(line)
        # Regardless, add to list of jurists.
        jurist_list.append(line)
    
    return(jurist_list)



def get_case_info(txt_file):
    
    # Extract the fields from the file.
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
        
        # Record the list of holdings.
        holdings = get_holdings(file)
        # Record the "Holdings" header statement.
        holdings_hdr = holdings[0]
        # Record the case outcome. 
        outcome = holdings[-1]
        
        # Record the statement of "Procedural Posture(s)".
        posture = get_posture(file)
        
        # Record the names of lawyers, judges and previous case.
        jurist_list = get_jurist_list(file)
        # The first line is the council for the plaintiff-appellant.
        # pla_appnt_council = jurist_list[0]
        # The next line is the council for the defendant-appellee.
        # def_appee_council = jurist_list[1]
        # The last line is the judicial panel.
        judicial_panel = jurist_list[len(jurist_list) - 1]
        
        
    # Collect the fields into a dictionary.
    case_info = {
        "case_code":
        case_code,
        
        "circ_num":
        circ_num,
        
        "pla_appnt":
        pla_appnt,
        
        "def_appee":
        def_appee,
        
        "case_num":
        case_num,
        
        "case_date":
        case_date,
        
        "background":
        background,
        
        "holdings_hdr":
        holdings_hdr,
        
        "outcome":
        outcome,
        
        "posture":
        posture,
        
        "judicial_panel":
        judicial_panel
        
        }
        
    return(case_info)



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


file_num_list = []
case_code_list = []
circ_num_list = []
case_num_list = []

# Get list of all files in a given directory sorted by name
txt_file_list = sorted( filter( os.path.isfile,
                        glob.glob(txt_path + '*') ) )

# Some files are problematic. 
txt_file_num_excl = [12, 15, 17]

txt_file_num_list = range(len(txt_file_list))

# txt_file_num_list = txt_file_num_list[txt_file_num_list not in txt_file_num_excl]

for txt_file_num in txt_file_num_list:
    
    if txt_file_num not in txt_file_num_excl:
        
        # Read the information from this case.
        txt_file = txt_file_list[txt_file_num]
        
        print("Reading case information from file number" + str(txt_file_num))
        
        # Get the dictionary of case info.
        case_info = get_case_info(txt_file)
        
        # Collect specific fields for analysis. 
        file_num_list.append(txt_file_num)
        case_code_list.append(case_info["case_code"])
        circ_num_list.append(case_info["circ_num"])
        case_num_list.append(case_info["case_num"])
    


print("")
# Now inspect the contents. 
for txt_file_num in range(len(case_code_list)):
    # print("Case %d: Case code: %s" % (file_num_list[txt_file_num], 
    #               case_code_list[txt_file_num]))
    # print("Case %d: Circuit number: %s" % (file_num_list[txt_file_num], 
    #               circ_num_list[txt_file_num]))
    print("Case %d: Case number: %s" % (file_num_list[txt_file_num], 
                  case_num_list[txt_file_num]))







##################################################
# Extra Code Snippets
##################################################





##################################################
# End
##################################################
