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
        return(line_list[0].isdigit() and line_list[-1].isdigit())
    else:
        return False

# Vector version for data frame columns:
def is_case_code_vec(df_col): 
    
    test_vec = pd.DataFrame(columns = ['is_valid'], 
                           index = range(len(df_col)))
    for row in range(len(df_col)):
        test_row = is_case_code(df_col[row])
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
    found_v = line.strip()[0] == "v"
    lines_read = 0
    while not found_v and lines_read < 20:
        pla_appnt_line = line.replace("\n","")
        if not pla_appnt_line.strip() == 'and':
            pla_appnt.append(pla_appnt_line)
        line = file.readline()
        lines_read = lines_read + 1
        found_v = line.strip()[0] == "v"
    
    # The next name(s) should be the Defendant-Appellee.
    def_appee = []
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
    return("No." in line_list or "Nos." in line_list or "Docket" in line_list)

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
    lines_read = 0
    while not found_synopsis and lines_read < 9:
        line = file.readline()
        lines_read = lines_read + 1
        line_list = line.split()
        # Check if the next line is "Synopsis".
        found_synopsis =  is_synopsis(line)
        # Skip the next line if it is a pipe (|).
        if not found_synopsis and line_list[0].strip() != "|":
            # The next line should be a date in text format.
            case_date.append(line.replace("\n",""))
    
    # Return one or all of the dates.
    # case_date = do_something_to(case_date)
    
    return(case_date)


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
def get_background(file):
    
    # Assumes the case date was just read. 
    # and that the previous line was the header "Synopsis".
    # line = file.readline()
    
    # The next line should be the "Background" paragraph.
    # Read until the background paragraph is found.
    found_background = False
    lines_read = 0
    while not found_background and lines_read < 3:
        line = file.readline()
        lines_read = lines_read + 1
        # Check if the next line begins with "Background".
        found_background =  is_background(line)
    
    # The next line should be the "Background" paragraph.
    if found_background:
        background = line.replace("\n","")
    else:
        background = "NA"
    
    return(background)

def is_holdings_hdr_keyword(line_check):
    
    # Remove puctuation.
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

# Record the "Holdings" header statement.
def get_holdings(file):
    
    # Skip a blank line and initialize list.
    line = file.readline()
    holdings = []
    
    # Skip lines to the holdings header.
    found_holdings_hdr = False
    lines_read = 0
    while not found_holdings_hdr and lines_read < 4:
        line = file.readline()
        lines_read = lines_read + 1
        # Check if the next line contains the verb "held".
        found_holdings_hdr =  is_holdings_hdr(line)
    
    
    # The next line is the "Holdings" header statement.
    holdings_hdr = line.replace("\n","")
    holdings.append(holdings_hdr)
    
    # Append the contents of the holdings. 
    finished_holdings = False
    lines_read = 0
    while not finished_holdings and lines_read < 20:
        line = file.readline()
        lines_read = lines_read + 1
        finished_holdings = is_finished_holdings(line)
        # Record last line unless it is blank:
        # the last line is the outcome. 
        if line[0].strip() != '':
            holdings.append(line.replace("\n",""))
        
    return(holdings)

# Record the case outcome. 
def get_outcome(file):
    # Deprecated: Appended to end of holdings.
    
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



# Record the statement of "Procedural Posture(s):".
def get_posture(file):
    # Assumes the outcome was just recorded after holdings. 
    
    # Not all cases have procedural posture.
    # Most common configuration is a blak space
    # followed by a line that starts with "Procedural Posture(s):".
    
    # Initialize with what might be a blank line.
    line = file.readline() 
    found_posture = is_posture(line)
    lines_read = 0
    while not found_posture and lines_read < 6:
        line = file.readline()
        lines_read = lines_read + 1
        found_posture = is_posture(line)
    
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
    line_list = line.split()
    return("Attorneys" in line_list or "Firms" in line_list)
    

# Determine when list of jurists is read up to judicial panel. 
def is_panel(line):
    
    # Reads over legal information util a line
    # that begins with "Before". 
    line_list = line.split()
    if line_list == []:
        return(False)
    elif len(line_list) > 1:
        # Sometimes there is a word before "Before".
        return(line_list[0].strip()[0:6] == "Before" \
               or line_list[1].strip()[0:6] == "Before")
    else:
        return(False)


# Record the names of lawyers, judges and previous case.
def get_jurist_list(file):
    
    found_jurists = False
    found_panel = False
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
    # should begin with "Before". 
    
    lines_read = 0
    while not found_panel and lines_read < 5:
        line = file.readline()
        lines_read = lines_read + 1
        # print("line = " + line)
        found_panel = is_panel(line)
        # Regardless, add to list of jurists.
        jurist_list.append(line)
    
    return(jurist_list)




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
        else:
            case_num = "NA"
        
        # Record the case date.
        if 'all' in fields or 'case_date' in fields:
            case_date = get_case_date(file)
        else:
            case_date = ["NA"]
        
        # Record the background, a paragraph describing the case. 
        if 'all' in fields or 'background' in fields:
            background = get_background(file)
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
        
        # Record the names of lawyers, judges and previous case.
        if 'all' in fields or 'judicial_panel' in fields:
            jurist_list = get_jurist_list(file)
            # The first line is the council for the plaintiff-appellant.
            # pla_appnt_council = jurist_list[0]
            # The next line is the council for the defendant-appellee.
            # def_appee_council = jurist_list[1]
            # The last line is the judicial panel.
            judicial_panel = jurist_list[len(jurist_list) - 1]
        else:
            judicial_panel = "NA"
            
        
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
          'holdings_hdr', 'outcome', 'posture', 'judicial_panel']
    
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
                                      'case_num', 
                                      'case_date_1', 'case_date_2', 'case_date_3', 'case_date_4', 
                                      'background', 
                                      'holdings_hdr', 'outcome', 'posture', 'judicial_panel'], 
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
        
    return(appeals)



##################################################
# End
##################################################

