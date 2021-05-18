

# Set parameters for example. 

n_draws <- 100000

delta_0 <- 0.25
# delta_0 <- 0.1


dis_av_pars <- dis_aversn_params(mu_in = c(1, 2, 3), delta = delta_0)




dis_av_pars$mu

dis_av_pars$D_inv

dis_av_pars$Sigma

#--------------------------------------------------
# Compare methods for drawing MVN rvs. 
#--------------------------------------------------


mu_mat <- matrix(rep(dis_av_pars$mu, n_draws), nrow = n_draws, byrow = TRUE)

# Write function to generate MVN rvs.
chol_S <- chol(dis_av_pars$Sigma)

u <- matrix(rnorm(n = n_draws*3), ncol = 3)


nu_std <- u %*% chol_S + mu_mat



# Use ready-made function.



nu_mv <- rmvnorm(n = n_draws, mean = dis_av_pars$mu, sigma = dis_av_pars$Sigma)




# Compare the estimated means and covariances. 

dis_av_pars$mu
summary(nu_std)
summary(nu_mv)



dis_av_pars$Sigma
cov(nu_std)
cov(nu_mv)




#--------------------------------------------------
# Compare alternative calculations of the probabilities wrt scaling. 
#--------------------------------------------------


# Standard approach as is.



# Standardizing for unit diagonal on Sigma. 







