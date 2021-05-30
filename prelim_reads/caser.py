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
    
    # The next name(s) should be the Defendant-Appellee.
    def_appee = []
    line = file.readline()
    
    # When the next line is a case number, the list of Defendant-Appellees is complete.
    found_case_num = is_case_num(line)
    lines_read = 0
    while not found_case_num and lines_read < 5:
        def_appee.append(line.replace("\n",""))
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
    return("No." in line_list or "Docket" in line_list)


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
    # Deprecated: Appended to end of holdings.
    
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
        # (pla_appnt, def_appee) = get_party_names(file)
        (pla_appnt, def_appee, last_line) = get_party_names(file)
        
        # Record the case number.
        # case_num = get_case_num(file)
        case_num = get_case_num(file, last_line)
        
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
# End
##################################################

