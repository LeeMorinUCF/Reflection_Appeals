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
# May 14, 2021
#
##################################################
#
# Estn_Sims performs simulations of the estimation of parameters
#   in a model of Judicial Panel Voting in U.S. Courts of Appeals.
#   It is part of the code base to accompany
#   the manuscript "Diversity Effects or Dissent Aversion?
#   Identification and Estimation in Judicial Panel Voting"
#   by Cameron, Morin and Paarsch
#   
#
# Dependencies:
#   None.
#
#
##################################################


# Clear workspace, if running interactively.
rm(list=ls(all=TRUE))

# Set working directory, if other than Credit_COVID19_Canada.
user_path <- 'C:/Users/le279259/OneDrive - University of Central Florida/Documents'
git_path <- 'Research/Appeals_Reflection/Reflection_Appeals'
wd_path <- sprintf("%s/%s", user_path, git_path)
setwd(wd_path)





##################################################
# Load Packages
##################################################

# library(name_of_package)






##################################################
# Set Parameters for Simulation
##################################################

# Number of appeals court cases.
n_cases <- 100

# Average intents of three appeals court judges.
mu <- c(0, 0, 0)
# mu_1 <- 0
# mu_2 <- 0
# mu_3 <- 0

install.packages("mvtnorm")
library(mvtnorm)



##################################################
# Define Functions for Simulation
##################################################

decision_gen <- function(mu, n_cases) {
  
  # Latent intents of three appeals court judges.
  nu <- mu + matrix(rnorm(3*n_cases), ncol = 3)
  # nu_1 <- mu_1 + rnorm(n_cases)
  # nu_2 <- mu_2 + rnorm(n_cases)
  # nu_3 <- mu_3 + rnorm(n_cases)

  
  # Votes of the appeals panel.
  y > 0
  # y_1 <- nu_1 > 0
  # y_2 <- nu_2 > 0
  # y_3 <- nu_3 > 0
  
  
  
}



##################################################
# Define Functions for Estimation
##################################################




##################################################
# Perform Simulation
##################################################





##################################################
# End
##################################################





