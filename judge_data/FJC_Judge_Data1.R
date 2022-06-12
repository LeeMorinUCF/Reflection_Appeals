

# Federal Court Cases:
# Biographical Directory of Article III Federal Judges


# FJC Data:
# https://www.fjc.gov/research/idb

# Judge data from here:
# https://www.fjc.gov/history/judges/biographical-directory-article-iii-federal-judges-export


# Clear workspace.
rm(list=ls(all=TRUE))


data_in_path <- '~/Research/Appeals_Reflection/FJC_Judge_Data/'




in_file_name <- 'judges.csv'
in_path_file_name <- sprintf('%s%s', data_in_path, in_file_name)

judges <- read.csv(file = in_path_file_name)


colnames(judges)

# “nid” refers to “Node ID.”
# This is a unique identifier for each judge
# generated solely for purposes of the FJC’s biographical database.
# The Node ID also corresponds to each judge’s biography
# on the website and may be used to create a link to a biography
# (for example, the biography of a judge with Node ID 1394646
#   will appear at: http://www.fjc.gov/node/1394646).
summary(judges[, 'nid'])
# All NIDs are populated.

# “jid” refers to “Judge Identification Number.”
# This was used as a unique identifier for each judge,
# generated for purposes of the database, until July 2016.
# These numbers are no longer used and will not be generated
# for judges added to the database after July 2016,
# but will remain in the export as a courtesy
# to researchers who may have relied on them.
summary(judges[, 'jid'])
# All JIDs are populated.


# Variables likely to be used in the analysis.
table(judges[, 'Gender'], useNA = 'ifany')
# All populated.

table(judges[, 'Race.or.Ethnicity'], useNA = 'ifany')
# All populated.


# How complete are the names?
# [3] "Last.Name"
# [4] "First.Name"
# [5] "Middle.Name"
# [6] "Suffix"


length(unique(judges[, 'Last.Name']))
# [1] 2690, most singletons.

name_tab <- table(judges[, 'Last.Name'], useNA = 'ifany')
sum(name_tab != 1)
name_tab[name_tab != 1]
# Many repeated names. None missing.
sum(name_tab)
sum(name_tab[name_tab == 1])
sum(name_tab[name_tab != 1])


length(unique(judges[, 'First.Name']))
name_tab <- table(judges[, 'First.Name'], useNA = 'ifany')
sum(name_tab != 1)
name_tab[name_tab != 1]
names(name_tab)[name_tab == 1]
# Some are initials.
# All populated, some filled in [within square brackets].




table(judges[, 'Suffix'], useNA = 'ifany')
#            II  III   IV  Jr.  Sr.
# 252 3226   21   39    2  295   27
# Numbers, juniors and seniors, most blank.


# Ages of judges.
# [9] "Birth.Year"
# [14] "Death.Year"
summary(as.integer(judges[, 'Birth.Year']))
#    Min. 1st Qu.  Median    Mean 3rd Qu.    Max.    NA's
#    1732    1889    1927    1913    1949    1987       1
summary(as.integer(judges[, 'Death.Year']))
#    Min. 1st Qu.  Median    Mean 3rd Qu.    Max.    NA's
#    1790    1934    1975    1962    2003    2022    1606
# Plausible age range. Many still alive.




# Variables likely to join with court records.
# [127] "Court.Type..[1-6]."
# [128] "Court.Name..[1-6]."
court_num <- 1
var_name <- 'Court.Type'
var_name_num <- sprintf('%s..%d.', var_name, court_num)
length(unique(judges[, var_name_num]))

table(judges[, var_name_num], useNA = 'ifany')
# Court 1:
# Other
# 127
# Supreme Court
# 78
# U.S. Circuit Court (1801-1802)
# 13
# U.S. Circuit Court (1869-1911)
# 37
# U.S. Circuit Court (other)
# 10
# U.S. Court of Appeals
# 462
# U.S. District Court
# 3135
# Similar for court 2, except more blanks.
# No judges with more than 4 appointments
# to US court of Appeals.

# Define subset for judges in the US court of Appeals.
var_name <- 'Court.Type'
app_sub <- FALSE
app_count <- 0
for (court_num in 1:6) {
  var_name_num <- sprintf('%s..%d.', var_name, court_num)
  app_sub <- app_sub | judges[, var_name_num] == 'U.S. Court of Appeals'
  app_count <- app_count + (judges[, var_name_num] == 'U.S. Court of Appeals')
}

