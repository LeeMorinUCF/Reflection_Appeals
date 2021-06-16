# -*- coding: utf-8 -*-
"""
##################################################
#
# Identification and Estimation in Judicial Panel Voting
# The caser Module
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
# This script is a module of function definitions.
# 
##################################################
"""

##################################################
# Import Modules.
##################################################

import os

import pandas as pd


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
        return((line_list[0].isdigit() and line_list[-1].isdigit())
               or (line_list[0].isdigit() and line_list[2].isdigit()))
    else:
        return False

# Vector version for data frame columns:
def is_case_code_vec(df_col): 
    
    test_vec = pd.DataFrame(columns = ['is_valid'], 
                           index = range(len(df_col)))
    for row in range(len(df_col)):
        test_row = is_case_code(df_col[row])
        # test_row = is_case_code(df_col.loc[:, row])
        test_vec['is_valid'][row] = test_row
        
    return(test_vec)

# Function to find and get the case code.
def get_case_code(file):

    # First look for the case code.
    found_case_code = False
    lines_read = 0
    while not found_case_code and lines_read < 20:
        line = file.readline()
        lines_read = lines_read + 1
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
    
    
def is_circ_num(line):
    line_list = line.split()
    if len(line_list) > 1:
        return(line_list[-1].strip().replace(".","") == "Circuit")
    else:
        return False

# Vector version for data frame columns:
def is_circ_num_vec(df_col): 
    
    test_vec = pd.DataFrame(columns = ['is_valid'], 
                           index = range(len(df_col)))
    for row in range(len(df_col)):
        test_row = is_circ_num(df_col[row])
        test_vec['is_valid'][row] = test_row
        
    return(test_vec)


# Record the circuit number.
def get_circ_num(file):
    
    # Assumes the case code was just recorded. 
    # The next line should be "United States Court of Appeals,"
    # Keep reading until then. 
    # found_uscoa = False
    found_circ_num = False
    lines_read = 0
    # while not found_uscoa and lines_read < 4:
    while not found_circ_num and lines_read < 6:
        line = file.readline()
        lines_read = lines_read + 1
        # found_uscoa = is_uscoa(line)
        found_circ_num = is_circ_num(line)
    
    # This line should be the circuit number,
    # if stopped as uscoa.
    # line = file.readline()
    
    # The present line should be the circuit number.
    # circ_num = line.split()[0]
    circ_num = line.replace("\n","")
    # Remove common strings to streamline circuit numbers.
    circ_num = circ_num.replace("United States Court of Appeals","")
    circ_num = circ_num.replace(".","")
    circ_num = circ_num.replace(",","")
    circ_num = circ_num.strip()
    
    return(circ_num)


# Get names of parties.
def get_party_names_depr(file):
    # DEPRECATED: Assumes parties are listed in one line each. 
    
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
    
# Determine if a valid Plaintiff-Appellant.
def is_pla_appnt(line):
    return('plaintiff' in line.lower() 
           or 'appellant' in line.lower()
           or 'petitioner' in line.lower())

# Vector version for data frame columns:
def is_pla_appnt_vec(df_col): 
    
    test_vec = pd.DataFrame(columns = ['is_valid'], 
                           index = range(len(df_col)))
    for row in range(len(df_col)):
        test_row = is_pla_appnt(df_col[row])
        test_vec['is_valid'][row] = test_row
        
    return(test_vec)


# Determine if a valid Defendant-Appellees.
def is_def_appee(line):
    return('defendant' in line.lower() 
           or 'appellee' in line.lower())

# Vector version for data frame columns:
def is_def_appee_vec(df_col): 
    
    test_vec = pd.DataFrame(columns = ['is_valid'], 
                           index = range(len(df_col)))
    for row in range(len(df_col)):
        test_row = is_def_appee(df_col[row])
        test_vec['is_valid'][row] = test_row
        
    return(test_vec)



# Get names of parties.
def get_party_names(file):
    
    # The next name(s) should be the Plaintiff-Appellant.
    pla_appnt = []
    line = file.readline()
    # When the next line is "v.", list of Plaintiff-Appellants is complete.
    # found_v = line.strip()[0] == "v"
    found_v = line.strip() == "v"
    # found_in_re = "in re" in line.lower()
    found_in_re = "in re" in line.lower()
    found_case_num = is_case_num(line)
    if found_in_re:
        pla_appnt_line = line.replace("\n","")
        pla_appnt.append(pla_appnt_line)
    lines_read = 0
    while not found_v and not found_in_re and not found_case_num and lines_read < 20:
        pla_appnt_line = line.replace("\n","")
        if not pla_appnt_line.strip() == 'and':
            pla_appnt.append(pla_appnt_line)
        line = file.readline()
        lines_read = lines_read + 1
        # found_v = line.strip()[0] == "v"
        found_v = line.strip() == "v"
        found_in_re = "in re" in line.lower()
        found_case_num = is_case_num(line)
    
    # The next name(s) should be the Defendant-Appellee.
    def_appee = []
    if not found_case_num:
        line = file.readline()
    
    # When the next line is a case number, the list of Defendant-Appellees is complete.
    found_case_num = is_case_num(line)
    lines_read = 0
    while not found_case_num and lines_read < 20:
        def_appee_line = line.replace("\n","")
        if not def_appee_line.strip() == 'and':
            def_appee.append(def_appee_line)
        line = file.readline()
        lines_read = lines_read + 1
        found_case_num = is_case_num(line)
    
    # The last line read should be the case_number. 
    last_line = line
    
    return( (pla_appnt, def_appee, last_line) )


