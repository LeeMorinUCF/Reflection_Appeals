
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
# MVTnorm_Sims performs simulations of the estimation of parameters
#   in of a trivariate probit model.
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


# install.packages("mvtnorm")
library(mvtnorm)

# mvtnorm example:
# sigma <- matrix(c(4,2,2,3), ncol=2)
# x <- rmvnorm(n=500, mean=c(1,2), sigma=sigma)
# colMeans(x)
# var(x)




##################################################
# Set Parameters for Simulation
##################################################

# Number of appeals court cases.
n_cases <- 100

# Average intents of three appeals court judges.
mu <- c(1, 0, -1)

# Covariance matrix of taste shifters. 
Sigma <- matrix(c(1.0, 0.5, 0.3, 
                  0.5, 1.0, 0.5,
                  0.3, 0.5, 1.0), ncol = 3)

# Test the multivariate normal CDF.
pmvnorm(lower = 0, upper = qnorm(0.975), 
        mean = 0,
        sigma = 1)
# 0.475 
pmvnorm(lower = 0, upper = qnorm(0.995), 
        mean = c(0,0),
        corr = matrix(c(1,0,0,1), ncol = 2))
# 0.245025


##################################################
# Define Functions for Simulation
##################################################

tri_probit_gen <- function(mu, Sigma, n_cases) {
  
  # Generate realizations from a trivariate probit model. 
  # Examples:
  # tri_probit_gen(mu = c(1, 0, -1), Sigma = diag(c(1, 2, 3)), n_cases = 5)
  
  # Latent intents of three appeals court judges.
  nu <- rmvnorm(n = n_cases, mean = mu, sigma = Sigma)
  
  
  # Votes of the appeals panel.
  y <- nu > 0
  
  return(y)
}

# tri_probit_gen(mu = c(1, 0, -1), Sigma = diag(c(1, 2, 3)), n_cases = 5)


##################################################
# Define Functions for Estimation
##################################################

tri_probit_param2vec <- function(mu, Sigma) {
  
  # Translate trivariate probit parameters to a vector.
  # This also works for bigger systems. 
  # Examples: 
  # tri_probit_param2vec(mu = c(0,1,2), Sigma = matrix(c(3,4,5,6,7,8,9,10,11), ncol = 3))
  # tri_probit_vec2param(param = c(0, 1, 2, 4, 5, 8))
  
  
  # Start with vector of means.
  param <- mu
  
  # Append the lower diagonal of Sigma. 
  param <- c(param, Sigma[lower.tri(Sigma, diag = FALSE)])
  
  return(param)
}


tri_probit_vec2param <- function(param) {
  
  # Translate trivariate probit parameters to a vector.
  # This must have the correct number of parameters (6).
  # Examples: 
  # tri_probit_vec2param(param = seq(6))
  # 
  
  if (length(param) != 6) {
    stop("param not correct length.")
  }
  
  # Extract vector of means.
  mu <- param[1:3]
  param <- param[4:6]
  
  # Generate covariance matrix. 
  Sigma = diag(c(1,1,1))
  
  # Append the lower diagonal of Sigma. 
  Sigma[lower.tri(Sigma, diag = FALSE)] <- param
  
  return(list(mu = mu, Sigma = Sigma))
}



tri_probit_loglike <- function(param, y) {
  
  # Likelihood function for a trivariate probit model. 
  # Examples:
  # tri_probit_loglike(param = rep(0, 6), y = matrix(c(T, T, F, T, T, F), nrow = 2))
  
  # Get parameters. 
  n_cases <- nrow(y)
  param_list <- tri_probit_vec2param(param)
  
  # Calculate the probabilities of the observed outcomes.
  loglike <- 0
  # i <- 1
  for (i in 1:n_cases) {
    
    # For each row, determine which side of the threshold to measure the CDF. 
    lower_bd <- rep(-Inf, 3)
    upper_bd <- rep( Inf, 3)
    # For events, the lower bound is zero, upper bound is infinity.
    lower_bd[y[i, ]] <- 0
    # For non-events, the upper bound is zero, lower bound is infinity.
    upper_bd[!y[i, ]] <- 0
    
    print("param = ")
    print(param)
    
    # Calculate the probability. 
    prob <- pmvnorm(lower = lower_bd, upper = upper_bd, 
                    mean = param_list$mu,
                    # corr = param_list$Sigma,
                    sigma = param_list$Sigma)
    
    # Print warning if msg is anything but "Normal Completion". 
    # if (prob$msg != "Normal Completion") {
    #   warning(c(sprintf("Warning message in pmvnorm is: %s", prob$msg), 
    #             "y = ", print(y[i, ])))
    # }
    
    # Accumulate the log in the likelihood function. 
    loglike <- loglike + log(prob[1])
    
  }
  
  
  return(loglike)
}




tri_probit_estn <- function(y, param_0 = FALSE, est_hessian = FALSE) {
  
  # Estimates the mean vector and correlation matrix 
  # for the trivariate probit model. 
  
  # Examples:
  # tri_probit_estn(tri_probit_gen(mu = c(1, 0, -1), Sigma = diag(c(1, 1, 1)), n_cases = 100))
  # tri_probit_estn(tri_probit_gen(mu = c(0, 0, 0), Sigma = diag(c(1, 1, 1)), n_cases = 100))
  
  if (length(param_hat_0) == 6) {
    param_hat_0 <- param_0
  } else {
    param_hat_0 <- rep(0, 6)
  }
  
  tri_probit_optim <- optim(par = param_hat_0, 
                            fn = tri_probit_loglike, 
                            y = y, 
                            method = "BFGS", 
                            hessian = est_hessian)
  
  if (tri_probit_optim$convergence == 1) {
    warning("In optim(), iteration reached maximum limit.")
  } else {
    warning(sprintf("In optim(),convergence code is %d.", 
                    tri_probit_optim$convergence))
  }
  
  param_hat <- tri_probit_optim$par
  param_list <- tri_probit_vec2param(param_hat)
  
  
  
  # If Hessian matrix is returned, append it to the vector of outputs. 
  if (est_hessian) {
    estim_list <- list(param_hat = param_hat, 
                       mu_hat = param_list$mu, 
                       Sigma_hat = param_list$Sigma, 
                       hessian = tri_probit_optim$hessian)
  } else {
    estim_list <- list(param_hat = param_hat, 
                       mu_hat = param_list$mu, 
                       Sigma_hat = param_list$Sigma)
  }
  
  return(param_list)
}




##################################################
# Perform Simulation
##################################################










##################################################
# End
##################################################