# verify.
court_num <- 1
var_name <- 'Court.Type'
var_name_num <- sprintf('%s..%d.', var_name, court_num)
length(unique(judges[, var_name_num]))

table(judges[app_sub, var_name_num], useNA = 'ifany')
table(judges[!app_sub, var_name_num], useNA = 'ifany')
# Check. This represents judges who have ever been appointed to the
# U.S. Courts of Appeals.

sum(app_sub)
table(app_sub, useNA = 'ifany')
# Only 811 judges in the entire history.


# Count distribution over numb er of separate appointments.
table(app_count, useNA = 'ifany')
# app_count
#    0    1    2    3
# 3051  786   23    2


# Names of courts of appeals.
court_num <- 1
var_type <- 'Court.Type'
var_name <- 'Court.Name'
var_type_num <- sprintf('%s..%d.', var_type, court_num)
var_name_num <- sprintf('%s..%d.', var_name, court_num)

app_sel <- judges[, var_type_num] == 'U.S. Court of Appeals'
length(unique(judges[app_sel, var_name_num]))

table(judges[app_sel, var_name_num], useNA = 'ifany')
# Consistent labeling:
# 'U.S. Court of Appeals for the X Circuit'


# Dates of appointments.
# [30] "Nomination.Date..1."
# [31] "Committee.Referral.Date..1."
# [32] "Hearing.Date..1."
# [34] "Committee.Action.Date..1."
# [37] "Confirmation.Date..1."
# [38] "Commission.Date..1."
# [45] "Termination.Date..1."

court_num <- 4
var_type <- 'Court.Type'
# var_name <- 'Court.Name'
# var_name <- 'Nomination.Date'
# var_name <- 'Committee.Referral.Date'
# var_name <- 'Hearing.Date'
# var_name <- 'Committee.Action.Date'
var_name <- 'Confirmation.Date'
# var_name <- 'Commission.Date'
# var_name <- 'Termination.Date'
var_type_num <- sprintf('%s..%d.', var_type, court_num)
var_name_num <- sprintf('%s..%d.', var_name, court_num)

app_sel <- judges[, var_type_num] == 'U.S. Court of Appeals'
sum(app_sel)
length(unique(judges[app_sel, var_name_num]))
# Commission.Dates:
# 1st apptmt:
# [1] 462
# [1] 397
# 2nd apptmt:
# [1] 320
# [1] 261
# 3rd apptmt:
# [1] 50
# [1] 37
# 4th apptmt:
# [1] 6
# [1] 6
# 5th, 6th apptmt:
# [1] 0
# [1] 0
# About 80% have commission dates.
# Similar number have Termination.Date
# (expected lower for present judges).
# For start dates, it appears that commission
# is observed most frequently.



colnames(judges)


############################################################
# Create file for output
# Judges in courts of appeals
############################################################

# Create abbreviated variables describing tenure,
# including multiple appointments.

#------------------------------------------------------------
# Operate on only the appeals court judges.
# Define subset for judges in the US court of Appeals.
#------------------------------------------------------------

var_name <- 'Court.Type'
app_sub <- FALSE
app_count <- 0
for (court_num in 1:6) {
  var_name_num <- sprintf('%s..%d.', var_name, court_num)
  app_sub <- app_sub | judges[, var_name_num] == 'U.S. Court of Appeals'
  app_count <- app_count + (judges[, var_name_num] == 'U.S. Court of Appeals')
}

# verify.
court_num <- 1
var_name <- 'Court.Type'
var_name_num <- sprintf('%s..%d.', var_name, court_num)
length(unique(judges[, var_name_num]))

table(judges[app_sub, var_name_num], useNA = 'ifany')
table(judges[!app_sub, var_name_num], useNA = 'ifany')
# Check. This represents judges who have ever been appointed to the
# U.S. Courts of Appeals.

sum(app_sub)
table(app_sub, useNA = 'ifany')
# Only 811 judges in the entire history.

# Take subset of data for courts of appeals.
app_judges <- judges[app_sub, ]


#------------------------------------------------------------
# Create summary variable for circuit numbers.
#------------------------------------------------------------

var_name <- 'Court.Name'
var_type <- 'Court.Type'

