#!/usr/bin/env python3
"""
Minimal reproduction of the dataLim issue without external dependencies
"""

import sys
sys.path.insert(0, 'lib')

# Import only what we need
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox

def print_datalim(*ax):
    for ax_ in ax:
        print(ax_.dataLim.intervaly, end=' / ')
    print()

# Simple test data
x = np.array([0, 1])
y1 = np.array([-22.7, 26.6])
y2 = np.array([-0.085, -2.98])

print("Reproducing the issue:")

fig, ax1 = plt.subplots()

ax1.stackplot(x, y1)
print("After stackplot on ax1:", end=" ")
print_datalim(ax1)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
print("After creating twinx:", end=" ")
print_datalim(ax1, ax2)

ax2.plot(x, y2)
print("After plot on ax2:", end=" ")
print_datalim(ax1, ax2)

plt.close('all')
print("Test completed")