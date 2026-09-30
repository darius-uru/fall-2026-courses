import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# given values
m = 1200
c = 400
Kp = 500
Kd = 1800
H = 3.5
taus = [1, 2, 3]
colors = ["red", "blue", "green"]

# time
t = np.linspace(0, 25, 5000)

# initial conditions [position, velocity, acceleration]
initial = [0, 0, 0]

# elevator differential equation
def elevator(z, t, tau):
    x = z[0]
    v = z[1]
    a = z[2]
    jerk = (Kp*H - Kp*x - (c + Kd)*v - (m + tau*c)*a) / (tau*m)
    return [v, a, jerk]

# solve for each value of tau
results = {}
for tau in taus:
    sol = odeint(elevator, initial, t, args=(tau,))
    x = sol[:, 0]
    v = sol[:, 1]
    a = sol[:, 2]
    # use the differential equation to get jerk
    j = (Kp*H - Kp*x - (c + Kd)*v - (m + tau*c)*a) / (tau*m)
    results[tau] = [x, v, a, j]

# make plots
fig, ax = plt.subplots(2, 2, figsize=(12, 8))
for tau, color in zip(taus, colors):

    ax[0, 0].plot(t, results[tau][0],color=color,label=rf"$\tau$ = {tau} s")
    ax[0, 1].plot(t, results[tau][1],color=color,label=rf"$\tau$ = {tau} s")
    ax[1, 0].plot( t, results[tau][2], color=color,label=rf"$\tau$ = {tau} s")
    ax[1, 1].plot( t, results[tau][3], color=color, label=rf"$\tau$ = {tau} s")

# target height
ax[0, 0].axhline( H,color="black",linestyle="--",label="Target Height")
# maximum height on position plot
for tau, color in zip(taus, colors):
    x = results[tau][0]
    max_height = np.max(x)
    max_index = np.argmax(x)
    max_time = t[max_index]
    # mark maximum height
    ax[0, 0].plot(max_time, max_height,"o",color=color)
    # label maximum height
    ax[0, 0].annotate(f"{max_height:.3f} m",(max_time, max_height),xytext=(5, 8),textcoords="offset points",color=color,fontsize=9)
# jerk limits
ax[1, 1].axhline( 0.8,color="black",linestyle="--",label=r"Comfort Limit: $|j|=0.80$ m/s$^3$")

ax[1, 1].axhline( -0.8, color="black", linestyle="--")

# maximum jerk values
jerk_text = ""
for tau in taus:
    max_jerk = np.max(np.abs(results[tau][3]))
    jerk_text += (
        rf"$\tau={tau}$ s: "
        rf"{max_jerk:.3f} m/s$^3$"
        "\n")

# put maximum jerk values on jerk plot
ax[1, 1].text(0.97,0.05,jerk_text,transform=ax[1, 1].transAxes,horizontalalignment="right",verticalalignment="bottom",bbox=dict(facecolor="white",alpha=0.8))

# labels
ax[0, 0].set_title("Position")
ax[0, 0].set_xlabel("Time [s]")
ax[0, 0].set_ylabel("Position [m]")

ax[0, 1].set_title("Velocity")
ax[0, 1].set_xlabel("Time [s]")
ax[0, 1].set_ylabel("Velocity [m/s]")

ax[1, 0].set_title("Acceleration")
ax[1, 0].set_xlabel("Time [s]")
ax[1, 0].set_ylabel(r"Acceleration [m/s$^2$]")

ax[1, 1].set_title("Jerk")
ax[1, 1].set_xlabel("Time [s]")
ax[1, 1].set_ylabel(r"Jerk [m/s$^3$]")

# grid and legends
for row in ax:
    for plot in row:
        plot.grid()
        plot.legend()

plt.tight_layout()
# save figure
plt.savefig( "PHYS410_HW2_Problem5_partA.png",dpi=300, bbox_inches="tight")
plt.show()
# maximum jerk for each elevator
for tau in taus:
    max_jerk = np.max(np.abs(results[tau][3]))
    print( "tau =", tau,"s | max jerk =",round(max_jerk, 3),"m/s^3")