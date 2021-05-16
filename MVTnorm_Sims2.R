
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
# This second version estimates a model without covariates
#   and specifies the covariance matrix as the identity matrix. 
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

# mvtnorm examples:

# sigma <- matrix(c(4,2,2,3), ncol=2)
# x <- rmvnorm(n=500, mean=c(1,2), sigma=sigma)
# colMeans(x)
# var(x)

# # Test the multivariate normal CDF.
# pmvnorm(lower = 0, upper = qnorm(0.975), 
#         mean = 0,
#         sigma = 1)
# # 0.475 
# pmvnorm(lower = 0, upper = qnorm(0.995), 
#         mean = c(0,0),
#         corr = matrix(c(1,0,0,1), ncol = 2))
# # 0.245025




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

tri_probit_param2vec <- function(mu, Sigma, model_name) {
  
  # Translate trivariate probit parameters to a vector.
  # This also works for bigger systems. 
  # Note: It ignores other parameters outside the specified model. 
  # Examples: 
  # tri_probit_param2vec(c(0,1,2), NULL, 'mu_only')
  # tri_probit_param2vec(c(0,1,2), matrix(seq(3,11), ncol = 3), 'mu_const')
  # tri_probit_param2vec(c(0,1,2), matrix(seq(3,11), ncol = 3), 'mu_cov')
  
  
  # Start with vector of means.
  param <- mu
  
  # Append the parameters from the covariance matrix, if any.
  if (model_name == 'mu_only') {
    # No additional parameters, Sigma is the identity matrix. 
  } else if (model_name == 'mu_const') {
    # The lower triangle of Sigma is a constant.
    param <- c(param, Sigma[2, 1])
  } else if (model_name == 'mu_cov') {
    # The entire covariance matrix is specified.
    # Append the lower triangle of Sigma. 
    param <- c(param, Sigma[lower.tri(Sigma, diag = FALSE)])
  }
  
  
  
  return(param)
}


tri_probit_num_params <- function(model_name) {
  
  # Determine the number of parameters for each model.  
  
  if (model_name == 'mu_only') {
    
    # No additional parameters for Sigma, Sigma is the identity matrix. 
    num_params <- 3
    
  } else if (model_name == 'mu_const') {
    
    # The lower triangle of Sigma is a constant.
    num_params <- 4
    
  } else if (model_name == 'mu_cov') {
    
    # The entire covariance matrix is specified.
    # Three parameters in the lower triangle. 
    num_params <- 6
    
  }
  
}


tri_probit_vec2param <- function(param, model_name) {
  
  # Translate trivariate probit parameters to a vector.
  # This must have the correct number of parameters.
  # Examples: 
  # tri_probit_vec2param(param = seq(3), 'mu_only')
  # tri_probit_vec2param(param = seq(4), 'mu_const')
  # tri_probit_vec2param(param = seq(6), 'mu_cov')
  # 
  
  
  # Extract vector of mean intercept.
  mu <- param[1:3]
  if (model_name == 'mu_only') {
    if (length(param) != 3) {
      stop("param not correct length.")
    }
    param <- NULL
  } else {
    param <- param[4:length(param)]
  }
  
  
  # Initialize covariance matrix. 
  Sigma = diag(c(1,1,1))
  
  if (model_name == 'mu_only') {
    # No additional parameters, Sigma is the identity matrix. 
  } else if (model_name == 'mu_const') {
    # The lower triangle of Sigma is a constant.
    if (length(param) != 1) {
      stop("param not correct length.")
    }
    Sigma[lower.tri(Sigma, diag = FALSE)] <- param
  } else if (model_name == 'mu_cov') {
    # The entire covariance matrix is specified.
    if (length(param) != 3) {
      stop("param not correct length.")
    }
    # Append the lower triangle of Sigma. 
    Sigma[lower.tri(Sigma, diag = FALSE)] <- param
  }
  
  # Append the upper triangle of Sigma, imposing symmetry. 
  Sigma[upper.tri(Sigma, diag = FALSE)] <- 
    Sigma[lower.tri(Sigma, diag = FALSE)]
  
  return(list(mu = mu, Sigma = Sigma))
}


# Numerical issue for likelihood function:
# Covariance matrix must be positive definite.
# param_list <- tri_probit_vec2param(param = c(0,0,0, 0.001,0,0))
# chol(param_list$Sigma)
# For now, prime the optimization with a warm start. 


