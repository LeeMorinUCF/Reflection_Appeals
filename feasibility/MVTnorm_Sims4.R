
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
# May 17, 2021
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
# This fourth version estimates a model with covariates and peer effects. 
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


alloc_judges <- function(x_judge) {
  
  # Create a list of judiciary panels for a series of cases
  # using a list of judges' characteristics. 
  # x_judge is a matrix of covariates for each judge, 
  # with a row for each judge and a column for each covariate.
  # Each combination of judges appears n_cycles times. 
  # Examples:
  # alloc_judges(x_judge = matrix(sample(c(0,1), 4*2, replace = TRUE), ncol = 2))
  
  # This version cycles through every permutation of judiciary panels. 
  
  num_judges <- nrow(x_judge)
  
  # Assemble a list of judges. 
  panels <- expand.grid(j1 = seq(num_judges), 
                        j2 = seq(num_judges), 
                        j3 = seq(num_judges))
  # Exclude any rows with duplicate judges. 
  panels <- panels[panels[, 'j1'] != panels[, 'j2'] &
                     panels[, 'j1'] != panels[, 'j3'] &
                     panels[, 'j2'] != panels[, 'j3'] , ]
  
  
  
  return(panels)
}


TVP_vote_gen <- function(alpha, beta, gamma, Sigma, 
                        x_judge, n_cycles, peer_fx = FALSE) {
  
  # Generate realizations from a trivariate probit model, 
  # using the attitudinal approach to modeling judicial decisions:
  # each judge has a set of covariates in the matrix x_judge, 
  # which has a row for each judge and a column for each covariate.
  # Each combination of judges appears n_cycles times. 
  # Be careful: it works with a vector of judge-specific intercepts, 
  # as well as a single intercept coefficient.
  # Examples:
  # TVP_att_gen(alpha = c(1, 0, -1), beta = c(1,1), Sigma = diag(c(1, 1, 1)), x_judge = matrix(sample(c(0,1), 4*2, replace = TRUE), ncol = 2), n_cycles = 3)
  # TVP_att_gen(alpha = 0.5, beta = c(1,1), Sigma = diag(c(1, 1, 1)), x_judge = matrix(sample(c(0,1), 4*2, replace = TRUE), ncol = 2), n_cycles = 3)
  
  # Verify compatible dimensions.
  num_covars <- ncol(x_judge)
  if (num_covars != length(beta)) {
    stop("Number of covariates do not match number of slope coefficients.")
  }
  
  # Populate the dataset in blocks by cycling through the combinations of judges. 
  panels <- alloc_judges(x_judge)
  num_panels <- nrow(panels)
  
  # Determine the number of cases by replicating each panel n_cycles times.
  n_cases <- n_cycles*num_panels
  y <- matrix(nrow = n_cases, ncol = 3)
  x <- matrix(nrow = n_cases, ncol = 3*num_covars)
  
  # For each combination of judges, calculate mean vector and latent intents. 
  for (j in 1:num_panels) {
    
    # Draw a panel of judges. 
    judge_index <- panels[j, ]
    
    # Draw the corresponding covariates. 
    x_judge_1 <- x_judge[unlist(judge_index[1]), ]
    x_judge_2 <- x_judge[unlist(judge_index[2]), ]
    x_judge_3 <- x_judge[unlist(judge_index[3]), ]
    
    
    # Calculate the mean intents for the panel.
    mu <- alpha + c(sum(x_judge_1 * beta), 
                    sum(x_judge_2 * beta), 
                    sum(x_judge_3 * beta))
    
    # Add peer effects, if required.
    if (peer_fx == TRUE) {
      mu <- mu + c(sum(x_judge_2 * gamma + x_judge_3 * gamma), 
                   sum(x_judge_1 * gamma + x_judge_3 * gamma), 
                   sum(x_judge_1 * gamma + x_judge_2 * gamma))
    }
    
    # Calculate the latent intents of three appeals court judges.
    nu <- rmvnorm(n = n_cycles, mean = mu, sigma = Sigma)
    
    # Determine the votes of the appeals panel.
    y_j <- nu > 0
    
    # Insert the votes into the dataset. 
    y[seq((j-1)*n_cycles + 1, j*n_cycles), ] <- y_j
    
    # Also record the sequence of covariates. 
    x[seq((j-1)*n_cycles + 1, j*n_cycles), ] <- 
      matrix(rep(c(x_judge_1, x_judge_2, x_judge_3), n_cycles), 
             nrow = n_cycles, byrow = TRUE)
    
  }
  
  # Collect the matrices of outcomes and covariates.
  TVP_votes <- list(y = y, x = x)
  
  return(TVP_votes)
}





##################################################
# Define Functions for Estimation
##################################################

