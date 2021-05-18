# Reflection_Appeals

Identification and Estimation in Judicial Panel Voting


# Simulation Evidence

I conducted some simulations to determine whether we can
identify the parameters of the econometric model. 

## Preliminary Models without Covariates

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
This is the design of the next model. 

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

The next step is to add covariates to the mean equation. 



## Models with Covariates (no peer effects nor dissent aversion)

### Common intercept for means, single-valued off-diagonal covariance matrix

By introducing covariates, we introduce a mean latent intent that depends
on the composition of the judiciary panel. 
Each judiciary panel is comprised of a permutation of three judges 
drawn from a pool of judges. 
Each judge has a vector of binary covariates and these covariates 
are stacked in a matrix, along with the triple of observed binary decisions. 


In the first model with covariates, there is a common intercept
and a common slope coefficient for the judge-specific covariates. 
The judges do not take into account the characteristics of the
other judges (no peer effects), 
nor the latent intent of other judges (no dissent aversion). 
These features are saved for later models. 

I ran a simulation, in which a dataset is formed with 
all permutations of judges, repeated several times. 
The only source of randomness is the shock to the latent intent. 

I set the following dimensions for the simulation
and the matrix of judicial panels:

```
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


```

I used the following parameter values:

```
# Average intents of three appeals court judges.
alpha_0 <- 0.25

# Slope coefficients on covariates common to all judges.
beta_0 <- c(1, 2)

# Correlation coefficient for the taste-shifters of pairs of judges.
# Off-diagonal element of Sigma
sigma_21 <- 0.5

# The parameter vector depends on the chosen model. 
model_name <- 'cov_const'
param_0 <- c(alpha_0, beta_0, sigma_21)

```

These were the estimation results:

```
> summary(estn_results)
     alpha            beta_1           beta_2         Sigma_21      
 Min.   :0.0106   Min.   :0.6609   Min.   :1.107   Min.   :0.09334  
 1st Qu.:0.1940   1st Qu.:0.8598   1st Qu.:1.990   1st Qu.:0.36962  
 Median :0.2768   Median :0.9896   Median :2.071   Median :0.49185  
 Mean   :0.2658   Mean   :0.9852   Mean   :2.061   Mean   :0.49026  
 3rd Qu.:0.3516   3rd Qu.:1.0861   3rd Qu.:2.184   3rd Qu.:0.61722  
 Max.   :0.5353   Max.   :1.3387   Max.   :4.175   Max.   :0.80175  
```

Again, these parameters appear to be unbiased estimates. 


## Models with Covariates and Peer Effects (no dissent aversion)



With peer effects, there is an additional parameter that is the 
slope coefficient of the covariates of the other judges. 
The mean latent intent for each judge depends on the common intercept, 
the contibution of the judge's own covariates, 
and the contribution of the covariates of the other two judges on the panel, 
with the same coefficients for each of the two cross-judge contributions. 


### Common intercept for means, single-valued off-diagonal covariance matrix



I set the same dimensions for the simulation
and the matrix of judicial panels as in the example above.



I used the following parameter values:

```
# Average intents of three appeals court judges.
# mu_0 <- c(1, 0, -1)
alpha_0 <- 0.25

# Slope coefficients on covariates for own characteristics, common to all judges.
beta_0 <- c(1, 2)

# Slope coefficients on covariates for peer effects, common to all judges.
gamma_0 <- c(-0.5, -1)

# Correlation coefficient for the taste-shifters of pairs of judges.
# Sigma is identity matrix. 

```



These were the estimation results:

```
> summary(estn_results)
     alpha             beta_1           beta_2         gamma_1           gamma_2       
 Min.   :-2.3383   Min.   :0.2237   Min.   :1.421   Min.   :-0.8929   Min.   :-1.2851  
 1st Qu.:-0.1296   1st Qu.:0.8026   1st Qu.:1.846   1st Qu.:-0.5807   1st Qu.:-1.0977  
 Median : 0.1053   Median :1.0434   Median :2.008   Median :-0.4751   Median :-0.9874  
 Mean   : 0.1657   Mean   :1.0523   Mean   :2.055   Mean   :-0.4837   Mean   :-0.9943  
 3rd Qu.: 0.5143   3rd Qu.:1.2624   3rd Qu.:2.183   3rd Qu.:-0.3851   3rd Qu.:-0.9038  
 Max.   : 1.7262   Max.   :3.2067   Max.   :4.016   Max.   :-0.2041   Max.   :-0.6265 
```


## Models with Covariates, Peer Effects and Dissent Aversion


# Work in Progress

Adding dissent aversion to the model changes the mean and covariance of the latent intent.
According to the following examples, 
it pushes a similarly-inclined panel further into the direction of agreement, 
in either the positive or negative direction. 
For judicial panels with a balance of intent, 
it pulls them toward indifference. 


