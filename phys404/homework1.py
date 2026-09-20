# needed libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial

# plotting
def parts_for_hw(section):

    # Defining distribution functions
    def guassian(x, mean, std):  # Continuous
        prob = 1/(np.sqrt(2*np.pi*std**2)) * np.exp(-(x-mean)**2 / (2*std**2))
        return prob

    def possion(n, mean):  # Discrete
        prob = (mean)**n / factorial(n) * np.exp(-mean)
        return prob

    def binomial(n, N, p):  # Discrete
        prob = (factorial(N))/(factorial(n)*factorial(N-n)) * p**n * (1-p)**(N-n)
        return prob
    
    # spatial span [for Gaussian]
    dx = 0.001
    xi = 0
    xf = 10
    x = np.arange(xi, xf+dx, dx)

    # index span [for Poisson and Binomial]
    dn = 1
    ni = 0
    nf = 10
    n = np.arange(ni, nf+dn, dn)

    # pass variable through functions
    if section == 1:
        normal_dis = guassian(x=x, mean=1, std=0.5)
        binomial_dis = binomial(n=n, N=10, p=0.1)
        possion_dis = possion(n=n, mean=1)

    elif section == 2:
        normal_dis = guassian(x=x, mean=2, std=1)
        binomial_dis = binomial(n=n, N=10, p=0.2)
        possion_dis = possion(n=n, mean=2)

    else:
        raise ValueError("Not an option")

    # plotting
    plt.figure(figsize=(8, 5))

    plt.plot(
        x, normal_dis,
        color="Red",
        label="Gaussian Distribution"
    )

    plt.plot(
        n, possion_dis,
        color="Purple",
        marker="o", ls="--",
        label="Poisson Distribution"
    )

    plt.plot(
        n, binomial_dis,
        color="Green",
        marker="o", ls="--",
        label="Binomial Distribution"
    )

    plt.title(f"Section {section}: Comparing Distributions")
    plt.xlabel("Sample Value")
    plt.ylabel("Probability / Probability Density")
    plt.xlim(xi, xf)
    plt.legend(loc="best")
    plt.grid(ls="--")

    plt.show()


parts_for_hw(1)
parts_for_hw(2)