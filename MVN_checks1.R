

# Set parameters for example. 

n_draws <- 100

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


# Example that illustrates scaling:

# Example in documentation.
a <- pmvnorm(lower=-Inf, upper=c(2,2), sigma = diag(2)*2)
b <- pmvnorm(lower=-Inf, upper=c(2,2)/sqrt(2), corr=diag(2))
# stopifnot(all.equal(round(a,5) , round(b, 5)))

print(sprintf("a = %f, b = %f", a, b))

# Example with correlation. 
a <- pmvnorm(lower=-Inf, upper=c(2,2), sigma = matrix(c(2,1,1,2), nrow=2))
b <- pmvnorm(lower=-Inf, upper=c(2,2)/sqrt(2), corr = matrix(c(1,0.5,0.5,1), nrow=2))
print(sprintf("a = %f, b = %f", a, b))


# Example with correlation and non-zero means. 
a <- pmvnorm(lower=-Inf, upper=c(2,2), mean = c(1,3), sigma = matrix(c(2,1,1,2), nrow=2))
b <- pmvnorm(lower=-Inf, upper=c(2,2)/sqrt(2), mean = c(1,3)/sqrt(2), corr = matrix(c(1,0.5,0.5,1), nrow=2))
print(sprintf("a = %f, b = %f", a, b))




# Example with correlation, different variances and non-zero means. 
a <- pmvnorm(lower=-Inf, upper=c(3,2.5), mean = c(1,3), sigma = matrix(c(3,1,1,4), nrow=2))
b <- pmvnorm(lower=-Inf, 
             upper=c(3/sqrt(3), 2.5/sqrt(4)), 
             mean = c(1/sqrt(3), 3/sqrt(4)), 
             corr = matrix(c(1,1/sqrt(3)/sqrt(4),1/sqrt(3)/sqrt(4),1), nrow=2))
print(sprintf("a = %f, b = %f", a, b))




#--------------------------------------------------
# Compare alternative calculations of the probabilities wrt scaling. 
#--------------------------------------------------
# Example specific to judicial model.

# delta_0 <- 0.25
delta_0 <- 0.1

dis_av_pars <- dis_aversn_params(mu_in = c(1, 2, 3), delta = delta_0)


dis_av_pars$mu

dis_av_pars$D_inv

dis_av_pars$Sigma


lower_bd <- -2
upper_bd <- 5.5

# Standard approach as is.


# Calculate the probability. 
a <- pmvnorm(lower = lower_bd, 
             upper = upper_bd, 
             mean = as.numeric(dis_av_pars$mu),
             # corr = param_list$Sigma,
             sigma = dis_av_pars$Sigma)



# Standardizing for unit diagonal on Sigma. 
b <- pmvnorm(lower = lower_bd/sqrt(dis_av_pars$Sigma[1,1]), 
             upper = upper_bd/sqrt(dis_av_pars$Sigma[1,1]), 
             mean = as.numeric(dis_av_pars$mu)/sqrt(dis_av_pars$Sigma[1,1]),
             # corr = param_list$Sigma,
             sigma = dis_av_pars$Sigma/dis_av_pars$Sigma[1,1])


print(sprintf("a = %f, b = %f", a, b))


# It works exactly like I would expect. 


