
# Verifying the calculations for the matrices 
# governing the system of equations. 

dis_aversn_params <- function(mu_in, delta) {
  
  # Matrices to modify the system of equations for dissent aversion.
  # Examples:
  # dis_aversn_params(mu_in = c(1, 2, 3), delta = 0.25)
  # dis_aversn_params(mu_in = c(-1, -2, -3), delta = 0.25)
  # dis_aversn_params(mu_in = c(-1, 0, 1), delta = 0.25)
  # dis_aversn_params(mu_in = c(1, 2, 3), delta = 0.1)
  # dis_aversn_params(mu_in = c(-1, 0, 1), delta = 0.1)
  
  # Denominator common to matrices involving D_inverse. 
  den_D_inv <- 2*delta^2 + delta - 1
  
  # Calculate the transition matrix.
  D_inv <- diag(c(1,1,1))*(delta - 1)/den_D_inv
  
  # Fill in the lower triangle.
  D_inv[lower.tri(D_inv, diag = FALSE)] <- - delta/den_D_inv
  
  # Copy the upper triangle.  
  D_inv[upper.tri(D_inv, diag = FALSE)] <- 
    D_inv[lower.tri(D_inv, diag = FALSE)]
  
  
  # Multiply the mean intent vector by the "transition" matrix. 
  mu_out <- mu_in %*% D_inv
  
  # Adjust the covariance matrix.
  Sigma <- D_inv %*% D_inv
  
  dis_av_pars <- list(mu = mu_out, Sigma = Sigma, D_inv = D_inv)
  
  
  return(dis_av_pars) 
}




delta_0 <- 0.25
delta_0 <- 0.1


dis_av_pars <- dis_aversn_params(mu_in = c(1, 2, 3), delta = delta_0)




dis_av_pars$D_inv

dis_av_pars$Sigma


Delta <- matrix(rep(0, 9), ncol = 3)
Delta[lower.tri(Delta, diag = FALSE)] <- delta_0
Delta[upper.tri(Delta, diag = FALSE)] <- delta_0



D <- diag(rep(1, 3)) - Delta


solve(D)


dis_av_pars$D_inv
