############################################
##  Intro. à Inferência Bayesiana - Lista 2
##  -> Questão 2
############################################
library(TeachingDemos)
library(ggplot2)
library(latex2exp)
library(pscl)
library(R2OpenBUGS)
library(coda)
library(lattice)
library(gridExtra)

# A) Evaluating the prior given the hyperparameters (a,b)
# ----------------------------------------------------------
# Hyperparameters
a1 <- 1; b1 <- 0.001
a2 <- 1; b2 <- 1000

# Prior distribution visualization
lambda_sup1 <- seq(0, 10, 0.01); lambda_sup2 <- seq(0, 0.01, 0.0001)
df1 <- data.frame(x=lambda_sup1, 
                 y=dgamma(lambda_sup1, a1, b1))
df2 <- data.frame(x=lambda_sup2, 
                 y=dgamma(lambda_sup2, a2, b2))

p1 <- ggplot(df1, aes(x)) +
  geom_line(aes(y=y), colour="#2A2A2A", size=0.5) +
  ylab(TeX("Priori I")) + xlab(TeX("$\\lambda$")) +
  ylim(c(0, 0.002)) +
  theme_minimal()
    
p2 <- ggplot(df2, aes(x)) +
  geom_line(aes(y=y), colour="#2A2A2A", size=0.5) +
  ylab(TeX("Priori II")) + xlab(TeX("$\\lambda$")) +
  theme_minimal()


pdf("res/Q2_A_prioris.pdf", width=8, height=3.5)
grid.arrange(p1, p2, nrow = 1)
dev.off()
  
# B) Plotting the Tri-Plot
# ----------------------------------------------------------
# Data
x <- c(6, 6, 2, 6, 5, 8, 3, 6, 4, 5)

# MLE Estimator
lmbd_mle <- sum(x)/length(x)

# Tri-plot visualization
support <- seq(0, 12, 0.01)
df <- data.frame(x =support, 
                 y1=dgamma(support, a1, b1),
                 y2=dpois(support, lmbd_mle),
                 y3=dgamma(support, a1 +sum(x), b1 +length(x)))

ggplot(df, aes(x)) +
  geom_line(aes(y=y3, colour="Posterior"), size=0.6) +
  geom_bar(aes(y=y2, colour="Likelihood"), stat="identity", size=0.5) +
  geom_line(aes(y=y1, colour="Prior"), linetype="dashed", size=0.5) +
  ylab(" ") + xlab(TeX("$\\theta$")) +
  theme_minimal() +
  theme(legend.title = element_blank(), legend.position = "top", axis.text.y=element_blank())

ggsave("../res/Q2_B_triplot.pdf", units='cm', width=16, height=7)

# C) Calculating the Bayesian estimators
# ----------------------------------------------------------
ap <- a1 +sum(x); bp <- b1 +length(x)
lambda_rsq  <- (ap)/(bp)                    # (Squared Loss)
lambda_rabs <- median(rgamma(100000, ap, bp)) # (Absolute Loss)
lambda_r01  <- (ap-1)/(bp)                  # (0-1 Loss)

# Tri-plot visualization
ggplot(df, aes(x)) +
  geom_line(aes(y=y3), colour="#2A2A2A", size=0.5) +
  geom_vline(aes(xintercept=lambda_rsq, color="Squared Loss"), linetype="dashed") +
  geom_vline(aes(xintercept=lambda_rabs, color="Absolute Loss"), linetype="dashed") +
  geom_vline(aes(xintercept=lambda_r01, color="0-1 Loss"), linetype="dashed") +
  ylab(" ") + xlab(TeX("$\\lambda$")) +
  theme_minimal() +
  theme(legend.title = element_blank(), legend.position = "top", axis.text.y=element_blank())
  
# D) OpenBUGS simulation of the model
#  & E) Compare with the estimators found in C)
# ----------------------------------------------------------
data   <- list(x=c(6, 6, 2, 6, 5, 8, 3, 6, 4, 5), n=10, a=a1, b=b1)
inits  <- function() { list(lambda = 5) }
params <- c("lambda")

out <- bugs(data, inits, params, model.file="model_Q2.txt", 
            n.iter=25000, n.chains=1, codaPkg=TRUE)

# Visualization
codaOut       <- read.bugs(out)
codaOutValues <- as.data.frame(as.matrix(codaOut))
  
summary(codaOut[,"lambda"])
densityplot(codaOut[,"lambda"])

# F) Find a 80% Confidence Interval using BUGS and R
# ----------------------------------------------------------
CI80_bugs <- HPDinterval(codaOut[,"lambda"], prob=.8) # Using the OpenBugs model
CI80_r    <- hpd(qgamma, shape=ap, rate=bp, conf=0.8) # Using the Posterior distribution

# G) Find the posterior predictive distribution
# ----------------------------------------------------------
# -- Using the OpenBugs model
data   <- list(x=c(6, 6, 2, 6, 5, 8, 3, 6, 4, 5), n=10, a=a1, b=b1)
inits  <- function() { list(lambda = 5) }
params <- c("lambda", "x_pred")

out <- bugs(data, NULL, params, model.file="model_Q2.txt", 
            n.iter=25000, n.chains=1, codaPkg=TRUE)

# Visualization
codaOut       <- read.bugs(out)
densplot(codaOut[,"x_pred"])

# -- Using a calculated posterior predictive
neg.binomial <- function(x, a, b) {
  return( choose(x+a-1, a-1) * (b/(b+1))^a * (1/(b+1))^x)
}

# Visualization
df <- data.frame(x=seq(0,20), y=neg.binomial(seq(0,20), ap, bp))

ggplot(df, aes(x)) +
  geom_histogram(aes(y=y), stat="identity") +
  ylab(" ") + xlab(TeX("$\\x_{n+1}$")) +
  theme_minimal()

# G) Find a estimative of x[n+1] and the associated error
# ----------------------------------------------------------
# -- Using the OpenBugs model
summary(codaOut[,'x_pred'])

# -- Using a calculated posterior predictive
x_til       <- ap / bp
x_til_error <- sqrt(ap/bp^2 * (bp+1) )

#