```
> dis_aversn_params(mu_in = c(1, 2, 3), delta = 0.25)
$mu
     [,1] [,2] [,3]
[1,]  3.2    4  4.8

$Sigma
     [,1] [,2] [,3]
[1,] 1.76 1.12 1.12
[2,] 1.12 1.76 1.12
[3,] 1.12 1.12 1.76

$D_inv
     [,1] [,2] [,3]
[1,]  1.2  0.4  0.4
[2,]  0.4  1.2  0.4
[3,]  0.4  0.4  1.2

> dis_aversn_params(mu_in = c(-1, 0, 1), delta = 0.25)
$mu
     [,1] [,2] [,3]
[1,] -0.8    0  0.8

$Sigma
     [,1] [,2] [,3]
[1,] 1.76 1.12 1.12
[2,] 1.12 1.76 1.12
[3,] 1.12 1.12 1.76

$D_inv
     [,1] [,2] [,3]
[1,]  1.2  0.4  0.4
[2,]  0.4  1.2  0.4
[3,]  0.4  0.4  1.2

> dis_aversn_params(mu_in = c(-1, -2, -3), delta = 0.25)
$mu
     [,1] [,2] [,3]
[1,] -3.2   -4 -4.8

$Sigma
     [,1] [,2] [,3]
[1,] 1.76 1.12 1.12
[2,] 1.12 1.76 1.12
[3,] 1.12 1.12 1.76

$D_inv
     [,1] [,2] [,3]
[1,]  1.2  0.4  0.4
[2,]  0.4  1.2  0.4
[3,]  0.4  0.4  1.2

> dis_aversn_params(mu_in = c(1, 2, 3), delta = 0.1)
$mu
         [,1] [,2]     [,3]
[1,] 1.590909  2.5 3.409091

$Sigma
          [,1]      [,2]      [,3]
[1,] 1.0717975 0.2453512 0.2453512
[2,] 0.2453512 1.0717975 0.2453512
[3,] 0.2453512 0.2453512 1.0717975

$D_inv
          [,1]      [,2]      [,3]
[1,] 1.0227273 0.1136364 0.1136364
[2,] 0.1136364 1.0227273 0.1136364
[3,] 0.1136364 0.1136364 1.0227273

> dis_aversn_params(mu_in = c(-1, 0, 1), delta = 0.1)
$mu
           [,1] [,2]      [,3]
[1,] -0.9090909    0 0.9090909

$Sigma
          [,1]      [,2]      [,3]
[1,] 1.0717975 0.2453512 0.2453512
[2,] 0.2453512 1.0717975 0.2453512
[3,] 0.2453512 0.2453512 1.0717975

$D_inv
          [,1]      [,2]      [,3]
[1,] 1.0227273 0.1136364 0.1136364
[2,] 0.1136364 1.0227273 0.1136364
[3,] 0.1136364 0.1136364 1.0227273


```


### Common intercept for means, single-valued off-diagonal covariance matrix

In this model, the constant value of the off-diagonal covariance value
is implied by the degree of dissent aversion in the panel. 



I used the following parameter values:


```


# Average intents of three appeals court judges.
# mu_0 <- c(1, 0, -1)
alpha_0 <- 0.25

# Slope coefficients on covariates for own characteristics, common to all judges.
beta_0 <- c(1, 2)

# Slope coefficients on covariates for peer effects, common to all judges.
gamma_0 <- c(-0.5, -1)

# Dissent aversion parameter. 
delta_0 <- 0.1
```


These were the estimation results:


```
> summary(estn_results)
     alpha              beta_1           beta_2         gamma_1           gamma_2       
 Min.   :-0.70174   Min.   :0.5226   Min.   :1.532   Min.   :-6.6189   Min.   :-4.1750  
 1st Qu.:-0.34946   1st Qu.:1.4199   1st Qu.:1.786   1st Qu.:-1.1933   1st Qu.:-1.5617  
 Median :-0.14867   Median :2.1394   Median :1.933   Median :-0.5742   Median :-0.8307  
 Mean   :-0.04541   Mean   :2.3247   Mean   :1.963   Mean   :-0.5428   Mean   :-0.7532  
 3rd Qu.: 0.07904   3rd Qu.:3.0452   3rd Qu.:2.079   3rd Qu.: 0.3266   3rd Qu.:-0.1005  
 Max.   : 2.56986   Max.   :4.7733   Max.   :2.836   Max.   : 4.3712   Max.   : 2.6407  
     delta         
 Min.   :-0.73620  
 1st Qu.:-0.31288  
 Median :-0.24733  
 Mean   :-0.26717  
 3rd Qu.:-0.18938  
 Max.   :-0.06455  
```


