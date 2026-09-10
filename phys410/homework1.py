import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint





def main():

    problem_four("a")

    problem_four("b")


def problem_four(part):
    # Constants
    R = 5
    g = 9.8

    # Pendulum ODE system
    def pendulum(y, t):
        phi, omega = y

        dphi_dt = omega
        domega_dt = -(g / R) * np.sin(phi)

        return [dphi_dt, domega_dt]

    # Initial conditions
    if part.lower() == "a":
        phi0 = np.deg2rad(15)
        omega0 = 0

    elif part.lower() == "b":
        phi0 = np.deg2rad(90)
        omega0 = 0

    else:
        raise ValueError("Part must be 'a' or 'b'.")

    y0 = [phi0, omega0]

    # Time interval
    dt = 0.25
    tspan = np.arange(0, 10 + dt, dt)

    # Numerical solution
    sol = odeint(pendulum, y0, tspan)

    phi = sol[:, 0]

    # Small-angle approximation
    phi_small = phi0 * np.cos(np.sqrt(g / R) * tspan)

    # Plot
    plt.figure(figsize=(8, 5))

    plt.plot(
        tspan,
        phi,
        label="Numerical solution",
        color="navy"
    )

    plt.plot(
        tspan,
        phi_small,
        "--",
        label="Small-angle approximation",
        color="red"
    )

    plt.xlabel("Time [s]")
    plt.ylabel(r"$\phi$ [rad]")
    plt.title(f"Pendulum Motion - Case {part.upper()}")

    plt.grid(ls="--")
    plt.legend()

    plt.show()


# Run problem 4
if __name__ == "__main__":

    main()