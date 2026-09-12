# needed libraries
import numpy as np
import matplotlib.pyplot as plt

# Defining distrubiton functions and helper functions for variance and mean
def variance(var):
    pass

def binomial(var):
    pass

def possion(var):
    pass

def guassian(var):
    pass

# spacial span
dn = 1
ni = 0
nf = 10
n = np.arange(ni, nf+dn, dn)

# pass variable through functions
normal_dis = guassian(n)
possion_dis = possion(n)
binomial_dis = binomial(n)

# plotting
plt.figure(figsize=(8, 5))
plt.plot(n, normal_dis, color = "Red", label = "Guassian Distribution")
plt.plot(n, normal_dis, color = "Purple", label = "Possion Distribution")
plt.plot(n, normal_dis, color = "Green", label = "Binomial Distribution")
plt.title("Figure 1: Comparing Distributions")
plt.xlabel("N Events")
plt.ylabel("Probability Density")
plt.legend(loc = "best")
plt.grid(ls = "--")
plt.show()
