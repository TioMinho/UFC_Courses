############################################
##  Intro. à Inferência Bayesiana - Lista 2
##  -> Questão 7
############################################
library(TeachingDemos)
library(ggplot2)
library(latex2exp)
library(pscl)
library(R2OpenBUGS)
library(coda)
library(lattice)
library(gridExtra)

# A) Modelling the prior distribution
# ----------------------------------------------------------
# Computing the inverse-gamma hyperparameters
a <- 20.25/10; b <- 0.5*(a-1)


# B) Compute the posterior estimative of the regression parameters
# ----------------------------------------------------------
data <- list(y=stack.loss, x=stack.x, n=21,
             a1=a, b1=b)
inits <- function() { list(tau=1, b=rnorm(4,0,2)) }
params <- c("tau","b","mu")

out <- bugs(data, inits, params, model.file="model_Q7.txt",
            n.iter=25000, n.chains=1, codaPkg=TRUE)

codaOut <- read.bugs(out)
summary(codaOut[,c('b[1]', 'b[2]', 'b[3]', 'b[4]')])

# C) Find credible intervals to the parameters
# ----------------------------------------------------------
HPDinterval(codaOut[,c('b[1]', 'b[2]', 'b[3]', 'b[4]')], prob=0.95)

# E) Plot the residues
# ----------------------------------------------------------
mu_means <- summary(codaOut[,6:(5+21)])$statistics[,1]

plot(seq(1,length(stack.loss)), (mu_means-stack.loss), pch=4)
abline(h = 0)

# F) Run the model using a non-informative prior
# ----------------------------------------------------------
data <- list(y=stack.loss, x=stack.x, n=21)
inits <- function() { list(s2=runif(1,-10000, 10000), b=rnorm(4,0,2)) }
params <- c("s2","p","px","b","mu")

out <- bugs(data, inits, params, model.file="model_Q7b.txt",
            n.iter=25000, n.chains=1, codaPkg=TRUE)

codaOut <- read.bugs(out)
summary(codaOut[,c('b[1]', 'b[2]', 'b[3]', 'b[4]')])

# G) Compute the probability of P(s2 > 1)
# ----------------------------------------------------------
summary(codaOut[,c('p[1]')])

# H) Compare the models
# ----------------------------------------------------------
mu_means <- summary(codaOut[,6:(5+21)])$statistics[,1]

plot(seq(1,length(stack.loss)), (mu_means-stack.loss), pch=4)
abline(h = 0)
title(paste("RSE = ", round(sum((mu_means-stack.loss)^2), 3)))

# I) Predict the three new datapoints and compute the associated error
# ----------------------------------------------------------
summary(codaOut[,c('px[1]', 'px[2]', 'px[3]')])
