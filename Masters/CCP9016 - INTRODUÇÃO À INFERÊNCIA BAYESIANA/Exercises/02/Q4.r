############################################
##  Intro. à Inferência Bayesiana - Lista 2
##  -> Questão 4
############################################
library(TeachingDemos)
library(ggplot2)
library(latex2exp)
library(pscl)
library(R2OpenBUGS)
library(coda)
library(lattice)
library(gridExtra)

# B) Using OpenBUGS gather evidence about 'a' and 'b'
#   from the posterior predictive distribution
# ----------------------------------------------------------
data   <- list(x=c(0.1,0.3,0.3,0.2,0.5,0.7,0.1,0.6,0.7,0.2), n=10)
inits  <- function() { list(a=1, b=2) }
params <- c("a", "b", "x_pred")

out <- bugs(data, NULL, params, model.file="model_Q4.txt",
            n.iter=10000, n.chains=1, codaPkg=TRUE)

codaOut       <- read.bugs(out)
codaOutValues <- as.data.frame(as.matrix(codaOut))

# Summarization
smm_x <- summary(codaOut[,"x_pred"])
x_mu  <- as.numeric(smm_x$statistics[1])
x_sd  <- as.numeric(smm_x$statistics[2])

# Calculating the parameters from the posterior predictive
a_pp <- ((1-x_mu)/x_sd^2 - 1/x_mu)*x_mu^2
b_pp <- a_pp*(1/x_mu - 1)

# -- Visualization
df <- data.frame(y=codaOutValues[,"x_pred"])

ggplot(df, aes(y)) +
  geom_density(color="#2A2A2A") +
  xlab(TeX("$\\tilde{x}$")) + ylab(TeX("$p(\\tilde{x} | x_1, \\cdots, x_n)$")) +
  theme_minimal()

# C) Estimate 'a' and 'b' from the Posterior Marginal distributions
# ----------------------------------------------------------
# Summarization
summary(codaOut[,c("a", "b")])

# Visualization
df <- data.frame(y1=codaOutValues[,"a"],
                 y2=codaOutValues[,"b"])

p1 <- ggplot(df, aes(y1)) +
  geom_density(color="#2A2A2A") +
  xlab(TeX("$\\alpha$")) + ylab(TeX("$p(\\alpha | x_1, \\cdots, x_n)$")) +
  theme_minimal()

p2 <- ggplot(df, aes(y2)) +
  geom_density(color="#2A2A2A") +
  xlab(TeX("$\\beta$")) + ylab(TeX("$p(\\beta | x_1, \\cdots, x_n)$")) +
  theme_minimal()
  
grid.arrange(p1, p2, nrow=1)

# D) Plot of the posterior predictive distribution given estimations
# ----------------------------------------------------------
# Get the parameter estimates
ab_means <- as.numeric(summary(codaOut[,c("a", "b")])$statistics[,1])
a_lsq <- ab_means[1]; b_lsq <- ab_means[2];

# Calculate the PDF for the given support
support <- seq(0, 1, 0.0001)
df <- data.frame(x=support, y=dbeta(support, a_lsq, b_lsq))

ggplot(df, aes(x)) +
  geom_line(aes(y=y), color="#2A2A2A") +
  xlab(TeX("$\\tilde{x}$")) + ylab(TeX("$p(\\tilde{x} | x_1, \\cdots, x_n)$")) +
  theme_minimal()

# E) Probability of P(X > 0.5)
# ----------------------------------------------------------
1 - pbeta(0.5, a_lsq, b_lsq)

# F) Compute 95% Credible intervals for 'a' and 'b' (OpenBUGS)
# ----------------------------------------------------------
HPDinterval(codaOut[,c('a','b')])