# Record the case number.
def get_case_num_depr(file):
    # DEPRECATED: Assumes a single line for Defendant-Appellee.
    
    # Assumes names of parties was just recorded. 
    # The next line should be the case number.
    line = file.readline()
    case_num = line.replace("\n","")
    
    return(case_num)
    

# Determine whether this line contains a case number.
def is_case_num(line):
    # A case number either contains the word "Docket" or "No."
    line_list = line.split()
    is_docket_no_tag = "No." in line_list or "Nos." in line_list or "Docket" in line_list
    is_docket_no = line.strip().replace("\n","").replace("-cv","").replace("-","").isdigit() and "-" in line
    return(is_docket_no_tag or is_docket_no)

# Vector version for data frame columns:
def is_case_num_vec(df_col): 
    
    test_vec = pd.DataFrame(columns = ['is_valid'], 
                           index = range(len(df_col)))
    for row in range(len(df_col)):
        test_row = is_case_num(df_col[row])
        test_vec['is_valid'][row] = test_row
        
    return(test_vec)


# Record the case number, either from the file of the last line.
def get_case_num(file, last_line):
    # Assumes names of parties was just recorded. 
    
    # Revised to accommodate multiple lines for Defendant-Appellee.
    # Either the case number is already in the last line, or in the next. 
    if is_case_num(last_line):
        # The case number is already in the last line.
        case_num = last_line.replace("\n","")
    else:
        # The case number is in the next line in the file.
        line = file.readline()
        case_num = line.replace("\n","")
        
    return(case_num)

def is_case_num_str(sub_str):
    
    # Examples:
    # is_case_num_str('12-1234')
    # True
    # is_case_num_str('19-9999')
    # True
    # is_case_num_str('No. 12-1')
    # False
    # is_case_num_str('leagalbeagle')
    # False
    
    # Determines whether a string is of the form YY-1234.
    if len(sub_str) == 7:
        str_1 = sub_str[0:2]
        str_2 = sub_str[2]
        str_3 = sub_str[3:len(sub_str)]
        return(str_1.isdigit() and str_2 == "-" and str_3.isdigit())
    else:
        return(False)



# Get list of case numbers from case_num string. 
def get_case_num_list(case_num):
    
    # Examples:
    # get_case_num_list('No. 04-6363.')
    # ['04-6363']
    # get_case_num_list('No. 2004-6363.')
    # ['04-6363']
    # get_case_num_list('Docket No. 04-6363.')
    # ['04-6363']
    # get_case_num_list('Nos. 04-6363, 04-6364.')
    # ['04-6363', '04-6364']
    case_num_list = []
    
    # Loop through characters in string, looking for YY-1234 pattern. 
    for char_num in range(len(case_num)):
        sub_str = case_num[char_num:(char_num + 7)]
        if is_case_num_str(sub_str):
            case_num_list.append(sub_str)
    
    return(case_num_list)


def is_synopsis(line):
    
    line_list = line.split()
    if len(line_list) > 0:
        return(line_list[0].strip().replace(":","") == "Synopsis")
    else:
        return False



# Record the case date.
def get_case_date(file):
    
    # Assumes case number was just recorded. 
    # Sometimes there are multiple dates:
    # Submitted, Submitted and Argued, Filed.
    # Dates separated by a pipe (|).
    # After all dates is a line with the word "Synopsis".
    
    case_date = []
    found_synopsis = False
    found_jurists = False
    found_panel = False
    lines_read = 0
    while not found_synopsis and not found_jurists and not found_panel and lines_read < 9:
        line = file.readline()
        lines_read = lines_read + 1
        # line_list = line.split()
        # Check if the next line is "Synopsis".
        found_synopsis = is_synopsis(line)
        # Check if the next line is "Attorneys and Law Firms"
        found_jurists = is_jurists(line)
        # Check if the next line starts with "Before".
        found_panel = is_panel(line)
        # Skip the next line if it is a pipe (|) or otherwise blank.
        # line_blank = is_blank(line)
        line_blank = line.strip() == "|" or line.strip() == ""
        # if not found_synopsis and not found_jurists and not found_panel and line_list[0].strip() != "|":
        if not found_synopsis and not found_jurists and not found_panel and not line_blank:
            # The next line should be a date in text format.
            case_date.append(line.replace("\n",""))
    
    # Return one or all of the dates.
    # case_date = do_something_to(case_date)
    
    # Pass the line for directng subsequent fields.
    
    return((case_date, line))


# Determine whether line contains a "Background" paragraph.
def is_background(line):
    line_list = line.split()
    if len(line_list) > 0:
        return(line_list[0].strip().replace(":","") == "Background")
    else:
        return False

# Vector version for data frame columns:
def is_background_vec(df_col): 
    
    test_vec = pd.DataFrame(columns = ['is_valid'], 
                           index = range(len(df_col)))
    for row in range(len(df_col)):
        test_row = is_background(df_col[row])
        test_vec['is_valid'][row] = test_row
        
    return(test_vec)

    