tri_probit_param2vec <- function(mu = NULL, alpha = NULL, beta = NULL, gamma = NULL, 
                                 Sigma, model_name) {
  
  # Translate trivariate probit parameters to a vector.
  # This also works for bigger systems. 
  # Note: It ignores other parameters outside the specified model. 
  # Examples: 
  # tri_probit_param2vec(mu = c(0,1,2), Sigma = NULL, model_name = 'mu_only')
  # tri_probit_param2vec(mu = c(0,1,2), Sigma = matrix(seq(3,11), ncol = 3), model_name = 'mu_const')
  # tri_probit_param2vec(mu = c(0,1,2), Sigma = matrix(seq(3,11), ncol = 3), model_name = 'mu_cov')
  # tri_probit_param2vec(alpha = 1, beta = c(2,3), Sigma = matrix(seq(4,12), ncol = 3), model_name = 'cov_const')
  # tri_probit_param2vec(alpha = 1, beta = c(2,3), gamma = c(4,5), Sigma = matrix(seq(6,14), ncol = 3), model_name = 'peer_fx')
  
  # Start with mean equation.
  if (model_name == 'cov_const') {
    param <- c(alpha, beta)
  } else if (model_name == 'peer_fx') {
    param <- c(alpha, beta, gamma)
  } else {
    # Vector of means with intercept only.
    param <- mu
  }
  
  # Append the parameters from the covariance matrix, if any.
  if (model_name %in% c('mu_only', 'peer_fx')) {
    # No additional parameters, Sigma is the identity matrix. 
  } else if (model_name %in% c('mu_const', 'cov_const')) {
    # The lower triangle of Sigma is a constant.
    param <- c(param, Sigma[2, 1])
  } else if (model_name == 'mu_cov') {
    # The entire covariance matrix is specified.
    # Append the lower triangle of Sigma. 
    param <- c(param, Sigma[lower.tri(Sigma, diag = FALSE)])
  }
  
  
  
  return(param)
}


tri_probit_num_params <- function(model_name, num_covars = 0) {
  
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
    
  } else if (model_name == 'cov_const') {
    # The lower triangle of Sigma is a constant, 
    # plus a mean and slope coefficients.
    # Three separate judge-specific intercepts:
    # num_params <- 4 + num_covars
    # One panel-wide intercept:
    num_params <- 2 + num_covars
    
  } else if (model_name == 'peer_fx') {
    # The Sigma is an identity matrix. 
    # One panel-wide intercept, 
    # plus a mean and slope coefficients for both
    # self-effects and peer effects.
    num_params <- 1 + 2*num_covars
  }
  
  return(num_params)
}


tri_probit_vec2param <- function(param, model_name, num_covars = 0) {
  
  # Translate trivariate probit parameters to a vector.
  # This must have the correct number of parameters.
  # Examples: 
  # tri_probit_vec2param(param = seq(3), model_name = 'mu_only')
  # tri_probit_vec2param(param = seq(4), model_name = 'mu_const')
  # tri_probit_vec2param(param = seq(6), model_name = 'mu_cov')
  # tri_probit_vec2param(param = seq(3), model_name = 'cov_const', num_covars = 1)
  # tri_probit_vec2param(param = seq(4), model_name = 'cov_const', num_covars = 2)
  # tri_probit_vec2param(param = seq(5), model_name = 'cov_const', num_covars = 3)
  # tri_probit_vec2param(param = seq(3), model_name = 'peer_fx', num_covars = 1)
  # tri_probit_vec2param(param = seq(5), model_name = 'peer_fx', num_covars = 2)
  # tri_probit_vec2param(param = seq(7), model_name = 'peer_fx', num_covars = 3)
  
  if (length(param) != tri_probit_num_params(model_name, num_covars)) {
    stop("param not correct length.")
  }
  
  if (model_name %in% c('cov_const', 'peer_fx')) {
    if (num_covars == 0) {
      stop("No covariates specified.")
    }
  }
  
  # Parameters for mean equation. 
  if (model_name == 'cov_const') {
    # Intercepts and slope coefficients. 
    mu <- NULL
    alpha <- param[1]
    beta <- param[seq(2, (1 + num_covars))]
    gamma <- NULL
  } else if (model_name == 'peer_fx') {
    # Intercepts and slope coefficients, 
    # for both self-effects and peer effects. 
    mu <- NULL
    alpha <- param[1]
    beta <- param[seq(2, 1 + num_covars)]
    gamma <- param[seq(1 + num_covars + 1, 1 + 2*num_covars)]
  } else {
    # Extract vector of mean intercept.
    mu <- param[1:3]
    alpha <- NULL
    beta <- NULL
    gamma <- NULL
  }
  
  
  if (model_name == 'mu_only') {
    # No more parameters. 
    param <- NULL
  } else {
    # Remaining parameters define Sigma. 
    param <- param[seq((1 + num_covars + 1), length(param))]
  }
  
  
  # Initialize covariance matrix. 
  Sigma = diag(c(1,1,1))
  
  if (model_name %in% c('mu_only', 'peer_fx')) {
    # No additional parameters, Sigma is the identity matrix. 
  } else if (model_name %in% c('mu_const', 'cov_const')) {
    # The lower triangle of Sigma is a constant.
    Sigma[lower.tri(Sigma, diag = FALSE)] <- param
  } else if (model_name == 'mu_cov') {
    # The entire covariance matrix is specified.
    # Append the lower triangle of Sigma. 
    Sigma[lower.tri(Sigma, diag = FALSE)] <- param
  }
  
  # Append the upper triangle of Sigma, imposing symmetry. 
  Sigma[upper.tri(Sigma, diag = FALSE)] <- 
    Sigma[lower.tri(Sigma, diag = FALSE)]
  
  
  return(list(mu = mu, alpha = alpha, beta = beta, gamma = gamma, Sigma = Sigma))
}