tri_probit_loglike <- function(param, y, model_name) {
  
  # Likelihood function for a trivariate probit model. 
  # Examples:
  # tri_probit_loglike(param = rep(0, 6), y = matrix(c(T, T, F, T, T, F), nrow = 2))
  
  
  # print("param = ")
  # print(param)
  
  # Get parameters. 
  n_cases <- nrow(y)
  param_list <- tri_probit_vec2param(param, model_name)
  
  # Verify that the covariance matrix is positive definite. 
  # Not necessary (yet).
  
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




tri_probit_estn <- function(y, model_name, param_0 = NULL, est_hessian = FALSE) {
  
  # Estimates the mean vector and correlation matrix 
  # for the trivariate probit model. 
  
  # Examples:
  # tri_probit_estn(tri_probit_gen(mu = c(1, 0, -1), Sigma = diag(c(1, 1, 1)), n_cases = 100))
  # tri_probit_estn(tri_probit_gen(mu = c(0, 0, 0), Sigma = diag(c(1, 1, 1)), n_cases = 100))
  
  # Need logic for model_name. 
  # Could write function for number of parameters. 
  num_params <- tri_probit_num_params(model_name)
  if (!is.null(param_0)) {
    if (length(param_0) == num_params) {
      param_hat_0 <- param_0
    } else {
      stop("param not correct length.")
    }
  } else {
    param_hat_0 <- rep(0, num_params)
  }
  # param_hat_0 <- param_0
  # print(param_hat_0)
  
  tri_probit_optim <- optim(par = param_hat_0, 
                            fn = tri_probit_loglike, 
                            y = y, 
                            model_name = model_name, 
                            method = "BFGS", 
                            hessian = est_hessian, 
                            control = list(fnscale= -1))
  
  if (tri_probit_optim$convergence == 1) {
    warning("In optim(), iteration reached maximum limit.")
  } else {
    warning(sprintf("In optim(),convergence code is %d.", 
                    tri_probit_optim$convergence))
  }
  
  param_hat <- tri_probit_optim$par
  param_list <- tri_probit_vec2param(param_hat, model_name)
  
  
  
  # If Hessian matrix is returned, append it to the vector of outputs. 
  estn_list <- list(param_hat = param_hat, 
                    mu_hat = param_list$mu, 
                    Sigma_hat = param_list$Sigma)
  if (est_hessian) {
    estn_list$hessian <- tri_probit_optim$hessian
  }
  
  return(estn_list)
}




##################################################
# Set Parameters for Simulation
##################################################

# Number of replications for simulation of estimation. 
num_reps <- 100

# Number of appeals court cases.
n_cases <- 100

# Average intents of three appeals court judges.
mu_0 <- c(1, 0, -1)


# Design of sigma depends on the chosen model. 
# model_name <- 'mu_only'
# param_0 <- mu_0

model_name <- 'mu_const'
param_0 <- c(mu_0, 0.5)
# 
# model_name <- 'mu_cov'
# param_0 <- c(mu_0, 0.8, 0.2, 0.5)


param_list <- tri_probit_vec2param(param_0, model_name)

mu_0 <- param_list$mu
Sigma_0 <- param_list$Sigma



# Previous approach specified the parameters directly. 

# # Covariance matrix of taste shifters. 
# Sigma_0 <- matrix(c(1.0, 0.8, 0.2, 
#                     0.8, 1.0, 0.5,
#                     0.2, 0.5, 1.0), ncol = 3)
# 
# # Collect into a vector of parameters.
# param_0 <- tri_probit_param2vec(mu = mu_0, Sigma = Sigma_0, model_name)


if (model_name == 'mu_only') {
  estn_results <- data.frame(matrix(nrow = num_reps, ncol = 3))
  colnames(estn_results) <- c(sprintf("mu_%d", seq(3)))
} else if (model_name == 'mu_const') {
  estn_results <- data.frame(matrix(nrow = num_reps, ncol = 4))
  colnames(estn_results) <- c(sprintf("mu_%d", seq(3)), 
                              "Sigma_21")
} else if (model_name == 'mu_cov') {
  estn_results <- data.frame(matrix(nrow = num_reps, ncol = 6))
  colnames(estn_results) <- c(sprintf("mu_%d", seq(3)), 
                              "Sigma_21", "Sigma_31", "Sigma_32")
}



##################################################
# Perform Simulation
##################################################


# rep_num <- 1
for (rep_num in 1:num_reps) {
  
  print(sprintf("Now completing iteration %d of %d. ", rep_num, num_reps))
  
  # Generate realization of trivariate probit. 
  y_sim <- tri_probit_gen(mu = mu_0, Sigma = Sigma_0, n_cases = n_cases)
  
  # Estimate model.
  estn_list <- tri_probit_estn(y = y_sim, model_name = model_name, param_0 = param_0)
  
  # Store estimation results. 
  estn_results[rep_num, ] <- estn_list$param_hat
  
}

summary(estn_results)



# I ran a simulation with these parameter inputs:


# # Number of replications for simulation of estimation. 
# num_reps <- 100
# 
# # Number of appeals court cases.
# n_cases <- 100
# 
# # Average intents of three appeals court judges.
# mu_0 <- c(1, 0, -1)
# 
# 
# # Design of sigma depends on the chosen model. 
# model_name <- 'mu_only'
# param_0 <- mu_0
# 
# > Sigma_0
# [,1] [,2] [,3]
# [1,]    1    0    0
# [2,]    0    1    0
# [3,]    0    0    1


# These were the results:

# mu_1             mu_2                 mu_3        
# Min.   :0.6433   Min.   :-2.275e-01   Min.   :-1.4758  
# 1st Qu.:0.9154   1st Qu.:-7.527e-02   1st Qu.:-1.1264  
# Median :0.9945   Median :-2.900e-07   Median :-0.9945  
# Mean   :1.0242   Mean   :-1.436e-03   Mean   :-1.0142  
# 3rd Qu.:1.1264   3rd Qu.: 7.527e-02   3rd Qu.:-0.9154  
# Max.   :1.4758   Max.   : 3.055e-01   Max.   :-0.5244  


# It works much better with an identity restriction on the 
# covariance matrix but 100 observations does not buy us much accuracy. 

# At least estimating the mean equation is numerically stable
# with only 100 observations. 




# Next, I ran another simulation with these parameter inputs:

# # Number of replications for simulation of estimation. 
# num_reps <- 100
# 
# # Number of appeals court cases.
# n_cases <- 100
# 
# # Average intents of three appeals court judges.
# mu_0 <- c(1, 0, -1)
# 
# 
# 
# model_name <- 'mu_const'
# param_0 <- c(mu_0, 0.5)

# > Sigma_0
# [,1] [,2] [,3]
# [1,]  1.0  0.5  0.5
# [2,]  0.5  1.0  0.5
# [3,]  0.5  0.5  1.0



# These were the results:




##################################################
# End
##################################################

