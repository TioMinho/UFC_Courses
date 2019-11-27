############################################
##  Intro. à Inferência Bayesiana - Lista 2
##  -> Questão 1
############################################
library(TeachingDemos)
library(ggplot2)
library(latex2exp)
library(pscl)
library(R2OpenBUGS)
library(coda)

# A) Triplot of the Prior/Likelihood/Posterior distributions
# ----------------------------------------------------------
# Data
y = c(1, 1, 2, 2, 4, 5, 4, 4, 6, 7)

# MLE Estimator
s2 = sum(log(y)^2)/length(y)

# Plot Prior/Likelihood/Posterior
support <- seq(0.0000001, 10, 0.01)
df <- data.frame(x =support, 
                 y1=densigamma(support, 3, 8),
                 y2=dlnorm(support, 0, s2),
                 y3=densigamma(support, 3 +length(y)/2, 8 +0.5*sum(log(y)^2)))

ggplot(df, aes(x)) +
  geom_line(aes(y=y1, colour="Prior"), linetype="dashed", size=0.5) +
  geom_line(aes(y=y2, colour="Likelihood"), linetype="dotdash", size=0.5) +
  geom_line(aes(y=y3, colour="Posterior"), size=0.6) +
  ylab(" ") + xlab(TeX("$\\theta$")) +
  theme_minimal() +
  theme(legend.title = element_blank(), legend.position = "top", axis.text.y=element_blank()) +
  #geom_vline(xintercept=hpd(qigamma, alpha=3 +length(y)/2, beta=8 +0.5*sum(log(y)^2), conf=0.50))

ggsave("../res/Q1_A_triplot.pdf", units='cm', width=16, height=9)


# C) Finding a (100-a)% credible interval for \theta with a = 5
# -------------------------------------------------------------
# Utilizing the function 'hpd' (TeachingDemos)
hpd(qigamma, alpha=3 +length(y)/2, beta=8 +0.5*sum(log(y)^2), conf=0.950)

# Utilizing the function quantiles
theta_sample = rigamma(10000, 3 +length(y)/2, 8 +0.5*sum(log(y)^2))
quantile(theta_sample, probs=c(0.025, 0.975))

# D) Modeling using OpenBUGS and comparing the estimators
#  & E) Obtain the expression for the posterior predictive distribution
# -------------------------------------------------------------
# Simulate the model
model.file = paste(getwd(), "data", "model_Q1.txt", sep='/')
data       = list(y = c(1, 1, 2, 2, 4, 5, 4, 4, 6, 7), n=10)
params     = c("theta")
inits      = function() { list(tau=1) } 

out <- bugs(data, inits, params, model.file, 
         n.iter=10000, n.chains = 1, codaPkg = TRUE)

out.coda       <- read.bugs(out)
out.codaValues <- as.data.frame(as.matrix(read.bugs(out)))
summary(out.coda)

#