# Record the background, a paragraph describing the case. 
def get_background(file, line):
    
    # Assumes the case date was just read. 
    # and that the previous line was the header "Synopsis".
    # Read the next line in all cases. 
    found_synopsis = is_synopsis(line)
    if found_synopsis:
        line = file.readline()
        background = line.replace("\n","")
    
    # The next line should be the "Background" paragraph.
    # Read until the background paragraph is found.
    # found_background = False
    # Check if this line is labeled background. 
    # If not, check the next line. 
    found_background = is_background(line)
    lines_read = 0
    while not found_background and lines_read < 1:
        line = file.readline()
        lines_read = lines_read + 1
        # Check if the next line begins with "Background".
        found_background =  is_background(line)
    
    # The next line should be the "Background" paragraph.
    if not found_synopsis:
        # Don't want to overwrite if it was recorded after "Synopsis".
        if found_background:
            background = line.replace("\n","")
        else:
            background = "NA"
    
    return(background)

def is_holdings_hdr_keyword(line_check):
    
    # Remove punctuation.
    line_check = line_check.replace("[","")
    line_check = line_check.replace("]","")
    line_check = line_check.replace("*","")
    line_check = line_check.lower()
    return(line_check == "holding"
           or line_check == "holdings"
           or line_check == "order"
           or line_check == "opinion"
           or line_check == "memorandum"
           or line_check == "unpublished"
           or line_check == "per"
           or line_check == "curiam")

# Determine whether line contains the verb "held".
def is_holdings_hdr(line):
    line_list = line.split()
    if len(line_list) > 0:
        line_check = line_list[0].strip().replace(":","")
        if is_holdings_hdr_keyword(line_check):
            return(True)
    # If the first word does not indicate a header, 
    # check the second word.
    if len(line_list) > 1:
        line_check = line_list[1].strip().replace(":","")
        return(is_holdings_hdr_keyword(line_check))
    else:
        return False

# Vector version for data frame columns:
def is_holdings_hdr_vec(df_col): 
    
    test_vec = pd.DataFrame(columns = ['is_valid'], 
                           index = range(len(df_col)))
    for row in range(len(df_col)):
        test_row = is_holdings_hdr(df_col[row])
        test_vec['is_valid'][row] = test_row
        
    return(test_vec)


# Determine whether line goes beyond list of holdings.
def is_finished_holdings(line):
    return(line[0] != '[' and line[0].strip() != '')


# Find the section entitled "West Haednotes".
def is_west_notes(line):
    line_list = line.split()
    if len(line_list) > 2:
        return(line_list[0].lower() == "west" and line_list[0].lower() == "headnotes")
    else:
        return False


# Record the "Holdings" header statement.
def get_holdings(file):
    
    # Skip a blank line and initialize list.
    line = file.readline()
    holdings = []
    
    # Skip lines to the holdings header.
    found_holdings_hdr = False
    # Stop if reached procedural posture or West Headnotes.
    found_posture = False
    found_west_notes = False
    lines_read = 0
    while (not found_holdings_hdr and not found_posture 
           and not found_west_notes and lines_read < 6):
        line = file.readline()
        lines_read = lines_read + 1
        # Check if the next line contains the verb "held".
        found_holdings_hdr =  is_holdings_hdr(line)
        # Check for items that should come after the header.
        found_posture =  is_posture(line)
        found_west_notes =  is_west_notes(line)
    
    
    # The next line is the "Holdings" header statement.
    holdings_hdr = line.replace("\n","")
    holdings.append(holdings_hdr)
    
    # Append the contents of the holdings. 
    finished_holdings = False
    lines_read = 0
    while (not finished_holdings and not found_posture 
           and not found_west_notes and lines_read < 20):
        line = file.readline()
        lines_read = lines_read + 1
        finished_holdings = is_finished_holdings(line)
        # Check for items that should come after the header.
        found_posture =  is_posture(line)
        found_west_notes =  is_west_notes(line)
        # Record last line unless it is blank:
        # the last line is the outcome. 
        if line[0].strip() != '':
            holdings.append(line.replace("\n",""))
        
    return(holdings)

def is_outcome(line):
    line_list = line.lower()
    return("affirm" in line_list
           or "reverse" in line_list
           or "vacate" in line_list
           or "remand" in line_list
           or "grant" in line_list
           or "deny" in line_list
           or "denied" in line_list
           or "dismiss" in line_list)

# Vector version for data frame columns:
def is_outcome_vec(df_col): 
    
    test_vec = pd.DataFrame(columns = ['is_valid'], 
                           index = range(len(df_col)))
    for row in range(len(df_col)):
        test_row = is_outcome(df_col[row])
        test_vec['is_valid'][row] = test_row
        
    return(test_vec)

# Record the case outcome. 
def get_outcome(file):
    # DEPRECATED: Appended to end of holdings.
    
    # Assumes the holdings were just passed.
    line = file.readline()
    # Record the case outcome. 
    outcome = line.replace("\n","")
    
    return(outcome)