# Numerical issue for likelihood function:
# Covariance matrix must be positive definite.
# param_list <- tri_probit_vec2param(param = c(0,0,0, 0.001,0,0))
# chol(param_list$Sigma)
# For now, prime the optimization with a warm start. 


tri_probit_loglike <- function(param, y, x = NULL, model_name) {
  
  # Likelihood function for a trivariate probit model. 
  # Examples:
  # tri_probit_loglike(param = rep(0, 6), y = matrix(c(T, T, F, T, T, F), nrow = 2))
  
  
  # print("param = ")
  # print(param)
  
  # Get parameters. 
  n_cases <- nrow(y)
  num_covars <- ncol(x)/3
  param_list <- tri_probit_vec2param(param, model_name, num_covars)
  
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
    
    
    # Calculate the mean vector of latent intents. 
    if (model_name %in% c('mu_only', 'mu_const', 'mu_cov')) {
      
      mean_tvprobit <- param_list$mu
      
    } else if (model_name %in% c('cov_const', 'peer_fx')) {
      
      # Calculate the mean intents for the panel.
      x_judge_1 <- x[i, seq(num_covars)]
      x_judge_2 <- x[i, seq(num_covars + 1, 2*num_covars)]
      x_judge_3 <- x[i, seq(2*num_covars + 1, 3*num_covars)]
      
      mean_tvprobit <- param_list$alpha + c(sum(x_judge_1 * param_list$beta), 
                                            sum(x_judge_2 * param_list$beta), 
                                            sum(x_judge_3 * param_list$beta))
    }
    
    # Add peer effects, if required.
    if (model_name == 'peer_fx') {
      mean_tvprobit <- mean_tvprobit + c(sum(x_judge_2 * param_list$gamma + 
                                               x_judge_3 * param_list$gamma), 
                                         sum(x_judge_1 * param_list$gamma + 
                                               x_judge_3 * param_list$gamma), 
                                         sum(x_judge_1 * param_list$gamma + 
                                               x_judge_2 * param_list$gamma))
    }
    
    
    # Calculate the probability. 
    prob <- pmvnorm(lower = lower_bd, upper = upper_bd, 
                    mean = mean_tvprobit,
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




tri_probit_estn <- function(y, x = NULL, 
                            model_name, param_0 = NULL, est_hessian = FALSE) {
  
  # Estimates the mean vector and correlation matrix 
  # for the trivariate probit model. 
  
  # Examples:
  # tri_probit_estn(tri_probit_gen(mu = c(1, 0, -1), Sigma = diag(c(1, 1, 1)), n_cases = 100))
  # tri_probit_estn(tri_probit_gen(mu = c(0, 0, 0), Sigma = diag(c(1, 1, 1)), n_cases = 100))
  
  # Check for correctly specified inputs. 
  if (model_name %in% c('cov_const', 'peer_fx')) {
    num_covars <- ncol(x)/3
  } else {
    num_covars <- 0
  }
  num_params <- tri_probit_num_params(model_name, num_covars)
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
  
  # Estimation depends on whether there are covariates. 
  if (model_name %in% c('cov_const', 'peer_fx')) {
    tri_probit_optim <- optim(par = param_hat_0, 
                              fn = tri_probit_loglike, 
                              y = y, 
                              x = x, 
                              model_name = model_name, 
                              method = "BFGS", 
                              hessian = est_hessian, 
                              control = list(fnscale= -1))
  } else {
    tri_probit_optim <- optim(par = param_hat_0, 
                              fn = tri_probit_loglike, 
                              y = y, 
                              model_name = model_name, 
                              method = "BFGS", 
                              hessian = est_hessian, 
                              control = list(fnscale= -1))
  }
  
  
  if (tri_probit_optim$convergence == 1) {
    warning("In optim(), iteration reached maximum limit.")
  } else {
    warning(sprintf("In optim(),convergence code is %d.", 
                    tri_probit_optim$convergence))
  }
  
  param_hat <- tri_probit_optim$par
  param_list <- tri_probit_vec2param(param_hat, model_name, num_covars)
  
  
  
  # If Hessian matrix is returned, append it to the vector of outputs. 
  estn_list <- list(param_hat = param_hat, 
                    mu_hat = NULL, 
                    alpha_hat = NULL, 
                    beta_hat = NULL, 
                    gamma_hat = NULL, 
                    Sigma_hat = param_list$Sigma, 
                    hessian = NULL)
  if (model_name == 'cov_const') {
    estn_list$alpha_hat <- param_list$alpha
    estn_list$beta_hat <- param_list$beta
  } else if (model_name == 'peer_fx') {
    estn_list$alpha_hat <- param_list$alpha
    estn_list$beta_hat <- param_list$beta
    estn_list$gamma_hat = param_list$gamma
  } else {
    estn_list$mu_hat = param_list$mu
  }
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



# Number of times each combination of judges appears on the panel. 
n_cycles <- 3

# Specify a dataset for the characteristics of judges.
num_judges <- 5
x_judge <- matrix(sample(c(0,1), num_judges*2, replace = TRUE), ncol = 2)

# Populate the dataset in blocks by cycling through the combinations of judges. 
panels <- alloc_judges(x_judge)
num_panels <- nrow(panels)
# 5 choose 3 is 60 distinct judiciary panels. 

# Determine the number of cases by replicating each panel n_cycles times.
n_cases <- n_cycles*num_panels
# 180 cases, in total.




# Average intents of three appeals court judges.
# mu_0 <- c(1, 0, -1)
alpha_0 <- 0.25

# Slope coefficients on covariates for own characteristics, common to all judges.
beta_0 <- c(1, 2)

# Slope coefficients on covariates for peer effects, common to all judges.
gamma_0 <- c(-0.5, -1)

# Correlation coefficient for the taste-shifters of pairs of judges.
# Off-diagonal element of Sigma
# sigma_21 <- 0.5
# Sigma is identity matrix. 

# Design of sigma depends on the chosen model. 
# model_name <- 'mu_only'
# param_0 <- mu_0

# model_name <- 'mu_const'
# param_0 <- c(mu_0, sigma_21)
# 
# model_name <- 'mu_cov'
# param_0 <- c(mu_0, 0.8, 0.2, 0.5)


# model_name <- 'cov_const'
# param_0 <- c(alpha_0, beta_0, sigma_21)


# Sigma is the identity matrix, to identify the model. 
model_name <- 'peer_fx'
param_0 <- c(alpha_0, beta_0, gamma_0)


param_list <- tri_probit_vec2param(param_0, model_name, 
                                   num_covars = length(beta_0))

mu_0 <- param_list$mu
alpha_0 <- param_list$alpha
beta_0 <- param_list$beta
gamma_0 <- param_list$gamma
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
} else if (model_name == 'cov_const') {
  estn_results <- data.frame(matrix(nrow = num_reps, ncol = 2 + length(beta_0)))
  colnames(estn_results) <- c("alpha", 
                              sprintf("beta_%d", seq(length(beta_0))), 
                              "Sigma_21")
} else if (model_name == 'peer_fx') {
  estn_results <- data.frame(matrix(nrow = num_reps, ncol = 1 + 2*length(beta_0)))
  colnames(estn_results) <- c("alpha", 
                              sprintf("beta_%d", seq(length(beta_0))), 
                              sprintf("gamma_%d", seq(length(beta_0))))
}



##################################################
# Perform Simulation
##################################################


# rep_num <- 1
for (rep_num in 1:num_reps) {
  
  print(sprintf("Now completing iteration %d of %d. ", rep_num, num_reps))
  
  # Generate realization of trivariate probit. 
  # y_sim <- tri_probit_gen(mu = mu_0, Sigma = Sigma_0, n_cases = n_cases)
  # TVP_att_sim <- TVP_att_gen(alpha = alpha_0, beta = beta_0, Sigma = Sigma_0, 
  #                            x_judge, n_cycles)
  TVP_vote_sim <- TVP_vote_gen(alpha = alpha_0, beta = beta_0, gamma = gamma_0, Sigma = Sigma_0, 
                               x_judge, n_cycles, peer_fx = TRUE)
  
  # Estimate model.
  estn_list <- tri_probit_estn(y = TVP_vote_sim$y, x = TVP_vote_sim$x, 
                               model_name = model_name, param_0 = param_0)
  
  # Store estimation results. 
  estn_results[rep_num, ] <- estn_list$param_hat
  
  
  
  # Print a progress report. 
  if (floor(rep_num/num_reps*10) == rep_num/num_reps*10) {
    print(summary(estn_results))
  }
  
  
}

summary(estn_results)

