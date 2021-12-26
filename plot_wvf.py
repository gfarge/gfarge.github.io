""" Plots my favicon """

# Imports
# =======
import numpy as np
import matplotlib.pyplot as plt


# Core
# ====
nu = 2.5  # frequency
sigma = 2  # gaussian width

X = np.arange(-1, 1, 1/100) * 2*np.pi
Y = np.sin(X*nu) * np.exp(-X**2/2/sigma**2)


# Plot
# ====
c = '#ff1493'

fig, ax = plt.subplots(facecolor=[0, 0, 0, 1], figsize=(1, 1))
fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
ax.axis('off')

ax.plot(X, Y, lw=4, c=c, solid_joinstyle='round', solid_capstyle='round')

plt.savefig('my_favicon.png', dpi=260, facecolor=[0, 0, 0, 0])

plt.show()
