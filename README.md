# Reflection_Appeals

Identification and Estimation in Judicial Panel Voting


## Simulation Evidence

I conducted some simulations to determine whether we can
identify the parameters of the econometric model. 

### Intercept for means, full off-diagonal covariance matrix

The first model that I considered is a trivariate probit model
with parameters that include 
a vector of mean values and 
a covariance matrix with variances restricted to one. 
This variant of the model has 6 free parameters. 

This simulation had these parameter inputs:

```
# Number of replications for simulation of estimation.
num_reps <- 100

# Number of appeals court cases.
n_cases <- 1000


# Average intents of three appeals court judges.
mu_0 <- c(1, 0, -1)

# Covariance matrix of taste shifters.
Sigma_0 <- matrix(c(1.0, 0.8, 0.2,
                    0.8, 1.0, 0.5,
                    0.2, 0.5, 1.0), ncol = 3)
```

In the first instance, I chose a sample size of 100
and noticed some numerical issues (we'll fix it later), 
so I cranked up the sample size to see if it helped. 

It did, but the estimation took a long time, 
so after two iterations, a few minutes later, 
I estimated how long it would take and began coding the next model.  
By the time I was ready to test the next model, 
we had made it to 35 iterations. 

Clearly more restrictions are in order, 
unless we use a more efficient algorithm. 

In any case, these are some preliminary results:

```
mu_1             mu_2               mu_3
Min.   :0.8618   Min.   :-0.09456   Min.   :-1.0914
1st Qu.:0.9738   1st Qu.:-0.01810   1st Qu.:-1.0517
Median :0.9924   Median : 0.00724   Median :-1.0038
Mean   :0.9922   Mean   : 0.00679   Mean   :-1.0063
3rd Qu.:1.0256   3rd Qu.: 0.03965   3rd Qu.:-0.9744
Max.   :1.0646   Max.   : 0.07614   Max.   :-0.8935
NA's   :65       NA's   :65         NA's   :65

    Sigma_21         Sigma_31          Sigma_32
 Min.   :0.7614   Min.   :0.02531   Min.   :0.3488
 1st Qu.:0.7931   1st Qu.:0.14109   1st Qu.:0.4544
 Median :0.8102   Median :0.20491   Median :0.4822
 Mean   :0.8118   Mean   :0.19694   Mean   :0.4899
 3rd Qu.:0.8299   3rd Qu.:0.24557   3rd Qu.:0.5265
 Max.   :0.8919   Max.   :0.35464   Max.   :0.5835
 NA's   :65       NA's   :65        NA's   :65
```

The mean is easier to estimate than the covariance.
In the next model, I will place more restrictions
on the covariance matrix.


### Intercept for means, identity covariance matrix

To reduce the set of parameters to be estimated, 
I restricted the off-diagonal elements to zero. 

This model has only the three parameters in the mean vector
of latent intents. 


This simulation had these parameter inputs:

```
# Number of replications for simulation of estimation.
num_reps <- 100

# Number of appeals court cases.
n_cases <- 100

# Average intents of three appeals court judges.
mu_0 <- c(1, 0, -1)


# Design of sigma depends on the chosen model.
model_name <- 'mu_only'
param_0 <- mu_0

> Sigma_0
[,1] [,2] [,3]
[1,]    1    0    0
[2,]    0    1    0
[3,]    0    0    1
```

These were the estimates:

```
mu_1             mu_2                 mu_3
Min.   :0.6433   Min.   :-2.275e-01   Min.   :-1.4758
1st Qu.:0.9154   1st Qu.:-7.527e-02   1st Qu.:-1.1264
Median :0.9945   Median :-2.900e-07   Median :-0.9945
Mean   :1.0242   Mean   :-1.436e-03   Mean   :-1.0142
3rd Qu.:1.1264   3rd Qu.: 7.527e-02   3rd Qu.:-0.9154
Max.   :1.4758   Max.   : 3.055e-01   Max.   :-0.5244
```

It works much better with an identity restriction on the
covariance matrix but 100 observations does not buy us much accuracy, 
even for the simple equation with intercepts for mean latent intents.

At least estimating the mean equation is numerically stable
with only 100 observations.



### Intercept for means, single-valued off-diagonal covariance matrix


Perhaps, the most we should have in the covariance matrix is a 
constant pairwise correlation across judges. 
This is the next model. 

I extended the set of parameters in the model
to restrict the off-diagonal elements of the covariance matrix 
to have equal-valued pairwise taste-shifters. 

This model has four parameters in total. 


```
# Number of replications for simulation of estimation.
num_reps <- 100

# Number of appeals court cases.
n_cases <- 100

# Average intents of three appeals court judges.
mu_0 <- c(1, 0, -1)



model_name <- 'mu_const'
param_0 <- c(mu_0, 0.5)

> Sigma_0
[,1] [,2] [,3]
[1,]  1.0  0.5  0.5
[2,]  0.5  1.0  0.5
[3,]  0.5  0.5  1.0
```


These were the results:

```
> summary(estn_results)
      mu_1             mu_2                mu_3            Sigma_21     
 Min.   :0.6000   Min.   :-0.366955   Min.   :-1.4286   Min.   :0.2020  
 1st Qu.:0.9166   1st Qu.:-0.066088   1st Qu.:-1.1294   1st Qu.:0.4423  
 Median :0.9997   Median : 0.004488   Median :-0.9964   Median :0.5087  
 Mean   :1.0050   Mean   : 0.018097   Mean   :-1.0190   Mean   :0.5111  
 3rd Qu.:1.1051   3rd Qu.: 0.124450   3rd Qu.:-0.9040   3rd Qu.:0.5716  
 Max.   :1.3972   Max.   : 0.341538   Max.   :-0.5968   Max.   :0.8187 
 ```
 
 
Again, it appears to work, aside from the variation from the small sample size.