# Determine if line begins with "Procedural Posture(s):".
def is_posture(line):
    
    # Reads over legal information util a line
    # that begins with "Procedural Posture(s):". 
    line_list = line.split()
    if line_list == [] or len(line_list) == 1:
        return(False)
    else:
        return(line_list[0].strip() == "Procedural" or 
               line_list[1].strip()[0:7] == "Posture")

# Vector version for data frame columns:
def is_posture_vec(df_col): 
    
    test_vec = pd.DataFrame(columns = ['is_valid'], 
                           index = range(len(df_col)))
    for row in range(len(df_col)):
        test_row = is_posture(df_col[row])
        test_vec['is_valid'][row] = test_row
        
    return(test_vec)


# Record the statement of "Procedural Posture(s):".
def get_posture(file):
    # Assumes the outcome was just recorded after holdings. 
    
    # Not all cases have procedural posture.
    # Most common configuration is a blak space
    # followed by a line that starts with "Procedural Posture(s):".
    
    # Initialize with what might be a blank line.
    line = file.readline() 
    found_posture = is_posture(line)
    # If we reach "West Headnotes", we've gone too far.
    found_west_notes = is_west_notes(line)
    lines_read = 0
    while not found_posture and not found_west_notes and lines_read < 7:
        line = file.readline()
        lines_read = lines_read + 1
        found_posture = is_posture(line)
        # Check that we didn't reach "West Headnotes".
        found_west_notes = is_west_notes(line)
    
    # The last should be the statement of "Procedural Posture(s)", 
    # if it is present.
    if found_posture:
        posture = line.replace("\n","")
    else:
        posture = "NA"
    
    return(posture)


# Determine when file is read up to list of jurists. 
def is_jurists(line):
    
    # Reads over legal information util a line
    # that contains "Attorneys and Law Firms".
    # line_list = line.split()
    # return("Attorneys" in line_list or "Firms" in line_list)
    return(line.strip() == "Attorneys and Law Firms" )
    

# Determine when list of jurists is read up to judicial panel. 
def is_panel(line):
    
    # Find the line with the judicial panel
    # should begin with "Before"
    # but could also start with "PRESENT:"
    # and include phrases like "Circuit Judge". 

    
    line_list = line.split()
    if line_list == []:
        return(False)
    elif len(line_list) > 1:
        # Sometimes there is a word present before "present" or before "Before".
        judge_hdr = (line_list[0].lower().strip()[0:6] == "before"
            or line_list[1].lower().strip()[0:6] == "before"
            or line_list[0].lower().strip()[0:7] == "present"
            or line_list[1].lower().strip()[0:7] == "present")
        contains_judge = "judge" in  line.lower()
        return(judge_hdr and contains_judge)
    else:
        return(False)

# Vector version for data frame columns:
def is_panel_vec(df_col): 
    
    test_vec = pd.DataFrame(columns = ['is_valid'], 
                           index = range(len(df_col)))
    for row in range(len(df_col)):
        test_row = is_panel(df_col[row])
        test_vec['is_valid'][row] = test_row
        
    return(test_vec)


# Record the names of lawyers, judges and previous case.
def get_jurist_list(file, line):
    
    # found_jurists = False
    # found_panel = False
    found_jurists = is_jurists(line)
    found_panel = is_panel(line)
    lines_read = 0
    while not found_jurists and not found_panel and lines_read < 500:
        line = file.readline()
        lines_read = lines_read + 1
        found_jurists = is_jurists(line)
        # Don't record the commentary in between; skip to jurists. 
        # Unless there is no heading "Attorneys and Law Firms".
        # In that case, stop at the judicial panel: 
        # a line that starts with "Before".
        found_panel = is_panel(line)
    
    
    # Now record the jurists in a list.
    jurist_list = []
    
    # If the panel is found before "Attorneys and Law Firms", 
    # then pad the list with missing names. 
    if found_panel:
        # The council for the plaintiff-appellant is missing.
        jurist_list.append("NA")
        # The council for the defendant-appellee is missing.
        jurist_list.append("NA")
        # If the panel has already been found, 
        # then only that one line remains.  
        jurist_list.append(line)
        
    
    # Otherwise, record the names of "Attorneys and Law Firms", 
    # along with the jucual panel, if reported.
    # The last line with the judicial panel
    # should begin with "Before"
    # but could also start with "PRESENT:"
    # and include phrases like "Circuit Judge". 
    
    lines_read = 0
    while not found_panel and lines_read < 10:
        line = file.readline()
        lines_read = lines_read + 1
        # print("line = " + line)
        found_panel = is_panel(line)
        # Regardless, add to list of jurists.
        jurist_list.append(line)
    
    return(jurist_list)



