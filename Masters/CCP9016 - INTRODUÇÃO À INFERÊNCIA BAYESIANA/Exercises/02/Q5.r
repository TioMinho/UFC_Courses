############################################
##  Intro. à Inferência Bayesiana - Lista 2
##  -> Questão 5
############################################
library(TeachingDemos)
library(ggplot2)
library(latex2exp)
library(pscl)
library(R2OpenBUGS)
library(coda)
library(lattice)
library(gridExtra)

# A) Model the problem conveniently
#  B) Find the best decision given the probabilities
# ----------------------------------------------------------
# Prior probabilities
ptheta_10 <- 0.5; ptheta_30 <- 0.3; ptheta_50 <- 0.2

# Likelihood probabilities
pX_theta_10 <- dbinom(8, 20, 0.1) 
pX_theta_30 <- dbinom(8, 20, 0.3)
pX_theta_50 <- dbinom(8, 20, 0.5)

pX <- (pX_theta_10*ptheta_10 + pX_theta_30*ptheta_30 + pX_theta_50*ptheta_50)

# Posterior probabilities
ptheta_X_10 <- (ptheta_10 * pX_theta_10) / pX
ptheta_X_30 <- (ptheta_30 * pX_theta_30) / pX
ptheta_X_50 <- (ptheta_50 * pX_theta_50) / pX

# C) Evaluate the hypothesis using posterior probabilities and risk table
# ----------------------------------------------------------
riskTable <- matrix(c(0, 1, 3,  
                      2, 0, 2,  
                      3, 1, 0), nrow=3, byrow=TRUE)
probs <- c(ptheta_X_10, ptheta_X_30, ptheta_X_50)

hypo_risk <- riskTable %*% probs


# E) Evaluate the hypothesis using a model with non-informative prior
# ----------------------------------------------------------
data   <- list(x=8)
params <- c("theta", "p")

out <- bugs(data, NULL, params, model.file="model_Q5.txt",
            n.iter=10000, n.chains=1, codaPkg=TRUE)

codaOut <- read.bugs(out)

# Hypothesis testing using only the probabilities
ptheta   <- summary(codaOut[,c("p[1]", "p[2]", "p[3]")])$statistics[,1]

# Hypothesis testing using also the risk table
hypo_risk <- riskTable %*% ptheta