pre_str <- 'U.S. Court of Appeals for the '
post_str <- ' Circuit'

# Abbreviate court names.
abb_df <- data.frame(
  name = c('District of Columbia', 'Federal',
           'First', 'Second', 'Third',
           'Fourth', 'Fifth', 'Sixth',
           'Seventh', 'Eighth', 'Ninth',
           'Tenth', 'Eleventh'),
  abb = c('DC', 'FED', seq(11)))


# court_num <- 1
for (court_num in seq(4)) {

  var_name_num <- sprintf('%s..%d.', var_name, court_num)
  new_var_name_num <- sprintf('app_%d_circ', court_num)
  var_type_num <- sprintf('%s..%d.', var_type, court_num)

  app_sel <- app_judges[, var_type_num] == 'U.S. Court of Appeals'

  # Leave blank for other appointments.
  app_judges[, new_var_name_num] <- ''
  # Copy court name without preamble.
  app_judges[app_sel,
             new_var_name_num] <- gsub(pre_str, '',
                                       app_judges[app_sel, var_name_num])
  # Remove word 'circuit'.
  app_judges[app_sel,
             new_var_name_num] <- gsub(post_str, '',
                                       app_judges[app_sel, new_var_name_num])
  # table(app_judges[, new_var_name_num], useNA = 'ifany')


  # Abbreviate court names.
  for (row in 1:nrow(abb_df)) {
    app_judges[app_sel,
               new_var_name_num] <- gsub(abb_df[row, 'name'],
                                         abb_df[row, 'abb'],
                                         app_judges[app_sel, new_var_name_num])
  }

  print(table(app_judges[, new_var_name_num], useNA = 'ifany'))
}



#------------------------------------------------------------
# Define variable for beginning of tenure.
#------------------------------------------------------------

var_name <- 'Commission.Date'
var_type <- 'Court.Type'

# court_num <- 1
for (court_num in seq(4)) {

  var_name_num <- sprintf('%s..%d.', var_name, court_num)
  new_var_name_num <- sprintf('app_%d_beg_yr', court_num)
  var_type_num <- sprintf('%s..%d.', var_type, court_num)

  app_sel <- app_judges[, var_type_num] == 'U.S. Court of Appeals'

  # Leave blank for other appointments.
  app_judges[, new_var_name_num] <- ''

  # Record year for appointments to courts of appeal.
  app_judges[app_sel, new_var_name_num] <-
    substr(app_judges[app_sel, var_name_num], 1, 4)


  print(table(app_judges[, new_var_name_num], useNA = 'ifany'))
}


#------------------------------------------------------------
# Define variable for end of tenure, if available.
#------------------------------------------------------------

var_name <- 'Termination.Date'
var_type <- 'Court.Type'

# court_num <- 4
for (court_num in seq(4)) {

  var_name_num <- sprintf('%s..%d.', var_name, court_num)
  new_var_name_num <- sprintf('app_%d_end_yr', court_num)
  var_type_num <- sprintf('%s..%d.', var_type, court_num)

  app_sel <- app_judges[, var_type_num] == 'U.S. Court of Appeals'

  # Leave blank for other appointments.
  app_judges[, new_var_name_num] <- ''

  # Record year for appointments to courts of appeal.
  app_judges[app_sel, new_var_name_num] <-
    substr(app_judges[app_sel, var_name_num], 1, 4)


  print(table(app_judges[, new_var_name_num], useNA = 'ifany'))
}



#------------------------------------------------------------
# Output a summary dataset for matching judges
# from court records.
#------------------------------------------------------------

outcol_sel <- c('nid',
                'Last.Name', 'First.Name', 'Middle.Name', 'Suffix',
                'Birth.Year', 'Death.Year',
                'app_1_circ', 'app_1_beg_yr', 'app_1_end_yr',
                'app_2_circ', 'app_2_beg_yr', 'app_2_end_yr',
                'app_3_circ', 'app_3_beg_yr', 'app_3_end_yr',
                'app_4_circ', 'app_4_beg_yr', 'app_4_end_yr')


out_file_name <- 'FJC_app_judge_list.csv'
data_out_path <- data_in_path
out_path_file_name <- sprintf('%s%s', data_out_path, out_file_name)


write.csv(file = out_path_file_name,
          x = app_judges[, outcol_sel],
          row.names = FALSE,
          na = '')