# Separate elements of line into list of 
# judges' names and titles.
def get_judge_names(line):
    
    # Examples:
    # get_judge_names("Before LUCERO, EBEL, and MURPHY, Circuit Judges.")
    # ['UCERO', 'EBEL', 'MURPHY']
    # get_judge_names("Before: LUCERO, EBEL, and MURPHY, Circuit Judges.")
    # ['UCERO', 'EBEL', 'MURPHY']
    # get_judge_names("Present: LUCERO, EBEL, and MURPHY, Circuit Judges.")
    # ['UCERO', 'EBEL', 'MURPHY']
    # get_judge_names("Before: MERRITT, ROGERS, and WHITE, Circuit Judges.")
    # ['MERRITT', 'ROGERS', 'WHITE']
    # get_judge_names("Before: J. W. MERRITT, ROGERS, and WHITE, Circuit Judges.")
    # ['J. W. MERRITT', 'ROGERS', 'WHITE']
    # get_judge_names("Before: J. W. MERRITT, W. B. ROGERS, and WHITE, Circuit Judges.")
    # ['J. W. MERRITT', 'W. B. ROGERS', 'WHITE']
    
    panel_list = []
    
    if not is_panel(line):
        return(panel_list)
    # Before anything else,
    # move past string "Before:",  "Before", or  "Present:"
    hdr_end_1 = line.lower().find('before:') + 7
    hdr_end_2 = line.lower().find('before') + 6
    hdr_end_3 = line.lower().find('present:') + 8
    hdr_end_4 = line.lower().find('present') + 7
    hdr_end = max(hdr_end_1, hdr_end_2, hdr_end_3, hdr_end_4)
    
    judge_line = line[hdr_end:(len(line))]
    
    # Next is to find commas, take next substring, 
    # verigy that it is not a judge's title, 
    # then append the judge's name to the list
    # and trim it from the string. 
    while len(judge_line) > 0:
        
        # Find the next comma, semicolon, or " and ", if any.
        next_comma = judge_line.find(',')
        next_semicolon = judge_line.find(';')
        next_and = judge_line.find(' and ')
        next_amp = judge_line.find(' & ')
        # If no other bounds, then remaining string might be the last judge.
        next_bound = find_next_bound(next_comma, next_semicolon, next_and, next_amp)
        # max_bound = max(next_comma, next_semicolon, next_and)
        if next_bound == -1:
            # No other bounds. 
            # Append last string, if it is not a title.
            # if not is_judge_title(judge_line):
            #     clean_str = judge_line.replace("\n","").replace(".","")
            #     clean_str = clean_str.replace(" and ","").strip()
            #     panel_list.append(clean_str)
            # Append last string, removing any titles and special characters.
            clean_str = clean_judge_name(judge_line)
            # clean_str = judge_line.replace("\n","").replace(".","")
            # clean_str = clean_str.replace("Judges","")
            # clean_str = clean_str.replace("Judge","")
            # clean_str = clean_str.replace("Circuit","")
            # clean_str = clean_str.replace("District","")
            # clean_str = clean_str.replace("Chief","")
            # clean_str = clean_str.replace("*","")
            # clean_str = clean_str.replace(" and ","").strip()
            # If there is anything left, append the judge's name. 
            # if len(clean_str) > 0 and not clean_str.isdigit():
            #     panel_list.append(clean_str)
            # Now the line is empty.
            judge_line = ''
        else:
            next_str = judge_line[0:next_bound]
            # Append next string, if it is not a title.
            # if not is_judge_title(next_str):
            #     clean_str = next_str.replace(",","")
            #     clean_str = clean_str.replace(";","")
            #     clean_str = clean_str.replace(" and ","").strip()
            #     if len(clean_str) > 0:
            #         # Maybe the string is ", and " -> "", so should be skipped.
            #         panel_list.append(clean_str)
            # Append last string, removing any titles and special characters.
            clean_str = clean_judge_name(next_str)
            # clean_str = next_str.replace("Judges","")
            # clean_str = clean_str.replace("Judge","")
            # clean_str = clean_str.replace("Circuit","")
            # clean_str = clean_str.replace("District","")
            # clean_str = clean_str.replace("Chief","")
            # clean_str = clean_str.replace("*","")
            # # Remove punctuation marks and bounds. 
            # clean_str = clean_str.replace(",","")
            # clean_str = clean_str.replace(";","")
            # clean_str = clean_str.replace(" and ","").strip()
            # If there is anything left, append the judge's name. 
            # if len(clean_str) > 0 and not clean_str.isdigit():
            #     panel_list.append(clean_str)
            # Trim this string from the line.
            judge_line = judge_line[next_bound:len(judge_line)]
            
        if len(clean_str) > 0 and not clean_str.isdigit():
            if clean_str.lower() == 'jr':
                # Append the suffix to the previous judge. 
                panel_list[len(panel_list) - 1] = panel_list[len(panel_list) - 1] + ", Jr."
            elif len(clean_str.split()) < 5:
                # Longer list of strings is probably a sentence and not a name:
                # Likely an incorrectly classified judicial panel. 
                # Otherwise, record the name of the next judge.
                panel_list.append(clean_str)
        
    
    # Then pull values in between. 
    
    
    return(panel_list)


