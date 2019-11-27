############################################
##  Intro. à Inferência Bayesiana - Lista 2
##  -> Questão 6
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
mu = 0.4; sd2 <- 0.001;
a <- ((1-mu)/sd2 - 1/mu)*mu^2
b <- a*(1/mu - 1)

# Finds the variance that leads to P(theta < 60%) ~= 95%
while(pbeta(0.6, a, b) > 0.95) {
  sd2 <- sd2*1.0001;
  a <- ((1-mu)/sd2 - 1/mu)*mu^2
  b <- a*(1/mu - 1)
}

# B) Simulating the BUGS model
# ----------------------------------------------------------
data   <- list(x=sample(c(rep(1,15), rep(0,85))), n=100,
               a=a, b=b)
params <- c("theta")

out <- bugs(data, NULL, params, model.file="model_Q6.txt",
            n.iter=25000, n.chains=1, codaPkg=TRUE)

codaOut <- read.bugs(out)
