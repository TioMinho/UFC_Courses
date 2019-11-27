############################################
##  Intro. à Inferência Bayesiana - Lista 2
##  -> Questão 3
############################################
library(TeachingDemos)
library(ggplot2)
library(latex2exp)
library(pscl)
library(R2OpenBUGS)
library(coda)
library(lattice)
library(gridExtra)
library(Rlab) # Bernoulli Distribution

# A) Constructs the model given the information in the question
# ----------------------------------------------------------
# Calculating the Beta Distribution parameters
mu <- 0.05; s2 <- 0.01;
a <- ((1-mu)/s2 - 1/mu)*mu^2
b <- a*(1/mu - 1)

# -- Visualization
# Data
x = sample(c(rep(1, 40), rep(0, 460)))

# MLE Estimator
theta_mle = sum(x)/length(x)

# Plot Prior/Likelihood/Posterior
support <- seq(0, 1, 0.001)
df <- data.frame(x =support, 
                 y1=dbeta(support, a, b),
                 #y2=dbern(support, theta_mle),
                 y3=dbeta(support, a +sum(x), b +length(x)-sum(x)))

ggplot(df, aes(x)) +
  geom_line(aes(y=y1, colour="Prior"), linetype="dashed", size=0.5) +
  #geom_histogram(aes(y=y2, colour="Likelihood"), stat="identity", linetype="dotdash", size=0.5) +
  geom_line(aes(y=y3, colour="Posterior"), size=0.6) +
  ylab(" ") + xlab(TeX("$\\theta$")) +
  xlim(c(0,0.14)) +
  theme_minimal() +
  theme(legend.title = element_blank(), legend.position = "top", axis.text.y=element_blank())

ggsave("res/triplot.pdf", units='cm', width=16, height=9)

# B) Find the Bayesian Estimators
# ----------------------------------------------------------
ap <- a +sum(x); bp <- b +length(x)-sum(x);
theta_rsq  <- (ap)/(ap+bp)                   # (Squared Loss)
theta_rabs <- median(rbeta(100000, ap, bp))  # (Absolute Loss)
theta_r01  <- (ap-1)/(ap+bp-2)               # (0-1 Loss)

# Tri-plot visualization
support <- seq(0, 0.2, 0.001)
df <- data.frame(x =support, y=dbeta(support, ap, bp))

ggplot(df, aes(x)) +
  geom_line(aes(y=y), colour="#2A2A2A", size=0.5) +
  geom_vline(aes(xintercept=theta_rsq, color="Squared Loss"), linetype="dashed") +
  geom_vline(aes(xintercept=theta_rabs, color="Absolute Loss"), linetype="dashed") +
  geom_vline(aes(xintercept=theta_r01, color="0-1 Loss"), linetype="dashed") +
  ylab(" ") + xlab(TeX("$\\theta$")) +
  theme_minimal() +
  theme(legend.title = element_blank(), legend.position = "top", axis.text.y=element_blank())

# C) Find a 90% Confidence interval for the model
# ----------------------------------------------------------
CI90_r <- hpd(qbeta, shape1=ap, shape2=bp, conf=0.9)  # Using the Posterior distribution

# Visualization
ggplot(df, aes(x)) +
  geom_line(aes(y=y), colour="#2A2A2A", size=0.5) +
  geom_vline(aes(xintercept=CI90_r[1]), color="blue", linetype="dashed") +
  geom_vline(aes(xintercept=CI90_r[2]), color="blue", linetype="dashed") +
  ylab(" ") + xlab(TeX("$\\theta$")) +
  theme_minimal() +
  theme(axis.text.y=element_blank())

# D) OpenBUGS simulation of the model
# ----------------------------------------------------------
data   <- list(x=40)
inits  <- function() { list(theta = 0.5) }
params <- c("theta")

out <- bugs(data, NULL, params, model.file="model_Q3.txt", 
            n.iter=25000, n.chains=1, codaPkg=TRUE)

# Visualization
codaOut       <- read.bugs(out)
codaOutValues <- as.data.frame(as.matrix(codaOut))

summary(codaOut[,"theta"])
densityplot(codaOut[,"theta"])  

# E) Found a estimate of the Posterior Predictive using OpenBUGS
# ----------------------------------------------------------
data   <- list(x=40)
inits  <- function() { list(theta = 0.5) }
params <- c("theta", "x_pred")

out <- bugs(data, NULL, params, model.file="model_Q3.txt", 
            n.iter=25000, n.chains=1, codaPkg=TRUE)

# Visualization
codaOut       <- read.bugs(out)
codaOutValues <- as.data.frame(as.matrix(codaOut))

summary(codaOut[,"x_pred"])
densplot(codaOut[,"x_pred"])  

# F) Found a 90% Confidence Interval for Theta using OpenBUGS
# ----------------------------------------------------------
CI90_bugs <- as.data.frame(HPDinterval(codaOut[,"theta"], prob=.9))

# Visualization
df <- data.frame(x=codaOutValues$theta)

ggplot(df, aes(x)) +
  geom_density(colour="#2A2A2A", size=0.5) +
  geom_vline(aes(xintercept=CI90_bugs$lower), color="blue", linetype="dashed") +
  geom_vline(aes(xintercept=CI90_bugs$upper), color="blue", linetype="dashed") +
  ylab(" ") + xlab(TeX("$\\theta$")) +
  theme_minimal() +
  theme(axis.text.y=element_blank())