def clean_judge_name(judge_str):
    
    # Pad with spaces. 
    clean_str = " " + judge_str + " "
    
    # Remove judge titles.
    clean_str = clean_str.replace("Judges"," ")
    clean_str = clean_str.replace("Judge"," ")
    clean_str = clean_str.replace("Justice"," ")
    clean_str = clean_str.replace("Circuit"," ")
    clean_str = clean_str.replace("District"," ")
    clean_str = clean_str.replace("Chief"," ")
    clean_str = clean_str.replace("Associate"," ")
    clean_str = clean_str.replace("Senior"," ")
    clean_str = clean_str.replace("Supreme"," ")
    clean_str = clean_str.replace("Hon"," ")
    clean_str = clean_str.replace("Honorable"," ")
    clean_str = clean_str.replace("Retired"," ")
    clean_str = clean_str.replace("(Ret.)"," ")
    clean_str = clean_str.replace("En banc"," ")
    
    # Remove other terminology. 
    clean_str = clean_str.replace("U.S."," ")
    clean_str = clean_str.replace("United States"," ")
    clean_str = clean_str.replace("Court"," ")
    clean_str = clean_str.replace("Appeals"," ")
    clean_str = clean_str.replace("International Trade"," ")
    clean_str = clean_str.replace("sitting by designation"," ")
    
    # Remove names or locations of courts.
    clean_str = clean_str.replace("First"," ")
    clean_str = clean_str.replace("Second"," ")
    clean_str = clean_str.replace("Third"," ")
    clean_str = clean_str.replace("Fourth"," ")
    clean_str = clean_str.replace("Fifth"," ")
    clean_str = clean_str.replace("Sixth"," ")
    clean_str = clean_str.replace("Seventh"," ")
    clean_str = clean_str.replace("Eighth"," ")
    clean_str = clean_str.replace("Ninth"," ")
    clean_str = clean_str.replace("Tenth"," ")
    clean_str = clean_str.replace("Eleventh"," ")
    clean_str = clean_str.replace("Twelfth"," ")
    
    clean_str = clean_str.replace("Northern"," ")
    clean_str = clean_str.replace("Southern"," ")
    clean_str = clean_str.replace("Eastern"," ")
    clean_str = clean_str.replace("Western"," ")
    clean_str = clean_str.replace("Middle"," ")
    clean_str = clean_str.replace("Maryland"," ")
    clean_str = clean_str.replace("West Virginia"," ")
    clean_str = clean_str.replace("Virginia"," ")
    clean_str = clean_str.replace("North Carolina"," ")
    clean_str = clean_str.replace("South Carolina"," ")
    
    # Remove common words.
    clean_str = clean_str.replace(" for "," ")
    clean_str = clean_str.replace(" of "," ")
    clean_str = clean_str.replace(" the "," ")
    
    
    # Remove line endings and special characters.
    clean_str = clean_str.replace("\n"," ").replace("."," ")
    clean_str = clean_str.replace("*"," ")
    
    # Remove punctuation marks and bounds. 
    clean_str = clean_str.replace(","," ")
    clean_str = clean_str.replace(";"," ")
    clean_str = clean_str.replace(" and ","")
    clean_str = clean_str.replace(" & ","")
    
    # Remove digits. 
    for i in range(10):
        clean_str = clean_str.replace(str(i)," ")
    
    
    # Strip the spaces produced by all of the above exclusions.
    clean_str = clean_str.strip()
    
    # Finally, return name in upper case to avoid unnecessary duplicates.
    clean_str = clean_str.upper()
    
    return(clean_str)
    

def find_next_bound(next_comma, next_semicolon, next_and, next_amp):
    
    # Find the index of the next bound between strings. 
    # Index skips over the boundary, 
    # which matters if it is more than a punctuation mark.
    # 
    # Examples:
    # find_next_bound(next_comma = -1, next_semicolon = 3, next_and = 5, next_amp = -1)
    # 4
    # find_next_bound(next_comma = -1, next_semicolon = -1, next_and = -1, next_amp = -1)
    # -1
    # find_next_bound(next_comma = -1, next_semicolon = 5, next_and = 2, next_amp = -1)
    # 6
    # find_next_bound(next_comma = -1, next_semicolon = 7, next_and = 2, next_amp = -1)
    # 7
    
    # If none of the strings are found, return -1.
    if max(next_comma, next_semicolon, next_and, next_amp) == -1:
        next_bound = -1
    else:
        # Find the smallest index among all that are not -1.
        if next_comma == -1:
            next_comma_bound = 999
        else:
            next_comma_bound = next_comma + 1
    
        if next_semicolon == -1:
            next_semicolon_bound = 999
        else:
            next_semicolon_bound = next_semicolon + 1
    
        if next_and == -1:
            next_and_bound = 999
        else:
            next_and_bound = next_and + 5
    
        if next_amp == -1:
            next_amp_bound = 999
        else:
            next_amp_bound = next_amp + 3
        
        next_bound = min(next_comma_bound, next_semicolon_bound, next_and_bound, next_amp_bound)
    
    
    return(next_bound)

# # Returns a list of judges' names. 
# def get_judge_names(panel_list):
    
#     # Loops through a list of strings
#     # and returns a string of *hopefully three*
#     # strings that are names of judges. 
    
#     judge_list = []
#     for panel_str in panel_list:
#         if not is_judge_title(panel_str):
#             # This should be the name of a judge.
#             # Append it to the list. 
#             judge_list.append(panel_str)
    
#     return(judge_list)
    
    



    
    
# Determine whether a string is one of the common judicial titles.
def is_judge_title(panel_str):
    
    found_judge_title = False
    
    found_judge_title = found_judge_title or "judge" in panel_str.lower()
    found_judge_title = found_judge_title or "circuit" in panel_str.lower()
    found_judge_title = found_judge_title or "chief" in panel_str.lower()

    
    return(found_judge_title)




# Function that identifies which field(s) match(es) a line, if any.
def which_field(line):
    
    field_names = []
    
    if is_case_code(line):
        field_names.append('case_code')
    
    if is_uscoa(line):
        field_names.append('uscoa')
    
    if is_circ_num(line):
        field_names.append('circ_num')
    
    if is_pla_appnt(line):
        field_names.append('pla_appnt')
    
    if is_def_appee(line):
        field_names.append('def_appee')
    
    if is_case_num(line):
        field_names.append('case_num')
    
    if is_synopsis(line):
        field_names.append('synopsis')
    
    if is_background(line):
        field_names.append('background')
    
    if is_holdings_hdr(line):
        field_names.append('holdings_hdr')
    
    if is_outcome(line):
        field_names.append('outcome')
    
    if is_posture(line):
        field_names.append('posture')
    
    if is_jurists(line):
        field_names.append('jurists')
    
    if is_panel(line):
        field_names.append('panel')
    
    return(field_names)





def get_case_info(txt_file, fields = 'all'):
    
    # This version records only selected fields.
    # Note the restriction that only consecutive ordering 
    # of fields is permitted.
    # Earlier fileds must be included for later fields to work.
    
    # Extract the fields from the file.
    with open(txt_file, 'r', encoding = 'utf-16') as file:
        
        # Record the case code. 
        if 'all' in fields or 'case_code' in fields:
            case_code = get_case_code(file)
        else:
            case_code = "NA"
        
        # Record the circuit number.
        if 'all' in fields or 'circ_num' in fields:
            circ_num = get_circ_num(file)
        else:
            circ_num = "NA"
        
        # Record the names of parties.
        # (pla_appnt, def_appee) = get_party_names(file)
        if 'all' in fields or 'pla_appnt' in fields or 'def_appee' in fields:
            (pla_appnt, def_appee, last_line) = get_party_names(file)
        else:
            pla_appnt = ["NA"]
            def_appee = ["NA"]
        
        # Record the case number.
        # case_num = get_case_num(file)
        if 'all' in fields or 'case_num' in fields:
            case_num = get_case_num(file, last_line)
            case_num_list = get_case_num_list(case_num)
        else:
            case_num = "NA"
            case_num_list = get_case_num_list(case_num)
        
        # Record the case date.
        if 'all' in fields or 'case_date' in fields:
            # case_date = get_case_date(file)
            (case_date, line) = get_case_date(file)
        else:
            case_date = ["NA"]
        
        # Some cases jump to "Attornies and Law Firms"
        # immediately after date.
        # These typically have "per curiam" decisions. 
        found_jurists = is_jurists(line)
        if not found_jurists:
            # This is a usual case with synopsis, background,
            # posture and holdings. 
            
            
            # Record the background, a paragraph describing the case. 
            if 'all' in fields or 'background' in fields:
                background = get_background(file, line)
            else:
                background = "NA"
            
            # Record the list of holdings.
            if 'all' in fields or 'outcome' in fields or 'holdings_hdr' in fields:
                holdings = get_holdings(file)
                # Record the "Holdings" header statement.
                holdings_hdr = holdings[0]
                # Record the case outcome. 
                outcome = holdings[-1]
            else:
                holdings_hdr = "NA"
                outcome = "NA"
                
            # Record the statement of "Procedural Posture(s)".
            if 'all' in fields or 'posture' in fields:
                posture = get_posture(file)
            else:
                posture = "NA"
        else:
            # Per curiam fields excludes these fields. 
            background = "NA"
            holdings_hdr = "NA"
            outcome = "NA"
            posture = "NA"
            # We might have to investigate these types of cases
            # to add some logic to retrieve these fields.
        
        # Record the names of lawyers, judges and previous case.
        if 'all' in fields or 'judicial_panel' in fields:
            jurist_list = get_jurist_list(file, line)
            # The first line is the council for the plaintiff-appellant.
            # pla_appnt_council = jurist_list[0]
            # The next line is the council for the defendant-appellee.
            # def_appee_council = jurist_list[1]
            # The last line is the judicial panel.
            judicial_panel = jurist_list[len(jurist_list) - 1]
            judge_names = get_judge_names(judicial_panel)
        else:
            judicial_panel = "NA"
            judge_names = get_judge_names(judicial_panel)
            
        
            
        
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
        
        "case_num_list":
        case_num_list,
        
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
        judicial_panel, 
        
        "judge_names":
        judge_names
        
        }
        
    return(case_info)

def print_case_info(case_info):
    
    
    # Print the results.
    print("case_code = ")
    print(case_info["case_code"])
    
    print("circ_num = ")
    print(case_info["circ_num"])
    
    print("pla_appnt = ")
    print(case_info["pla_appnt"])
    
    print("def_appee = ")
    print(case_info["def_appee"])
    
    print("case_num = ")
    print(case_info["case_num"])
    
    print("case_num_list = ")
    print(case_info["case_num_list"])
    
    print("case_date = ")
    print(case_info["case_date"])
    
    print("background = ")
    print(case_info["background"])
    
    print("holdings_hdr = ")
    print(case_info["holdings_hdr"])
    
    print("outcome = ")
    print(case_info["outcome"])
    
    print("posture = ")
    print(case_info["posture"])
    
    print("judicial_panel = ")
    print(case_info["judicial_panel"])
    
    print("judge_names = ")
    print(case_info["judge_names"])
    

# Get data frame of case info from list of case files. 
def get_case_df(txt_file_list, num_fields, print_msg):
    
    # Loop over text file list.
    num_files = len(txt_file_list)
    txt_file_num_list = range(num_files)
    
    # Record field listed in order. 
    field_list = ['file_name', 'case_code', 'circ_num', 
          'pla_appnt', 
          'def_appee',
          'case_num', 
          'case_date', 
          'background', 
          'holdings_hdr', 'outcome', 'posture', 'judicial_panel', 
          'judge_names']
    
    fields = []
    for field_num in range(min(num_fields, len(field_list))):
        fields.append(field_list[field_num])
    
    if print_msg:
        print("List of fields:")
        print(fields)
    
    
    # Initialize data frame.
    # Same fields in the data frame, regardless.
    appeals = pd.DataFrame(columns = ['file_name', 'case_code', 'circ_num', 
                                      'pla_appnt_1', 'pla_appnt_2', 'pla_appnt_3', 
                                      'def_appee_1', 'def_appee_2', 'def_appee_3', 'def_appee_4',
                                      'case_num', 'case_num_list', 'num_case_nums', 
                                      'case_num_1', 'case_num_2', 'case_num_3',
                                      'case_date_1', 'case_date_2', 'case_date_3', 'case_date_4', 
                                      'background', 
                                      'holdings_hdr', 'outcome', 'posture', 
                                      'judicial_panel', 'judge_names', 'num_judges', 
                                      'judge_1', 'judge_2', 'judge_3', 'judge_4'], 
                           index = txt_file_num_list)
    
    for txt_file_num in txt_file_num_list:
        
        
        # Read the information from this case.
        txt_file = txt_file_list[txt_file_num]
        
        # Isolate the file name and primt a message.
        if print_msg:
            txt_file_name = os.path.split(txt_file)[1]
            print("Reading case information from file " + "'" +  txt_file_name + "'")
        
        
        # Get the dictionary of case info.
        case_info = get_case_info(txt_file, fields)
        
        
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
        
        # There may be multiple case numbers for related cases. 
        appeals['case_num'][txt_file_num] = case_info["case_num"]
        appeals['case_num_list'][txt_file_num] = case_info["case_num_list"]
        appeals['num_case_nums'][txt_file_num] = len(case_info["case_num_list"])
        # Case numbers are collected in a list.
        for case_num_num in range(3):
            case_num_var_name = "case_num_" + str(case_num_num + 1)
            if case_num_num < len(case_info["case_num_list"]):
                appeals[case_num_var_name][txt_file_num] = case_info["case_num_list"][case_num_num]
            else:
                appeals[case_num_var_name][txt_file_num] = "NA"
        
        
        
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
        
        # Colect names of *hopefully three* judges (last column should be blank).
        appeals['judicial_panel'][txt_file_num] = case_info["judicial_panel"]
        appeals['judge_names'][txt_file_num] = case_info["judge_names"]
        appeals['num_judges'][txt_file_num] = len(case_info["judge_names"])
        # Record the names of the judges in separate fields.
        for judge_num in range(4):
            judge_var_name = "judge_" + str(judge_num + 1)
            if judge_num < len(case_info["judge_names"]):
                appeals[judge_var_name][txt_file_num] = case_info["judge_names"][judge_num]
            else:
                appeals[judge_var_name][txt_file_num] = "NA"
        
    return(appeals)



# Count the valid observations
def count_valid_obsns(appeals):
    
    valid_counts = pd.DataFrame(columns = ['file_name', 'case_code', 'circ_num', 
                                      # 'pla_appnt_1', 'pla_appnt_2', 'pla_appnt_3', 
                                      # 'def_appee_1', 'def_appee_2', 'def_appee_3', 'def_appee_4',
                                      'case_num', 
                                      # 'case_date_1', 'case_date_2', 'case_date_3', 'case_date_4', 
                                      'background', 
                                      'holdings_hdr', 'outcome', 'posture', 'judicial_panel'], 
                           index = appeals.index)
    
    valid_counts['file_name'] = appeals['file_name']
    valid_counts['case_code'] = is_case_code_vec(appeals['case_code'])
    # valid_counts['case_code'] = is_case_code_vec(appeals.ix[:, 'case_code'])
    valid_counts['circ_num'] = is_circ_num_vec(appeals['circ_num'])
    valid_counts['case_num'] = is_case_num_vec(appeals['case_num'])
    valid_counts['background'] = is_background_vec(appeals['background'])
    valid_counts['holdings_hdr'] = is_holdings_hdr_vec(appeals['holdings_hdr'])
    valid_counts['outcome'] = is_outcome_vec(appeals['outcome'])
    valid_counts['posture'] = is_posture_vec(appeals['posture'])
    valid_counts['judicial_panel'] = is_panel_vec(appeals['judicial_panel'])

    
    return(valid_counts)

##################################################
# End
##################################################


